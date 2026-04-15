#!/usr/bin/env bash
set -euo pipefail

python -m ipykernel install \
  --user \
  --name plotnine-polars \
  --display-name "Python (plotnine-polars)"
