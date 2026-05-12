"""Integration tests for research_sources helpers.

These tests hit the real local systems (Obsidian CLI, sqlite canon db, calibredb).
They're skipped automatically when the underlying tool or data isn't available, so
the suite stays green on a machine that doesn't have everything wired up yet.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.research_sources import (  # noqa: E402
    DEFAULT_CALIBRE_LIBRARY,
    DEFAULT_CANON_DB,
    DEFAULT_DPD_DB,
    CalibreHit,
    CanonHit,
    VaultHit,
    gemini_cross_check,
    resolve_citation,
    search_calibre,
    search_canon,
    search_vault,
)

# ---------- skip markers ----------

obsidian_available = pytest.mark.skipif(
    shutil.which("obsidian") is None, reason="obsidian CLI not installed"
)
calibre_available = pytest.mark.skipif(
    shutil.which("calibredb") is None or not DEFAULT_CALIBRE_LIBRARY.exists(),
    reason="calibredb or library not available",
)
canon_available = pytest.mark.skipif(
    not DEFAULT_CANON_DB.exists(), reason="canon db not available"
)
gemini_available = pytest.mark.skipif(
    shutil.which("gemini") is None, reason="gemini CLI not installed"
)
dpd_available = pytest.mark.skipif(
    DEFAULT_DPD_DB is None or not DEFAULT_DPD_DB.exists(),
    reason="dpd.db not configured (VICAYA_DPD_DB)",
)


# ---------- resolve_citation ----------


class TestResolveCitation:
    """Fallback behaviour — no dpd.db needed."""

    def test_machine_field(self):
        c = resolve_citation("s0201m_mul", "23")
        assert c.machine == "s0201m_mul:23"

    def test_mn_fallback_contains_nikaya_and_paranum(self):
        c = resolve_citation("s0201m_mul", "23")
        assert "MN" in c.human
        assert "23" in c.human
        assert c.pitaka == "Sutta"
        assert c.text_type == "mūla"

    def test_dn_fallback(self):
        c = resolve_citation("s0101m_mul", "1")
        assert "DN" in c.human
        assert c.pitaka == "Sutta"

    def test_vinaya_attakatha_fallback(self):
        c = resolve_citation("vin01a_att", "5")
        assert c.pitaka == "Vinaya"
        assert "aṭṭhakathā" in c.human
        assert "5" in c.human

    def test_abhidhamma_tika_fallback(self):
        c = resolve_citation("abh02t_tik", "7")
        assert c.pitaka == "Abhidhamma"
        assert "ṭīkā" in c.human

    def test_extra(self):
        c = resolve_citation("e0101n_mul", "1")
        assert c.pitaka == "Extra"

    def test_unknown_falls_back_gracefully(self):
        c = resolve_citation("xyz999_mul", "1")
        assert "1" in c.human


@dpd_available
class TestResolveCitationWithDPD:
    """DPD-backed lookup — skipped when VICAYA_DPD_DB is not set."""

    def test_mn60_para_97(self):
        c = resolve_citation("s0202m_mul", "97")
        assert c.human == "MN60 Apaṇṇakasuttaṃ para 97"
        assert c.machine == "s0202m_mul:97"
        assert c.pitaka == "Sutta"

    def test_an_kesamutti(self):
        c = resolve_citation("s0402m2_mul", "66")
        assert "Kesamutti" in c.human
        assert "para 66" in c.human

    def test_commentary_mn60(self):
        c = resolve_citation("s0202a_att", "92")
        assert c.human == "MNa60 para 92"
        assert c.pitaka == "Commentary"

    def test_range_paranum(self):
        c = resolve_citation("s0202m_mul", "97-99")
        assert "MN60" in c.human
        assert "para 97–99" in c.human

    def test_dn1(self):
        c = resolve_citation("s0101m_mul", "1")
        assert "DN1" in c.human
        assert "Brahmajāla" in c.human


# ---------- search_canon ----------


@canon_available
class TestSearchCanon:
    def test_pali_search_in_mn(self):
        hits = search_canon("dukkha", books=["s0201m_mul"], lang="pali", limit=3)
        assert len(hits) > 0
        for h in hits:
            assert isinstance(h, CanonHit)
            assert h.book_code == "s0201m_mul"
            assert "dukkha" in h.pali.lower()

    def test_english_search(self):
        hits = search_canon(
            "suffering", books=["s0201m_mul"], lang="english", limit=3
        )
        # English translations may be sparse; tolerate empty result but not crash.
        for h in hits:
            assert "suffering" in h.english.lower()

    def test_prefix_expansion(self):
        hits = search_canon("dukkha", books=["s02*"], lang="pali", limit=5)
        assert len(hits) > 0
        # All hits should come from s02* tables.
        for h in hits:
            assert h.book_code.startswith("s02")

    def test_default_scope_is_suttas(self):
        # No `books` arg -> defaults to s*_mul tables.
        hits = search_canon("buddho", limit=3)
        for h in hits:
            assert h.book_code.startswith("s")


# ---------- search_vault ----------


@obsidian_available
class TestSearchVault:
    def test_search_returns_list(self):
        # We don't know what's in the vault; just verify the call shape works.
        hits = search_vault("the", limit=3)
        assert isinstance(hits, list)
        for h in hits:
            assert isinstance(h, VaultHit)


# ---------- search_calibre ----------


@calibre_available
class TestSearchCalibre:
    def test_metadata_search_by_tag(self):
        hits = search_calibre("", tags=["Buddhism"], limit=3)
        assert isinstance(hits, list)
        for h in hits:
            assert isinstance(h, CalibreHit)
            assert h.book_id > 0
            assert h.title

    def test_search_returns_calibre_hits(self):
        hits = search_calibre("Buddha", limit=3)
        assert isinstance(hits, list)


# ---------- gemini_cross_check ----------


@gemini_available
class TestGeminiCrossCheck:
    def test_trivial_prompt_returns_text(self):
        # Trivial call; just verify the subprocess works and we get a string.
        out = gemini_cross_check("Reply with the single word: pong")
        assert isinstance(out, str)
        # Don't assert content — model may be chatty. Empty string is also fine
        # (means timeout/error path was hit cleanly without crashing).


class TestChannelAllowlist:
    def test_channel_allowlist_parses(self, tmp_path):
        from tools.research_sources import load_channel_allowlist

        f = tmp_path / "channels.md"
        f.write_text(
            "# header\n\n"
            "## Format\n\n"
            "```\n## trusted\n- Example In Fence\n```\n\n"
            "## trusted\n- Trusted A | UC1111111111111111111111\n\n"
            "## probationary\n- Prob A\n- Prob B | UC2222222222222222222222\n\n"
            "## excluded\n- Bad Channel\n",
            encoding="utf-8",
        )
        a = load_channel_allowlist(f)
        assert sorted(a.keys()) == ["excluded", "probationary", "trusted"]
        assert [c["name"] for c in a["trusted"]] == ["Trusted A"]
        assert a["trusted"][0]["channel_id"] == "UC1111111111111111111111"
        assert [c["name"] for c in a["probationary"]] == ["Prob A", "Prob B"]
        assert [c["name"] for c in a["excluded"]] == ["Bad Channel"]
        assert not any(c["name"] == "Example In Fence" for c in a["trusted"])

    def test_seeded_allowlist_loads_with_probationary_entries(self):
        from tools.research_sources import load_channel_allowlist

        a = load_channel_allowlist()
        assert len(a["probationary"]) >= 9


class TestSearchYouTube:
    def test_search_youtube_parses_yt_dlp_stdout(self, monkeypatch):
        from tools.research_sources import YouTubeHit, search_youtube

        fake_stdout = (
            "vid1|||Talk One|||Buddhist Insights @ Empty Cloud|||UCabc|||1234.5\n"
            "vid2|||Talk Two|||Random Slop Channel|||UCdef|||NA\n"
            "vid3|||Talk Three|||Buddha Tube|||UCghi|||60.0\n"
        )

        class Result:
            returncode = 0
            stdout = fake_stdout

        monkeypatch.setattr(
            "tools.research_sources.subprocess.run",
            lambda *a, **kw: Result(),
        )
        allowlist = {
            "trusted": [{"name": "Buddhist Insights @ Empty Cloud", "channel_id": ""}],
            "probationary": [],
            "excluded": [{"name": "Buddha Tube", "channel_id": ""}],
        }
        hits = search_youtube("anything", channels=allowlist, limit=10)
        assert len(hits) == 2
        assert all(isinstance(h, YouTubeHit) for h in hits)
        first = hits[0]
        assert first.video_id == "vid1"
        assert first.title == "Talk One"
        assert first.tier == "trusted"
        assert first.duration == 1234.5
        assert first.url == "https://youtu.be/vid1"
        assert hits[1].duration is None
        assert hits[1].tier == "probationary"


class TestTranscriptCache:
    def test_transcript_cache_hit_skips_network(self, tmp_path, monkeypatch):
        import json
        from dataclasses import asdict

        from tools.research_sources import (
            YouTubeTranscript,
            fetch_youtube_transcript,
        )

        cached = YouTubeTranscript(
            video_id="cachedvid",
            lang="en",
            is_auto=False,
            segments=[{"start": 0.0, "duration": 1.0, "text": "hello"}],
            fetched="2026-05-12",
        )
        (tmp_path / "cachedvid.json").write_text(
            json.dumps(asdict(cached)), encoding="utf-8"
        )

        def _boom(*a, **kw):
            raise AssertionError("network must not be called on cache hit")

        try:
            import youtube_transcript_api
            monkeypatch.setattr(
                youtube_transcript_api.YouTubeTranscriptApi, "__init__", _boom
            )
        except ImportError:
            pass

        result = fetch_youtube_transcript("cachedvid", cache_dir=tmp_path)
        assert result is not None
        assert result.video_id == "cachedvid"
        assert result.is_auto is False
        assert result.segments[0]["text"] == "hello"
