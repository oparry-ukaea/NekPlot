"""
Demonstrates
- reading of 1D fields (rho, rhou, E) from nektar output
- calculation of derived fields (u from rhou,rho; T from rho,u,E)
- comparison with CSV data
"""

from demo_setup import LOCATIONS
from utils.plotting import plot_styles, plot_rho_u_T
from NekPlot.data import get_source
import os.path


# Add analytic data source
dsv_src = get_source("dsv", os.path.join(LOCATIONS["sol1D"],"analytic.csv") , delimiter=",", label="analytic")

# Remap column headers so that names match Nektar variables
analytic_var_name_mappings = dict(coords="x",rho="density",u="velocity",T="temperature")
dsv_src.add_var_name_mappings(analytic_var_name_mappings)

# Set series aesthetics
dsv_src.set_plot_kws(plot_styles["analytic"])


# Add Nektar source
nek_src = get_source("nektar", LOCATIONS["sol1D"], label="nektar")

# Add derived fields
nek_src.add_field('u', "rhou/rho")
nek_src.add_field('T', "(E-rhou*rhou/rho/2)/rho*(Gamma-1.0)/GasConstant")

# Set series aesthetics
nek_src.set_plot_kws(plot_styles["sol1D_pts"])


plot_rho_u_T([dsv_src, nek_src])
#plot_rho_u_T([dsv_src, nek_src],fpath=os.path.join(LOCATIONS["sol1D"],"sol-1D_rho-u-T.png"))