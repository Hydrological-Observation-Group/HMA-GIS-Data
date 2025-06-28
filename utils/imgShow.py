## author: xin luo
## create: 2020, modify: 2025.6.18
## des: remote sensing image visualization

import matplotlib.pyplot as plt
import numpy as np


def imgShow(img, ax=None, extent=None, color_bands=(2,1,0), clip_percent=2, per_band_clip=False):
    '''
    Description: show the single image.
    args:
        img: (row, col, band) or (row, col), DN range should be in [0,1]
        ax: axes for showing image.
        extent: list, the coordinates of the extent. 
        num_bands: a list/tuple, [red_band,green_band,blue_band]
        clip_percent: for linear strech, value within the range of 0-100. 
        per_band_clip: if True, the band values will be clipped by each band respectively. 
    return: None
    '''
    img = img.copy()
    img[np.isnan(img)]=0   ## remove NaN values 
    img = np.squeeze(img)

    if np.min(img) == np.max(img):
        if len(img.shape) == 2:
            if ax: ax.imshow(np.clip(img, 0, 1), extent=extent, vmin=0,vmax=1)
            else: plt.imshow(np.clip(img, 0, 1), extent=extent, vmin=0,vmax=1)
        else:
            if ax: ax.imshow(np.clip(img[:,:,0], 0, 1), extent=extent, vmin=0, vmax=1)
            else: plt.imshow(np.clip(img[:,:,0], 0, 1), extent=extent, vmin=0, vmax=1)
    else:
        if len(img.shape) == 2:
            img_color = np.expand_dims(img, axis=2)
        else:
            img_color = img[:,:,[color_bands[0], color_bands[1], color_bands[2]]]    
        img_color_clip = np.zeros_like(img_color)
        if per_band_clip == True:
            for i in range(img_color.shape[-1]):
                if clip_percent == 0:
                    img_color_hist = [0,1]
                else:
                    img_color_hist = np.percentile(img_color[:,:,i], [clip_percent, 100-clip_percent])
                img_color_clip[:,:,i] = (img_color[:,:,i]-img_color_hist[0])\
                                    /(img_color_hist[1]-img_color_hist[0]+0.0001)
        else:
            if clip_percent == 0:
                    img_color_hist = [0,1]
            else:
                img_color_hist = np.percentile(img_color, [clip_percent, 100-clip_percent])
            img_color_clip = (img_color-img_color_hist[0])\
                                     /(img_color_hist[1]-img_color_hist[0]+0.0001)

        if ax: ax.imshow(np.clip(img_color_clip, 0, 1), extent=extent, vmin=0, vmax=1)
        else: plt.imshow(np.clip(img_color_clip, 0, 1), extent=extent, vmin=0, vmax=1)


def imsShow(img_list, img_name_list, clip_list=None, figsize=(8,4),\
                            color_bands_list=None, axis=True, row=None, col=None):
    ''' 
    des: visualize multiple images.
        input: 
            img_list: containes all images
            img_names_list: image names corresponding to the images
            clip_list: percent clips (histogram) corresponding to the images
            color_bands_list: color bands combination corresponding to the images
            row, col: the row and col of the figure
            axis: True or False
        return: None
    '''
    if not clip_list:
        clip_list = [2 for i in range(len(img_list))]
    if not color_bands_list:
        color_bands_list = [[2, 1, 0] for i in range(len(img_list))]
    if row == None:
        row = 1
    if col == None:
        col = len(img_list)
    fig, ax = plt.subplots(row, col, figsize=figsize)
    for i in range(row):
        for j in range(col):
            ind = (i*col)+j
            if ind == len(img_list):
                break
            imgShow(img=img_list[ind], ax=ax[ind], 
                        color_bands=color_bands_list[ind], clip_percent=clip_list[ind])        
            ax[ind].set_title(img_name_list[ind])
            if not axis: ax[ind].set_axis_off()
    plt.show()
                                