#! /usr/bin/env python
"""Standalone script to update all dependencies in pyproject.toml with their latest versions.
The dependencies must be pinned with "==", else they are skipped.
"""

import sys
import tomllib
import subprocess
import os


def usage():
    """Print usage info"""
    print("./update_pyproject_toml_deps.py <path to pyproject.toml>")
    sys.exit(1)


def update_pkg(group, pkg, newversion, projectdir, optional=False):
    """Update one package in pyproject.toml and sync the virtual environment by downloading the new version."""
    command = ["uv", "add", "--project", projectdir, "--quiet", "--color=never"]
    if optional:
        command.append("--optional")
        command.append(group)
    elif group:
        command.append("--group")
        command.append(group)
    command.append(f"{pkg}=={newversion}")
    subprocess.check_call(command)


def main(args):
    """Update all dependencies in a pyproject.toml file."""
    if not args:
        print("ERROR: no pyproject.toml file given")
        usage()
    pyproject_path = args[0]
    if not os.path.isfile(pyproject_path):
        print(f"ERROR: path {pyproject_path} not found")
        usage()
    projectdir = os.path.abspath(os.path.dirname(pyproject_path))

    # parse pyproject.toml
    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    # update project dependencies
    update_dependencies(None, pyproject["project"]["dependencies"], projectdir)
    # update optional dependencies
    for group, dependencies in (
        pyproject["project"].get("optional-dependencies", []).items()
    ):
        update_dependencies(group, dependencies, projectdir, optional=True)
    # update dependency groups
    for group, dependencies in pyproject.get("dependency-groups", {}).items():
        update_dependencies(group, dependencies, projectdir)


def update_dependencies(group, dependencies, projectdir, optional=False):
    """Update given dependency list."""
    for dep in dependencies:
        if "==" not in dep:
            print(f"WARN: skip non-pinned dependency {dep!r} in group {group}")
            continue
        pkg, version = dep.split("==", 1)
        # use uv pip compile to get the newest version
        command = [
            "uv",
            "pip",
            "compile",
            "-",
            "--color=never",
            "--quiet",
            "--no-deps",
            "--no-header",
            "--no-annotate",
        ]
        res = subprocess.run(
            command, input=pkg, text=True, check=True, capture_output=True
        )
        newdep = res.stdout.strip()
        newversion = newdep.split("==", 1)[1]
        if newversion != version:
            print("INFO: update", dep, "-->", newversion)
            update_pkg(group, pkg, newversion, projectdir, optional=optional)


if __name__ == "__main__":
    main(sys.argv[1:])
