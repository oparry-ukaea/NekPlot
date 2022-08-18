"""
Demonstrates
- reading of 1D fields (rho, rhou, E) from nektar checkpoint files
- calculation of derived fields (u from rhou,rho; T from rho,u,E)
"""
from demo_setup import LOCATIONS
from utils.plotting import plot_styles, plot_rho_u_T
from NekPlot.data import get_source

# Add a data source for each checkpoint file
data_srcs = []
for chk_num in range(0,100,20):
    nek_src = get_source("nektar", LOCATIONS["sol1D"], chk_num=chk_num, label=f"Checkpoint {chk_num}")
    nek_src.add_field('u', "rhou/rho")
    nek_src.add_field('T', "(E-rhou*rhou/rho/2)/rho*(Gamma-1.0)/GasConstant")
    nek_src.set_plot_kws(plot_styles[f"sol1D_chk{chk_num}"])
    data_srcs.append(nek_src)

# Plot fields from all sources
plot_rho_u_T(data_srcs)