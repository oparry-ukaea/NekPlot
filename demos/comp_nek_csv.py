import demo_setup
from NekPlot.data import get_source
from matplotlib import pyplot as plt
import os.path
import sys

#--------------------------------------------------------------------------------------------------
# Helper functions
def plot_rho_u_T(data_srcs):
    # Plot rho, u, T from each data source in three panels
    fig,axes = plt.subplots(nrows=1, ncols=3, figsize=(17, 5))
    prop_labels = dict(rho=r'$\rho$',u=r'$u$',T=r'$T$')
    for ii,prop in enumerate(['rho','u','T']):
        axes[ii].set_xlabel("x")
        axes[ii].set_ylabel(prop_labels[prop])
        for data_src in data_srcs:
            axes[ii].plot(data_src.get('coords'), data_src.get(prop), label=data_src.label, **data_src.get_plot_kws())

    # Add legend to all axes
    for ax in axes:
        ax.legend()

    plt.show(block=True)

def print_usage():
    print("usage:")
    print("  %s [nektar_run_paths] [nektar_session_fnames] [analytic_csv_path]" % sys.argv[0])
    print("  (where 'nektar_run_paths' and 'nektar_session_fnames' may be comma separated lists)")

    analytic_csv_path     = "/home/oparry/code/nektar-1d-sol/scripts/data/analytic.csv"
    nektar_run_paths      = ["/home/oparry/code/nektar-1d-sol/run/%s" % run for run in ["old_serial","new_mpi"]]
    nektar_session_fnames = 2*["Euler1D.xml"]
    print("  e.g.")
    print("   python %s %s %s %s" % (sys.argv[0],",".join(nektar_run_paths),",".join(nektar_session_fnames),analytic_csv_path))
#--------------------------------------------------------------------------------------------------

#==================================================================================================
def compare_nek_runs_rho_u_T(run_paths, session_fnames, plot_styles, file_bases_in=None, run_labels_in=None):
    run_labels = [os.path.basename(p) for p in run_paths] if run_labels_in is None else run_labels_in
    file_bases = [""]*len(run_paths) if file_bases_in is None else file_bases_in

    # Check arg sizes all agree
    arg_lens = [len(file_bases),len(run_paths),len(run_labels), len(plot_styles), len(session_fnames)]
    ulens = set(arg_lens)
    if len(ulens) != 1:
        exit(__name__+": argument lengths must all be the same")

    # Generate nektar sources and add new fields
    data_srcs = []
    for irun in range(arg_lens[0]):
        nsrc = get_source("nektar", run_paths[irun], session_fnames[irun], file_base=file_bases[irun], label=run_labels[irun])
        nsrc.set_plot_kws(plot_styles[irun])
        nsrc.add_field('u', "rhou/rho")
        nsrc.add_field('T', "(E-rhou*rhou/rho/2)/rho*(Gamma-1.0)/GasConstant")
        data_srcs.append(nsrc)

    plot_rho_u_T(data_srcs)
#==================================================================================================

#==================================================================================================
def compare_rho_u_T_with_analytic(nektar_run_path, nektar_session_fname, analytic_csv_path, analytic_var_name_mappings, nektar_file_base="", nektar_label_in=None):
    nektar_label = "nektar, %s" % os.path.basename(nektar_run_path) if nektar_label_in is None else nektar_label_in
    
    # Add analytic data source
    dsv_src = get_source("dsv", analytic_csv_path, delimiter=",", label="analytic")
    dsv_src.add_var_name_mappings(analytic_var_name_mappings)
    dsv_src.set_plot_kws(dict(linestyle="-", color='r'))

    # Add nektar source
    nsrc = get_source("nektar", nektar_run_path, nektar_session_fname, file_base=nektar_file_base, label=nektar_label)
    nsrc.set_plot_kws(dict(color='b', linestyle="", linewidth=0.2, marker='x', markersize=5, markeredgewidth=0.5, mec='b', mfc='b', markevery=8 ))
    nsrc.add_field('u', "rhou/rho")
    nsrc.add_field('T', "(E-rhou*rhou/rho/2)/rho*(Gamma-1.0)/GasConstant")
    
    plot_rho_u_T([dsv_src, nsrc])
#==================================================================================================

#==================================================================================================
def demo_rho_u_plots(nektar_run_paths, nektar_session_fnames, analytic_csv_path):
    # Compare a nektar run with some analytic data    
    analytic_var_name_mappings = dict(coords="x",rho="density",u="velocity",T="temperature")
    compare_rho_u_T_with_analytic(nektar_run_paths[0], nektar_session_fnames[0], analytic_csv_path, analytic_var_name_mappings)

    # Compare multiple nektar runs with each other
    plot_styles    = plot_styles=[dict(linestyle="--", color='r'),dict(linestyle=":", color='b')]
    compare_nek_runs_rho_u_T(nektar_run_paths, nektar_session_fnames, plot_styles)
#==================================================================================================


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print_usage()
    else:
        nektar_run_paths = sys.argv[1].split(",")
        nektar_session_fnames = sys.argv[2].split(",")
        analytic_csv_path = sys.argv[3]
        demo_rho_u_plots(nektar_run_paths, nektar_session_fnames, analytic_csv_path)