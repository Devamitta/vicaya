# Colored console output with timing helpers for the vicaya pipeline.
import time
from datetime import datetime
from typing import ClassVar, Union

_GREEN = "\033[32m"
_RED = "\033[31m"
_YELLOW = "\033[33m"
_BRIGHT_YELLOW = "\033[93m"
_CYAN = "\033[36m"
_WHITE = "\033[37m"
_RESET = "\033[0m"


class Printer:
    """Colored terminal output with optional mini and main timing."""

    _ticx: ClassVar[datetime | None] = None

    def __init__(self):
        self.start_time: float | None = None

    @classmethod
    def tic(cls) -> None:
        cls._ticx = datetime.now()

    @classmethod
    def toc(cls) -> None:
        if cls._ticx is None:
            print(f"{_RED}Error: tic() not called before toc(){_RESET}")
            return
        elapsed = datetime.now() - cls._ticx
        print(f"{_CYAN}{'-' * 40}{_RESET}")
        print(f"{_CYAN}{elapsed}{_RESET}")

    def bip(self) -> None:
        self.start_time = time.time()

    def bop(self) -> str:
        if self.start_time is None:
            return "0.000"
        return f"{time.time() - self.start_time:.3f}"

    def print_bop(self) -> None:
        print(f"{self.bop():>10}")

    def yellow_title(self, text: str) -> None:
        print(f"{_BRIGHT_YELLOW}{text}{_RESET}")
        self.bip()

    def green_title(self, text: str) -> None:
        print(f"{_GREEN}{text}{_RESET}")
        self.bip()

    def green_tmr(self, text: str) -> None:
        print(f"{_GREEN}{text:<35}{_RESET}", end="")
        self.bip()

    def cyan_tmr(self, text: str) -> None:
        print(f"{_CYAN}{text:<35}{_RESET}", end="")
        self.bip()

    def yes(self, message: Union[int, str]) -> None:
        formatted = f"{message:>10,}" if isinstance(message, int) else f"{message:>10}"
        print(f"{_GREEN}{formatted}{_RESET}", end="")
        self.print_bop()

    def no(self, message: Union[int, str]) -> None:
        formatted = f"{message:>10,}" if isinstance(message, int) else f"{message:>10}"
        print(f"{_RED}{formatted}{_RESET}", end="")
        self.print_bop()

    def green(self, text: str) -> None:
        print(f"{_GREEN}{text}{_RESET}")

    def red(self, text: str) -> None:
        print(f"{_RED}{text}{_RESET}")

    def amber(self, text: str) -> None:
        print(f"{_YELLOW}{text}{_RESET}")

    def warning(self, text: str) -> None:
        print(f"{_YELLOW}! {text}{_RESET}")

    def cyan(self, text: str) -> None:
        print(f"{_CYAN}{text}{_RESET}")

    def white(self, text: str) -> None:
        print(f"{_WHITE}{text}{_RESET}")

    def summary(self, key: str, value: Union[str, int]) -> None:
        print(f"{_GREEN}{key:<20}{_RESET}{value}")

    def counter(self, count: int, total: int, word: str) -> None:
        print(f"{count:>10,} / {total:<10,} {word[:20]:<20} {self.bop():>10}")
        self.bip()


_pr = Printer()

# Module-level functions — backward-compatible API used by scripts
def green(text: str) -> None: _pr.green(text)
def yes(message: Union[int, str]) -> None: _pr.yes(message)
def no(message: Union[int, str]) -> None: _pr.no(message)
def warning(text: str) -> None: _pr.warning(text)
def red(text: str) -> None: _pr.red(text)
def amber(text: str) -> None: _pr.amber(text)
def cyan(text: str) -> None: _pr.cyan(text)
def white(text: str) -> None: _pr.white(text)
def yellow_title(text: str) -> None: _pr.yellow_title(text)
def green_title(text: str) -> None: _pr.green_title(text)
def green_tmr(text: str) -> None: _pr.green_tmr(text)
def cyan_tmr(text: str) -> None: _pr.cyan_tmr(text)
def bip() -> None: _pr.bip()
def bop() -> str: return _pr.bop()
def tic() -> None: Printer.tic()
def toc() -> None: Printer.toc()
def summary(key: str, value: Union[str, int]) -> None: _pr.summary(key, value)
def counter(count: int, total: int, word: str) -> None: _pr.counter(count, total, word)
