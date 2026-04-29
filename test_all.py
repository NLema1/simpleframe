"""Test every method in simpleframe to make sure it works end-to-end."""

from simpleframe import I_want_a, I_want_to

print("=" * 60)
print("TEST 1: Creation + basic transformations")
print("=" * 60)

df = I_want_a.dataframe({
    "name": ["Alice", "Bob", "Charlie", "Dana", "Eve"],
    "age": [30, 25, 35, 28, 42],
    "salary": [50000, 60000, 70000, 55000, 90000],
    "region": ["East", "West", "East", "West", "East"],
})

df = I_want_to.filter(df, where="age > 26")
df = I_want_to.add_column(df, name="bonus", formula="salary * 0.1")
df = I_want_to.sort(df, by="bonus", descending=True)
df.see()

print("\n--- show_polars output ---")
df.show_polars()

print("\n" + "=" * 60)
print("TEST 2: group_and_summarize")
print("=" * 60)

df2 = I_want_a.dataframe({
    "region": ["East", "West", "East", "West", "East"],
    "revenue": [100, 200, 150, 250, 175],
})
df2 = I_want_to.group_and_summarize(df2, group_by="region", summarize="revenue", using="sum")
df2.see()
print()
df2.show_polars()

print("\n" + "=" * 60)
print("TEST 3: join")
print("=" * 60)

people = I_want_a.dataframe({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"]})
scores = I_want_a.dataframe({"id": [1, 2, 3], "score": [90, 85, 95]})
joined = I_want_to.join(people, scores, on="id", how="inner")
joined.see()
print()
joined.show_polars()

print("\n" + "=" * 60)
print("TEST 4: missing values")
print("=" * 60)

import polars as pl
raw = pl.DataFrame({"name": ["Alice", "Bob", None], "age": [30, None, 25]})
df3 = I_want_to.fill_missing(raw, column="age", with_value=0)
df3 = I_want_to.drop_missing(df3, columns=["name"])
df3.see()
print()
df3.show_polars()

print("\n" + "=" * 60)
print("TEST 5: string operations")
print("=" * 60)

df4 = I_want_a.dataframe({"name": ["alice smith", "bob jones", "charlie brown"]})
df4 = I_want_to.uppercase(df4, column="name")
df4 = I_want_to.split_column(df4, column="name", on=" ", into=["first", "last"])
df4.see()
print()
df4.show_polars()

print("\n" + "=" * 60)
print("TEST 6: rename, drop, select")
print("=" * 60)

df5 = I_want_a.dataframe({"a": [1, 2], "b": [3, 4], "c": [5, 6]})
df5 = I_want_to.rename(df5, old="a", new="alpha")
df5 = I_want_to.drop(df5, columns="b")
df5 = I_want_to.select(df5, columns=["alpha", "c"])
df5.see()
print()
df5.show_polars()

print("\n" + "=" * 60)
print("TEST 7: keep_where_contains")
print("=" * 60)

df6 = I_want_a.dataframe({"name": ["Alice", "Bob", "Albert"]})
df6 = I_want_to.keep_where_contains(df6, column="name", text="Al")
df6.see()
print()
df6.show_polars()

print("\n\nALL TESTS PASSED ✓")
