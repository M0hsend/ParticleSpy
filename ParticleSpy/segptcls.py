# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 15:06:08 2018

@author: qzo13262
"""

import numpy as np
import scipy.ndimage as ndi

from skimage.filters import threshold_otsu, threshold_mean, threshold_minimum
from skimage.filters import threshold_yen, threshold_isodata, threshold_li
from skimage.filters import threshold_local

from skimage.measure import label, regionprops
from skimage.morphology import remove_small_objects, watershed
from skimage.segmentation import clear_border, mark_boundaries
from skimage.feature import peak_local_max

def process(im, process_param):
    
    if isinstance(im,(list,)):
        data = im[0].data
    else:
        data = im.data
        
    if process_param["threshold"]!=None:
        labels = threshold(data, process_param)
        
    labels = clear_border(labels)
    
    if process_param["watershed"]!=None:
        labels = p_watershed(labels)
        
    if process_param["min_size"]!=None:
        remove_small_objects(labels,process_param["min_size"],in_place=True)
            
    return(labels)
    
def threshold(data, process_param):
    
    if process_param["threshold"] == "otsu":
        thresh = threshold_otsu(data)
    if process_param["threshold"] == "mean":
        thresh = threshold_mean(data)
    if process_param["threshold"] == "minimum":
        thresh = threshold_minimum(data)
    if process_param["threshold"] == "yen":
        thresh = threshold_yen(data)
    if process_param["threshold"] == "isodata":
        thresh = threshold_isodata(data)
    if process_param["threshold"] == "li":
        thresh = threshold_li(data)
    if process_param["threshold"] == "local":
        thresh = threshold_local(data,21)
            
    mask = data > thresh
    
    labels = label(mask)
    
    return(labels)
    
def p_watershed(thresh_image):
    distance = ndi.distance_transform_edt(thresh_image)
    local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)),
                            labels=thresh_image)
    markers = ndi.label(local_maxi)[0]
    labels = watershed(-distance, markers, mask=thresh_image)
    return(labels)