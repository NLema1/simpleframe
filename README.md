# simpleframe

**Readable Polars wrappers so AI-generated data code makes sense to humans.**

> **Pre-release.** Not yet on PyPI. Install directly from GitHub:
> ```bash
> pip install git+https://github.com/NLema1/simpleframe.git
> ```

## The problem

The vibe-coding era has an interpretability problem. AI writes code, you run it, and you have no idea what just happened.

`simpleframe` fixes that for dataframes. Tell AI to use `simpleframe` and the code it produces reads like English. When you're ready, call `.show_polars()` to see the real Polars equivalent and graduate.

Don't stop using AI — stop being blind to what it's doing.

## See it

```python
# What AI usually writes:
df = pl.read_csv("sales.csv").filter(pl.col("amount") > 100).group_by("region").agg(pl.col("amount").sum())

# What AI writes when you ask it to use simpleframe:
df = I_want_a.csv("sales.csv")
df = I_want_to.filter(df, where="amount > 100")
df = I_want_to.group_and_summarize(df, group_by="region", summarize="amount", using="sum")
```

When you want to learn the real syntax:

```python
df.show_polars()
```

```text
import polars as pl

df = pl.read_csv("sales.csv")
df = df.sql("SELECT * FROM self WHERE amount > 100")
df = df.group_by("region").agg(pl.col("amount").sum().alias("amount"))
```

## Quick start

```python
from simpleframe import I_want_a, I_want_to

df = I_want_a.dataframe({
    "name": ["Alice", "Bob", "Charlie"],
    "age": [30, 25, 35],
    "salary": [50000, 60000, 70000],
})

df = I_want_to.filter(df, where="age > 26")
df = I_want_to.add_column(df, name="bonus", formula="salary * 0.1")
df = I_want_to.sort(df, by="bonus", descending=True)

df.see()           # print the data
df.show_polars()   # print the real Polars code
```

## What's in v1

**Creation (`I_want_a`):** `dataframe`, `csv`, `excel`, `json`, `parquet`, `sample`

**Transformations (`I_want_to`):** `filter`, `sort`, `select`, `add_column`, `rename`, `drop`, `group_and_summarize`, `join`, `fill_missing`, `drop_missing`, `uppercase`, `lowercase`, `keep_where_contains`, `split_column`

**On any SimpleFrame:** `.see()`, `.show_polars()`, `.to_polars()`

## Tell AI to use it

Drop this in your AI prompt:

> Use the `simpleframe` Python package. Import `I_want_a` for creating dataframes and `I_want_to` for transformations. Methods read like English, e.g. `I_want_to.filter(df, where="age > 30")`.

## Status

Pre-release. API may change based on feedback. Issues and feedback welcome.

## License

MIT
