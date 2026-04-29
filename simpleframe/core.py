"""Core SimpleFrame class — wraps a Polars DataFrame and tracks operations."""

from __future__ import annotations
import polars as pl


class SimpleFrame:
    """A wrapper around a Polars DataFrame that remembers what was done to it.

    Every transformation appends a line of equivalent Polars code to `history`.
    Call `.show_polars()` to see the real Polars code behind your work.
    Call `.see()` to print the data.
    Call `.to_polars()` to get the underlying Polars DataFrame.
    """

    def __init__(self, df: pl.DataFrame, history: list[str] | None = None):
        self._df = df
        self.history: list[str] = list(history) if history else []

    # ----- access helpers -----
    def to_polars(self) -> pl.DataFrame:
        """Return the underlying Polars DataFrame."""
        return self._df

    def see(self, rows: int = 10) -> SimpleFrame:
        """Print the first `rows` of the data. Returns self for chaining."""
        print(self._df.head(rows))
        return self

    def show_polars(self) -> SimpleFrame:
        """Print the equivalent Polars code for everything done so far."""
        if not self.history:
            print("# No operations yet.")
        else:
            print("import polars as pl")
            print()
            for line in self.history:
                print(line)
        return self

    # ----- internal -----
    def _chain(self, new_df: pl.DataFrame, code_line: str) -> SimpleFrame:
        """Return a new SimpleFrame with the operation appended to history."""
        return SimpleFrame(new_df, self.history + [code_line])

    # ----- pretty repr -----
    def __repr__(self) -> str:
        return f"SimpleFrame ({self._df.height} rows × {self._df.width} cols)\n{self._df}"
