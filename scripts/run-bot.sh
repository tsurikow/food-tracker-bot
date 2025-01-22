#!/usr/bin/env bash

set -e

#alembic revision --autogenerate

alembic upgrade head
exec python -O -m app
