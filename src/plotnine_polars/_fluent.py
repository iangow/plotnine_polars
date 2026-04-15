from __future__ import annotations

from functools import wraps
from importlib import import_module
from typing import Any, Callable

from plotnine.ggplot import ggplot as plotnine_ggplot

coords = import_module("plotnine.coords")
facets = import_module("plotnine.facets")
geoms = import_module("plotnine.geoms")
guides = import_module("plotnine.guides")
labels = import_module("plotnine.labels")
mapping = import_module("plotnine.mapping")
positions = import_module("plotnine.positions")
scales = import_module("plotnine.scales")
stats = import_module("plotnine.stats")
themes = import_module("plotnine.themes")


def _make_method(factory: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(factory)
    def method(self, *args: Any, **kwargs: Any):
        return self + factory(*args, **kwargs)

    method.__doc__ = f"Fluent alias for `self + {factory.__name__}(...)`."
    return method


def _iter_methods() -> list[tuple[str, Callable[..., Any]]]:
    methods: list[tuple[str, Callable[..., Any]]] = [("aes", mapping.aes)]
    namespaces = (
        (coords, set()),
        (
            facets,
            {"as_labeller", "label_both", "label_context", "label_value", "labeller"},
        ),
        (geoms, {"arrow"}),
        (labels, set()),
        (positions, set()),
        (scales, set()),
        (stats, set()),
        (themes, {"theme", "theme_get", "theme_set", "theme_update"}),
        (guides, {"guides"}),
    )

    for namespace, skipped in namespaces:
        for name in namespace.__all__:
            if name in skipped:
                continue
            methods.append((name, getattr(namespace, name)))

    methods.extend(
        [
            ("add_theme", themes.theme),
            ("add_guides", guides.guides),
        ]
    )
    return methods


def add_fluent_methods(cls: type[Any]) -> None:
    def add(self, other: Any):
        return self + other

    if not hasattr(cls, "add"):
        setattr(cls, "add", add)

    for name, factory in _iter_methods():
        if hasattr(cls, name):
            continue
        setattr(cls, name, _make_method(factory))


class ggplot(plotnine_ggplot):
    """
    A `plotnine.ggplot` subclass with fluent plotting helpers.
    """


add_fluent_methods(ggplot)
