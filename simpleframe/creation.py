"""I_want_a — creation methods for SimpleFrame.

Usage:
    from simpleframe import I_want_a
    df = I_want_a.dataframe({"name": ["Alice", "Bob"], "age": [30, 25]})
    df = I_want_a.csv("data.csv")
"""

from __future__ import annotations
import polars as pl
from .core import SimpleFrame


class _IWantA:
    """Methods for creating dataframes."""

    @staticmethod
    def dataframe(data: dict) -> SimpleFrame:
        """Build a dataframe from a dictionary like {"name": [...], "age": [...]}."""
        df = pl.DataFrame(data)
        code = f"df = pl.DataFrame({data!r})"
        return SimpleFrame(df, [code])

    @staticmethod
    def csv(path: str) -> SimpleFrame:
        """Read a CSV file."""
        df = pl.read_csv(path)
        code = f'df = pl.read_csv("{path}")'
        return SimpleFrame(df, [code])

    @staticmethod
    def excel(path: str, sheet: str | None = None) -> SimpleFrame:
        """Read an Excel file. Optionally specify a sheet name."""
        if sheet:
            df = pl.read_excel(path, sheet_name=sheet)
            code = f'df = pl.read_excel("{path}", sheet_name="{sheet}")'
        else:
            df = pl.read_excel(path)
            code = f'df = pl.read_excel("{path}")'
        return SimpleFrame(df, [code])

    @staticmethod
    def json(path: str) -> SimpleFrame:
        """Read a JSON file."""
        df = pl.read_json(path)
        code = f'df = pl.read_json("{path}")'
        return SimpleFrame(df, [code])

    @staticmethod
    def parquet(path: str) -> SimpleFrame:
        """Read a Parquet file."""
        df = pl.read_parquet(path)
        code = f'df = pl.read_parquet("{path}")'
        return SimpleFrame(df, [code])

    @staticmethod
    def sample(rows: int = 10, columns: list[str] | None = None) -> SimpleFrame:
        """Generate a small sample dataframe with random integers — useful for testing."""
        import random
        if columns is None:
            columns = ["a", "b", "c"]
        data = {col: [random.randint(0, 100) for _ in range(rows)] for col in columns}
        df = pl.DataFrame(data)
        code = (
            f"# Random sample data\n"
            f"df = pl.DataFrame({{...{rows} rows × {len(columns)} cols...}})"
        )
        return SimpleFrame(df, [code])


# Public singleton — users do `from simpleframe import I_want_a`
I_want_a = _IWantA()
