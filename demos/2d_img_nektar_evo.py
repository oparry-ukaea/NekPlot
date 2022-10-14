"""
Demonstrates
- reading of fields and 2D coords from nektar output files
"""
from demo_setup import LOCATIONS
from utils.plotting import plot_styles, plot_u_field
from NekPlot.data import get_source

nek_src = get_source("nektar", LOCATIONS["convection2D"], session_fnames=["convection_2d.xml", "convection_2d_mesh.xml"], label="convection 2D", file_base='convection_2d')
nek_src.set_plot_kws(plot_styles["convection2D"])
plot_u_field(nek_src)