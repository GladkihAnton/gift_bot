#!/bin/sh

set -x

# Sort imports one per line, so autoflake can remove unused imports
isort --force-single-line-imports .
autoflake --remove-all-unused-imports --recursive --remove-unused-variables --ignore-init-module-imports --in-place .
# Sort imports back
isort .
black .
