from __future__ import annotations

import polars as pl

from ._fluent import ggplot


@pl.api.register_dataframe_namespace("ggplot")
class GGPlotNamespace:
    """
    Polars dataframe namespace for plotnine.
    """

    def __init__(self, dataframe: pl.DataFrame):
        self._dataframe = dataframe

    def __call__(self, *args, **kwargs) -> ggplot:
        return ggplot(self._dataframe, *args, **kwargs)

    def plot(self, *args, **kwargs) -> ggplot:
        return self(*args, **kwargs)
