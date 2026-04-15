import polars as pl
from plotnine import aes, coord_trans, facet_null, geom_line, geom_point, labs
from plotnine import scale_x_continuous

import plotnine_polars
from plotnine_polars import ggplot


def test_namespace_returns_fluent_plot():
    df = pl.DataFrame({"x": [1, 2, 3], "y": [3, 2, 1]})

    plot = df.ggplot()

    assert isinstance(plot, ggplot)
    assert plot.data is df


def test_plot_method_matches_call():
    df = pl.DataFrame({"x": [1, 2, 3], "y": [3, 2, 1]})

    plot = df.ggplot.plot()

    assert isinstance(plot, ggplot)
    assert plot.data is df


def test_fluent_api_matches_plotnine_addition():
    df = pl.DataFrame({"x": [1, 2, 3], "y": [3, 2, 1]})

    plot = (
        df.ggplot()
        .aes("x", "y")
        .geom_point(color="red")
        .geom_line()
        .labs(title="fluent")
        .scale_x_continuous()
        .coord_trans()
        .facet_null()
    )
    expected = (
        ggplot(df)
        + aes("x", "y")
        + geom_point(color="red")
        + geom_line()
        + labs(title="fluent")
        + scale_x_continuous()
        + coord_trans()
        + facet_null()
    )

    assert plot.mapping == expected.mapping
    assert len(plot.layers) == len(expected.layers)
    assert [layer.geom.__class__ for layer in plot.layers] == [
        layer.geom.__class__ for layer in expected.layers
    ]
    assert plot.labels == expected.labels
    assert plot.coordinates.__class__ is expected.coordinates.__class__
    assert plot.facet.__class__ is expected.facet.__class__
    assert len(plot.scales) == len(expected.scales)


def test_fluent_api_handles_name_collisions():
    df = pl.DataFrame({"x": [1, 2, 3], "y": [3, 2, 1]})

    themed_plot = (
        df.ggplot(aes("x", "y"))
        .geom_point()
        .add_theme(aspect_ratio=1)
    )
    guided_plot = themed_plot.add_guides(color="none").theme_gray()

    assert themed_plot.theme.getp("aspect_ratio") == 1
    assert guided_plot.guides.color == "none"
    assert hasattr(guided_plot.theme, "getp")
    assert callable(guided_plot.add_theme)
    assert callable(guided_plot.add_guides)
    assert callable(guided_plot.theme_gray)


def test_import_registers_namespace():
    assert plotnine_polars is not None
    assert hasattr(pl.DataFrame({"x": [1]}), "ggplot")
