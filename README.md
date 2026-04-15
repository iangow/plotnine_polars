# plotnine-polars

`plotnine-polars` adds a Polars dataframe namespace for `plotnine` and
exposes a fluent plotting API.

```python
import polars as pl
import plotnine_polars

df = pl.DataFrame({"x": [1, 2, 3], "y": [3, 2, 1]})

plot = (
    df.ggplot()
    .aes("x", "y")
    .geom_point()
    .geom_line()
)
```

This is equivalent to:

```python
from plotnine import aes, geom_line, geom_point, ggplot

plot = ggplot(df).add(aes("x", "y")).geom_point().geom_line()
```

Importing `plotnine_polars` registers the Polars namespace.
