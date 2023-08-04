#!/usr/bin/env bash

set -eo pipefail

REQUIREMENTS_LOCAL="/app/docker/requirements-local.txt"
#
# Make sure we have dev requirements installed
#
if [ -f "${REQUIREMENTS_LOCAL}" ]; then
  echo "Installing local overrides at ${REQUIREMENTS_LOCAL}"
  pip install --no-cache-dir -r "${REQUIREMENTS_LOCAL}"
else
  echo "Skipping local overrides"
fi

/usr/bin/run-server.sh
