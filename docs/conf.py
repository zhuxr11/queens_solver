import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "queens_solver"
copyright = "zhuxr11"
author = ", ".join(
    [
        "朱修锐 <zxr6@163.com>",
    ]
)

master_doc = "index"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "autoapi.extension",
    "sphinx.ext.viewcode",  # optional: adds links to source code
    # 'sphinx.ext.autosummary', # optional: generate summary tables
    "sphinx_multiversion",
]
# Auto-generate docs
autotype_api = "python"
autoapi_dirs = ["../queens_solver"]
autodoc_typehints = "description"  # show type hints in doc body
napoleon_google_docstring = False  # disable Google-style
napoleon_numpy_docstring = True  # parse NumPy style docstrings

# Handle warnings and skips
suppress_warnings = ["ref.python"]


def skip_attribute(app, what, name, obj, skip, options):
    if what == "attribute":
        return True
    elif what in ["function", "method"]:
        method_name = name.split(".")[-1]
        if method_name.startswith("_"):
            return True
    return skip


def setup(app):
    app.connect("autoapi-skip-member", skip_attribute)


templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_js_files = [
    "js/dynamic_version_links.js",  # dynamic version links generator
]
html_css_files = ["css/custom_style.css"]

html_sidebars = {
    "**": [
        "versioning.html",
    ],
}


# Sphinx multiversion setups
smv_tag_whitelist = r"^v\d+\.\d+\.\d+$"
smv_branch_whitelist = r"(master|dev)"
smv_outputdir_format = "{ref.name}"
smv_prefer_remote_refs = False
