import os.path
import sys

# Store some useful locations in a dict
LOCATIONS = {}
LOCATIONS["root"]  = os.path.abspath(os.path.dirname(__file__)+"/..")
LOCATIONS["demos"] = os.path.join(LOCATIONS["root"],"demos")
LOCATIONS["data"]  = os.path.join(LOCATIONS["demos"],"data")
LOCATIONS["sol1D"] = os.path.join(LOCATIONS["data"],"sol1D")

# Add NekPlot root to sys.path. Avoids needing to keep reinstalling during development.
sys.path.append(LOCATIONS["root"])