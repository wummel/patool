"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import sys
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "patool"
version = "4.0.0"
author = "Bastian Kleineidam"
copyright = '2024 ' + author


def add_patoolib_path():
    """Add the parent directory to sys.path to find patoolib,
    which is used by the sphinx.ext.autodoc extension.
    """
    import pathlib

    basepath = pathlib.Path(__file__).parents[3]
    sys.path.append(str(basepath))
    # test importing patoolib
    import patoolib  # noqa: F401


add_patoolib_path()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
]

templates_path = ['_templates']
exclude_patterns = []

source_suffix = '.md'
language = 'en'

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

html_theme_options = {
    'nosidebar': True,
    'show_powered_by': False,
    'show_relbars': False,
}

pygments_style = 'rrt'
