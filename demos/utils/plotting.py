from matplotlib import pyplot as plt

# define some sets of plot keywords
plot_styles = {}
plot_styles["analytic"]  = dict(linestyle="-", color='r')
plot_styles["sol1D_pts"] = dict(color='b', linestyle="", linewidth=0.2, marker='x', markersize=5, markeredgewidth=0.5, mec='b', mfc='b', markevery=8 )

for chk_num,color,lsty in zip(range(0,100,20),"rbgcm",["-", ":", "-.", ":","--"]):
    plot_styles[f"sol1D_chk{chk_num}"] = dict(color=color,linestyle=lsty)

#--------------------------------------------------------------------------------------------------
# Helper functions
def plot_rho_u_T(data_srcs,fpath=None):
    # Plot rho, u, T from each data source in three panels
    fig,axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 5))
    plt.subplots_adjust(left=0.05,right=0.95,top=0.95)
    prop_labels = dict(rho=r'$\rho$',u=r'$u$',T=r'$T$')
    for ii,prop in enumerate(['rho','u','T']):
        axes[ii].set_xlabel("s",fontsize=16)
        axes[ii].set_ylabel(prop_labels[prop],fontsize=15)
        axes[ii].tick_params(labelsize=12)
        for data_src in data_srcs:
            axes[ii].plot(data_src.get('coords'), data_src.get(prop), label=data_src.label, **data_src.get_plot_kws())

    # Add legend to all axes
    for ax in axes:
        ax.legend()

    if fpath is None:
        plt.show(block=True)
    else:
        plt.savefig(fpath)
#--------------------------------------------------------------------------------------------------
