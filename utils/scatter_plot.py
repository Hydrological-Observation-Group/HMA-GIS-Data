## author: xin luo
## creat: 2024.11.27  # modify: xxxx
## des: scatter plot with color and size legend


import cartopy.crs as ccrs 
import matplotlib.pyplot as plt

def scatter_plot(x, y, size,  color, ax='None', 
                          labels_size = [3, 6, 9], labels_color = [0.1, 0.4, 0.7], 
                          scale_size = 1, cmap="RdYlBu", color_range=[-1,1],
                          title_legend_color="dh/dt \n($m/yr$)",
                          title_legend_size="Glacier area\n     (${km^2}$)",
                          font_size=8,
                          loc_color="lower left", 
                          bbox_to_anchor_color=(0.01, 0.),
                          loc_size="lower left", 
                          bbox_to_anchor_size=(0.14, 0.)):
    '''params:
            x: x coordinates
            y: y coordinates
            size: size of points
            color: color of points
            ax: axis, default is None
            labels_size: labels of size legend
            labels_color: labels of color legend
            scale_size: scale of size legend, control the size of points
            cmap: color map
            color_range: color range
            loc_color: location of color legend
            bbox_to_anchor_color: bbox_to_anchor of color legend
            loc_size: location of size legend
            bbox_to_anchor_size: bbox_to_anchor of size legend
    '''

    if ax == 'None':
        fig = plt.figure(figsize=(8,8))
        ax = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())
    scatter = ax.scatter(
            x = x,
            y = y,
            s = size*scale_size,
            c = color,
            cmap=cmap,
            alpha=1, 
            linewidth=2,
            vmin=color_range[0],
            vmax=color_range[1],
            transform=ccrs.PlateCarree(),
            )

    ## add color legend
    handles_1, labels_1 = scatter.legend_elements(prop="colors", 
                                                  num=labels_color)
    legend_color = ax.legend(handles_1, labels_1, 
                                loc=loc_color, 
                                title=title_legend_color,
                                facecolor='white', 
                                edgecolor='black',
                                borderpad=0.5, 
                                labelspacing=0.8,
                                bbox_to_anchor=bbox_to_anchor_color,  
                                markerscale=1, 
                                fontsize=font_size)
    ax.add_artist(legend_color)

    ## add size legend
    handles_2, labels_2 = scatter.legend_elements(prop="sizes", 
                                                num=[labels_size[0]*scale_size, labels_size[1]*scale_size, labels_size[2]*scale_size], 
                                                alpha=0.4)
    legend_glacier_area = ax.legend(handles_2, 
                                [labels_size[0], labels_size[1], labels_size[2]], 
                                loc=loc_size, 
                                title=title_legend_size, 
                                facecolor='white',
                                edgecolor='black', 
                                borderpad=0.5, 
                                labelspacing=0.88, 
                                bbox_to_anchor=bbox_to_anchor_size, 
                                markerscale=1, 
                                fontsize=font_size,
                                )
    for handle in legend_glacier_area.legend_handles: handle.set_markeredgecolor('none')
    ax.add_artist(legend_glacier_area)
    return ax