# Configuration file for the Sphinx documentation builder.

# -- Project information
import os 
import sys 
sys.path.append('/home/nathan/thermoflux-rtd')
sys.path.insert(0,'/home/nathan/thermoflux-rtd/thermo_flux/core/')
sys.path.insert(0, os.path.abspath('../thermo_flux/core/'))
try:
    import model
    print("✅ Import successful")
except Exception as e:
    print(f"❌ Import failed: {e}")

project = 'Thermo-flux'
copyright = '2024, E.N.Smith'
author = 'E.N.Smith'

release = '0.1'
version = '0.1.0'

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

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
