# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 11:01:23 2022

@author: Ines Barbero-García

Crops and computes changes using PCA
"""

import sys
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from cv2 import imread
from sklearn.decomposition import PCA
import shutil

def crop_and_get_change(path_in, path_out_change, crop_file):
    if crop_file != '0': #Crop_file 0 in case no cropping required
        crop_file = open(crop_file, 'r')
        crop_file_lines = crop_file.readlines()
        num_subimages=len(crop_file_lines)
    else:
        num_subimages=1
    
    if not os.path.exists(path_out_change) :
        os.mkdir(path_out_change)
        
    folder_list = os.listdir(path_in)
    for folder in folder_list:
        print('folder ' + folder)
        image_list = os.listdir(path_in + folder)
        
        path_out=path_in + folder + '/processed/'  
        if  os.path.exists(path_out):
            shutil.rmtree(path_out)
        
        os.mkdir(path_out)
        
    
        for file in image_list:
            if file.endswith('cal.jpg'):
          
                print('cropping ' + file)
                #In case the path_out does not exist create
                
                
                img=cv2.imread(path_in + folder + '/' + file, cv2.COLOR_BGR2RGB)
                img=img[:,:, ::-1]#Real RGB colors
                
                if crop_file != '0':
                    i=0
                    for line in crop_file_lines:#Each line gives a subimage: y_min, y_max, x_min, x_max  
                        line = line.split()
                        img_band = img[int(line[0]):int(line[1])]
                        plt.imsave(path_out + file[:-4] + '_' + str(i+1) +'c.jpg', img_band[:,int(line[2]):int(line[3])])
                        i+=1
                else:
                    plt.imsave(path_out + file[:-4] + '_1c.jpg', img)
                    
                    
                    
                                
        '''Compute PCA changes'''
        i=0
        while i < num_subimages: #For each subimage created by cropping
            print('PCA for subimage ' + str(i+1))    
            list_images=[]
            for file in os.listdir(path_out):
                if file.endswith(str(i+1) + "c.jpg"):
                    list_images.append(file)
                                   
            j=0
            for file in list_images:
                bulldozer_img = imread(path_out + file,0).flatten()
                #Get 15 images to compute PCA
                if len(list_images)<=15:
                    selected_images=list_images
                else:
                    selected_images=list_images[j:j+15]
    
                j+=1
                #Compute PCA with selected images
            
                comb_img=[]
                for selected_file in selected_images:
                    img=imread(path_out + selected_file,0)
                    img_flat=img.flatten()
                
                    comb_img.append(img_flat)
                        
                pca = PCA(1) # we need only 1 principal component.

                pca1 = pca.fit_transform(np.transpose(comb_img))[:,0]
            
                pca1 = (pca1 - np.min(pca1))
                pca1 = pca1/(np.max(pca1)/255)
                #Image values can be inverted, so get the "version" that is more similar to original
                if np.std(img_flat-pca1) > np.std(img_flat+pca1):
                    pca1=255-pca1    
                
                pca1_change = (bulldozer_img - pca1).reshape(len(img), len(img[0]))
    
                plt.imsave(path_out_change + file[:-4] + '_change.jpg', pca1_change, cmap='gray')
            i+=1

if __name__ == "__main__":
    #File path were the folders for different days or time frames are located
    path_in=sys.argv[1]
    #Output path for change images
    path_out=sys.argv[2]
    #Crop file, can be 0 if no cropping required
    crop_file=sys.argv[3]
    crop_and_get_change(path_in +'/', path_out +'/', crop_file)
    sys.exit(0)