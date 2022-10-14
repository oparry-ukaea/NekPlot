import os.path
import sys

# Store some useful locations in a dict
LOCATIONS = {}
LOCATIONS["root"]         = os.path.abspath(os.path.dirname(__file__)+"/..")
LOCATIONS["demos"]        = os.path.join(LOCATIONS["root"],"demos")
LOCATIONS["data"]         = os.path.join(LOCATIONS["demos"],"data")
LOCATIONS["sol1D"]        = os.path.join(LOCATIONS["data"],"sol1D")
LOCATIONS["convection2D"] = os.path.join(LOCATIONS["data"],"convection_2d")

# Add NekPlot root to sys.path. Avoids need to keep reinstalling during development.
sys.path.append(LOCATIONS["root"])