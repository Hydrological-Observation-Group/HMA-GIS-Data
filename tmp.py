## author: xin luo
## creat: 2024.11.27  # modify: xxxx
## des: scatter plot with color and size legend

import cartopy.crs as ccrs 
import matplotlib.pyplot as plt

def scatter_plot(x, y, size, color, ax=None, 
                 labels_size=[3, 6, 9], labels_color=[0.1, 0.4, 0.7], 
                 scale_size=1, cmap="RdYlBu", color_range=[-1, 1],
                 title_legend_color="dh/dt \n($m/yr$)",
                 title_legend_size="Glacier area\n     (${km^2}$)",
                 font_size=8,
                 loc_color="lower left", 
                 bbox_to_anchor_color=(0.01, 0.),
                 loc_size="lower left", 
                 bbox_to_anchor_size=(0.14, 0.)):
    '''
    Create a scatter plot with both color and size legends.
    
    Parameters:
        x: array-like
            x coordinates
        y: array-like
            y coordinates
        size: array-like
            size of points
        color: array-like
            color values for points
        ax: matplotlib.axes.Axes, optional
            Existing axes to plot on. If None, creates new figure
        labels_size: list of int
            labels of size legend
        labels_color: list of float
            labels of color legend
        scale_size: float
            scale factor for point sizes
        cmap: str
            colormap for color legend
        color_range: list of float
            range of color values
        title_legend_color: str
            title for color legend
        title_legend_size: str
            title for size legend
        font_size: int
            font size for legends
        loc_color: str
            location for color legend
        bbox_to_anchor_color: tuple
            bbox_to_anchor for color legend
        loc_size: str
            location for size legend
        bbox_to_anchor_size: tuple
            bbox_to_anchor for size legend
    '''
    
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    
    scatter = ax.scatter(
        x, y,
        s=size * scale_size,
        c=color,
        cmap=cmap,
        alpha=1,
        linewidth=2,
        vmin=color_range[0],
        vmax=color_range[1],
        transform=ccrs.PlateCarree(),
    )
    
    # Add color legend
    handles_color, labels_color = scatter.legend_elements(prop="colors", num=labels_color)
    legend_color = ax.legend(handles_color, labels_color, loc=loc_color, title=title_legend_color,
                             facecolor='white', edgecolor='black', borderpad=0.5,
                             labelspacing=1, markerscale=1, fontsize=font_size,
                             bbox_to_anchor=bbox_to_anchor_color)
    ax.add_artist(legend_color)
    
    # Add size legend
    handles_size, labels_size = scatter.legend_elements(prop="sizes", num=labels_size, alpha=0.6)
    legend_size = ax.legend(handles_size, [int(label * scale_size) for label in labels_size], loc=loc_size,
                            title=title_legend_size, edgecolor='black', borderpad=0.8,
                            labelspacing=1, bbox_to_anchor=bbox_to_anchor_size,
                            markerscale=1, fontsize=font_size)
    ax.add_artist(legend_size)
    
    return ax

# Example usage
if __name__ == "__main__":
    # Example data
    x = [70, 80, 90, 100]
    y = [25, 30, 35, 40]
    size = [100, 200, 300, 400]
    color = [-0.5, 0, 0.5, 1]
    
    scatter_plot(x, y, size, color)
    plt.show()