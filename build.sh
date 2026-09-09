#!/usr/bin/env bash
set -e
set -o pipefail
info() {
    echo -e "\n$1\n"
}

# Defining variables
VENV="${VENV:-.venv_build}"
PY="$VENV/bin/python3"

# Removing existing build venv
info "Removing existing build venv"
rm -rf "$VENV"

# Creating build venv
info "Creating build venv"
python3.12 -m venv "$VENV"
info "Updating pip"
"$PY" -m pip install --upgrade pip
info "Installing or updating uv"
"$PY" -m pip install --upgrade uv
info "Installing or updating application and build dependencies"
"$PY" -m uv pip install --upgrade ".[build]"

# Running build steps
info "Checking version"
"$PY" ./build/check_version.py
info "Removing previous distribution artifacts"
rm -rf dist
info "Building package"
"$PY" -m uv build
info "hepreporter 'uv build' done!"
