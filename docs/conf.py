# Configuration file for the Sphinx documentation builder.

# -- Project information
import site
import pathlib
import sys
import os

print("\n=== RTD Python Environment ===")
print(f"sys.executable: {sys.executable}")
print(f"sys.path:\n  " + "\n  ".join(sys.path))

# Try to find site-packages
try:
    site_packages = site.getsitepackages()
except AttributeError:
    site_packages = [p for p in sys.path if 'site-packages' in p]

print("\n=== Contents of site-packages/thermo_flux ===")
for path in site_packages:
    thermo_path = os.path.join(path, "thermo_flux")
    if os.path.exists(thermo_path):
        for f in pathlib.Path(thermo_path).rglob("*"):
            print(f"  {f.relative_to(thermo_path.parent)}")
    else:
        print(f"  [Not found in: {path}]")

try:
    import thermo_flux.core
    print("✅ Import successful")
except Exception as e:
    print(f"❌ Import failed: {e}")

project = 'Thermo-flux'
copyright = '2024, E.N.Smith'
author = 'E.N.Smith'

#release = '0.1'
#version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]


intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

#html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
#epub_show_urls = 'footnote'
