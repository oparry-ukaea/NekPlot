# Add NekPlot root to sys.path. Avoids needing to keep reinstalling during development.
import os.path
import sys
nekplot_root = os.path.abspath(os.path.dirname(__file__)+"/..")
sys.path.append(nekplot_root)