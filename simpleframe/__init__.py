"""simpleframe — readable Polars wrappers so AI-generated data code makes sense.

Quick start:

    from simpleframe import I_want_a, I_want_to

    df = I_want_a.dataframe({"name": ["Alice", "Bob"], "age": [30, 25]})
    df = I_want_to.filter(df, where="age > 20")
    df.see()
    df.show_polars()   # prints the equivalent real Polars code
"""

from .core import SimpleFrame
from .creation import I_want_a
from .transform import I_want_to

__version__ = "0.1.0"
__all__ = ["SimpleFrame", "I_want_a", "I_want_to"]
