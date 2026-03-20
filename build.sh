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
info "Upgrading pip"
"$PY" -m pip install --no-cache-dir --upgrade pip
info "Installing build requirements"
"$PY" -m pip install --no-cache-dir -r ./build/requirements.txt

# Running build steps
info "Generating build info"
"$PY" ./build/generate_build_info.py
info "Building package"
"$PY" -m build
info "SVGPatcher build done!"