"""I_want_to — transformation methods for SimpleFrame.

Each method returns a new SimpleFrame and appends the equivalent Polars
code to its history so users can call `.show_polars()` and learn the real syntax.
"""

from __future__ import annotations
import polars as pl
from .core import SimpleFrame


def _ensure(sf) -> SimpleFrame:
    """Accept either a SimpleFrame or a raw Polars DataFrame."""
    if isinstance(sf, SimpleFrame):
        return sf
    if isinstance(sf, pl.DataFrame):
        return SimpleFrame(sf, ["# (existing polars dataframe)"])
    raise TypeError(
        f"Expected a SimpleFrame or polars DataFrame, got {type(sf).__name__}"
    )


class _IWantTo:
    """Methods for transforming dataframes."""

    # ---------- filter / sort / select ----------

    @staticmethod
    def filter(sf, where: str) -> SimpleFrame:
        """Keep only rows matching `where` (a Polars SQL-style expression).

        Example: I_want_to.filter(df, where="age > 30")
        """
        sf = _ensure(sf)
        new_df = sf.to_polars().sql(f"SELECT * FROM self WHERE {where}")
        code = f'df = df.sql("SELECT * FROM self WHERE {where}")'
        return sf._chain(new_df, code)

    @staticmethod
    def sort(sf, by: str | list[str], descending: bool = False) -> SimpleFrame:
        """Sort rows by a column (or list of columns)."""
        sf = _ensure(sf)
        new_df = sf.to_polars().sort(by, descending=descending)
        code = f"df = df.sort({by!r}, descending={descending})"
        return sf._chain(new_df, code)

    @staticmethod
    def select(sf, columns: list[str]) -> SimpleFrame:
        """Keep only the named columns."""
        sf = _ensure(sf)
        new_df = sf.to_polars().select(columns)
        code = f"df = df.select({columns!r})"
        return sf._chain(new_df, code)

    # ---------- add / rename / drop ----------

    @staticmethod
    def add_column(sf, name: str, formula: str) -> SimpleFrame:
        """Add a new column computed from a Polars expression string.

        Example: I_want_to.add_column(df, name="bonus", formula="salary * 0.1")
        """
        sf = _ensure(sf)
        new_df = sf.to_polars().sql(f"SELECT *, ({formula}) AS {name} FROM self")
        code = f'df = df.sql("SELECT *, ({formula}) AS {name} FROM self")'
        return sf._chain(new_df, code)

    @staticmethod
    def rename(sf, old: str, new: str) -> SimpleFrame:
        """Rename a single column."""
        sf = _ensure(sf)
        new_df = sf.to_polars().rename({old: new})
        code = f'df = df.rename({{"{old}": "{new}"}})'
        return sf._chain(new_df, code)

    @staticmethod
    def drop(sf, columns: str | list[str]) -> SimpleFrame:
        """Remove a column (or list of columns)."""
        sf = _ensure(sf)
        cols = [columns] if isinstance(columns, str) else columns
        new_df = sf.to_polars().drop(cols)
        code = f"df = df.drop({cols!r})"
        return sf._chain(new_df, code)

    # ---------- group + summarize ----------

    @staticmethod
    def group_and_summarize(
        sf,
        group_by: str | list[str],
        summarize: str,
        using: str = "sum",
    ) -> SimpleFrame:
        """Group rows by one or more columns, then summarize another column.

        `using` can be: "sum", "mean", "min", "max", "count", "median".
        Example: I_want_to.group_and_summarize(df, group_by="region", summarize="revenue", using="sum")
        """
        sf = _ensure(sf)
        agg_map = {
            "sum": pl.col(summarize).sum(),
            "mean": pl.col(summarize).mean(),
            "average": pl.col(summarize).mean(),
            "min": pl.col(summarize).min(),
            "max": pl.col(summarize).max(),
            "count": pl.col(summarize).count(),
            "median": pl.col(summarize).median(),
        }
        if using not in agg_map:
            raise ValueError(
                f"`using` must be one of {list(agg_map)}, got '{using}'"
            )
        new_df = sf.to_polars().group_by(group_by).agg(agg_map[using].alias(summarize))
        code = (
            f"df = df.group_by({group_by!r})"
            f".agg(pl.col({summarize!r}).{using}().alias({summarize!r}))"
        )
        return sf._chain(new_df, code)

    # ---------- join ----------

    @staticmethod
    def join(sf_left, sf_right, on: str | list[str], how: str = "inner") -> SimpleFrame:
        """Join two dataframes on a shared column (or columns).

        `how` can be: "inner", "left", "right", "full", "cross".
        """
        left = _ensure(sf_left)
        right = _ensure(sf_right)
        new_df = left.to_polars().join(right.to_polars(), on=on, how=how)
        code = f"df = df.join(other_df, on={on!r}, how={how!r})"
        return left._chain(new_df, code)

    # ---------- missing values ----------

    @staticmethod
    def fill_missing(sf, column: str, with_value) -> SimpleFrame:
        """Replace null/missing values in `column` with `with_value`."""
        sf = _ensure(sf)
        new_df = sf.to_polars().with_columns(
            pl.col(column).fill_null(with_value).alias(column)
        )
        code = f"df = df.with_columns(pl.col({column!r}).fill_null({with_value!r}))"
        return sf._chain(new_df, code)

    @staticmethod
    def drop_missing(sf, columns: str | list[str] | None = None) -> SimpleFrame:
        """Drop rows with missing values in the given column(s).

        If `columns` is None, drops any row with any missing value.
        """
        sf = _ensure(sf)
        if columns is None:
            new_df = sf.to_polars().drop_nulls()
            code = "df = df.drop_nulls()"
        else:
            cols = [columns] if isinstance(columns, str) else columns
            new_df = sf.to_polars().drop_nulls(subset=cols)
            code = f"df = df.drop_nulls(subset={cols!r})"
        return sf._chain(new_df, code)

    # ---------- string operations ----------

    @staticmethod
    def uppercase(sf, column: str) -> SimpleFrame:
        """Convert a string column to UPPERCASE."""
        sf = _ensure(sf)
        new_df = sf.to_polars().with_columns(
            pl.col(column).str.to_uppercase().alias(column)
        )
        code = f"df = df.with_columns(pl.col({column!r}).str.to_uppercase())"
        return sf._chain(new_df, code)

    @staticmethod
    def lowercase(sf, column: str) -> SimpleFrame:
        """Convert a string column to lowercase."""
        sf = _ensure(sf)
        new_df = sf.to_polars().with_columns(
            pl.col(column).str.to_lowercase().alias(column)
        )
        code = f"df = df.with_columns(pl.col({column!r}).str.to_lowercase())"
        return sf._chain(new_df, code)

    @staticmethod
    def keep_where_contains(sf, column: str, text: str) -> SimpleFrame:
        """Keep only rows where `column` contains `text`."""
        sf = _ensure(sf)
        new_df = sf.to_polars().filter(pl.col(column).str.contains(text))
        code = f"df = df.filter(pl.col({column!r}).str.contains({text!r}))"
        return sf._chain(new_df, code)

    @staticmethod
    def split_column(sf, column: str, on: str, into: list[str]) -> SimpleFrame:
        """Split a string column on a delimiter into multiple new columns."""
        sf = _ensure(sf)
        split_expr = pl.col(column).str.split(on)
        new_cols = [
            split_expr.list.get(i, null_on_oob=True).alias(name)
            for i, name in enumerate(into)
        ]
        new_df = sf.to_polars().with_columns(new_cols)
        code = (
            f"df = df.with_columns([pl.col({column!r}).str.split({on!r})"
            f".list.get(i).alias(name) for i, name in enumerate({into!r})])"
        )
        return sf._chain(new_df, code)


I_want_to = _IWantTo()
