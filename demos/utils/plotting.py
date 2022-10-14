from matplotlib import pyplot as plt
import numpy as np

# define some sets of plot keywords
plot_styles = {}
plot_styles["analytic"]     = dict(linestyle="-", color='r')
plot_styles["convection2D"] = dict()
plot_styles["sol1D_pts"]    = dict(color='b', linestyle="", linewidth=0.2, marker='x', markersize=5, markeredgewidth=0.5, mec='b', mfc='b', markevery=8 )

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
            axes[ii].plot(data_src.get('x'), data_src.get(prop), label=data_src.label, **data_src.get_plot_kws())

    # Add legend to all axes
    for ax in axes:
        ax.legend()

    if fpath is None:
        plt.show(block=True)
    else:
        plt.savefig(fpath)
#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------
def plot_u_field(data_src,mode='img',log=False):
    fwidth = 1.5 if mode=='img' else 9
    fig,axes = plt.subplots(nrows=1, ncols=1, figsize=(fwidth, 7.5))
    
    axes.set_xlabel("x")
    axes.set_ylabel("y")

    x = data_src.get('x')
    y = data_src.get('y')
    u1D = data_src.get('u')

    if mode == 'img':
        # Regular spaced coords vary a bit after 12th decimal point; round them to get unique values:
        xb = sorted(set(np.round(x,decimals=12)))
        yb = sorted(set(np.round(y,decimals=12)))
        xindices = np.digitize(x,xb)-1
        yindices = np.digitize(y,yb)-1

        u = np.ones((len(xb),len(yb)))
        for i1D,(ix,iy) in enumerate(zip(xindices,yindices)):
            u[ix,iy] = u1D[i1D]

        if log:
            #u[u<0]=1e-6
            u = np.log10(u+1)

        plt.imshow(u,interpolation='none', extent=[min(xb),max(xb),min(yb),max(yb)],aspect=0.2,vmax=np.percentile(u,98))
    elif mode=='scatter':
        axes.scatter(x, y, c=u1D, label=data_src.label, **data_src.get_plot_kws())
    else:
        raise ValueError(f"plot_u_field: {mode} is not a valid mode string")
    plt.show(block=True)
#--------------------------------------------------------------------------------------------------