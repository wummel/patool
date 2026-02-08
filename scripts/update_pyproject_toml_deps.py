#! /usr/bin/env -S uv run --script

"""Update all dependencies in pyproject.toml with their latest versions-
The dependencies must be pinned with "==".
"""

import sys
import tomllib
import subprocess
import os


def usage():
    """Print usage info"""
    print("./update_pyproject_toml_deps.py <path to pyproject.toml>")
    sys.exit(1)


def update_pkg(group, pkg, newversion, projectdir):
    """Update one package in pyproject.toml and sync the virtual environment by downloading the new version."""
    command = ["uv", "add", "--project", projectdir]
    if group:
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
    # update_dependencies(
    #    "optional-dependencies",
    #    pyproject["project"].get("optional-dependencies", []),
    #    projectdir,
    # )
    # update dependency groups
    for group, dependencies in pyproject.get("dependency-groups", {}).items():
        update_dependencies(group, dependencies, projectdir)


def update_dependencies(group, dependencies, projectdir):
    """Update given dependency list."""
    for dep in dependencies:
        if "==" not in dep:
            print("SKIP unversioned", group, dep)
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
            print("UPDATE", dep, "-->", newversion)
            update_pkg(group, pkg, newversion, projectdir)


if __name__ == "__main__":
    main(sys.argv[1:])
