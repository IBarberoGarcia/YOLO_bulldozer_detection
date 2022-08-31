# -*- coding: utf-8 -*-
"""
Created on Mon Aug  1 09:40:08 2022

@author: Ines Barbero-García

Creates a file with:
date,hour,detection_id,conf,x_img,y_img,x,y,z
"""
import os
import sys
import numpy as np
import cv2 

def transform_2Dto3D_coord(images_folder, image, x, y, points_3D_file, crop_file):
    #First check which subimage it is
    subimage =  int(image[26])
    if crop_file !='0':
        crop_file = open(crop_file, 'r')
        crop_lines = crop_file.readlines()
        
        y_min_crop = int(crop_lines[subimage-1].split()[0])
        x_min_crop = int(crop_lines[subimage-1].split()[2])

        
    #Transform image coordinates from %(yolo) to pixels
    im = cv2.imread(images_folder + '/' + image)
    y_size, x_size, c = im.shape

    
    x_img = x_size*x
    y_img = y_size*y
    if x_img>x_size-10 or x_img<10:#If detection is in the edge that bulldozer should be detected in overlapping image
        return False
    #Transform subimages coordinates to image coordinates
    if crop_file != '0':
        print('x_min ' + str(x_min_crop))
        y_img = int(round(y_img + y_min_crop, 0))
        x_img = int(round(x_img + x_min_crop, 0))
        

    #To 3D coordinates
    points3D = np.load(points_3D_file)
    x_3d = points3D[y_img, x_img, 0]
    y_3d = points3D[y_img, x_img, 1]
    z_3d = points3D[y_img, x_img, 2]

    if x_3d == 0:#If no value in that pixel
        x = points3D[:, :, 0]
        i=2
        while i<10 and y_img-i>0 and x_img-i>0 and y_img+i<y_size and x_img+i<x_size : 
            submatrix_x = x[y_img-i:y_img+i,x_img-i:x_img+i]
            points3D = np.load(points_3D_file)
            if np.max(abs(submatrix_x))!= 0: #Any valid value in this window?
                x_3d = np.mean(submatrix_x[submatrix_x != 0])
                
                y = points3D[:, :, 1]
                submatrix_y = y[y_img-i:y_img+i,x_img-i:x_img+i]
                y_3d = np.mean(submatrix_y[submatrix_y != 0])
                
                z = points3D[:, :, 2]
                submatrix_z = z[y_img-i:y_img+i,x_img-i:x_img+i]
                z_3d = np.mean(submatrix_z[submatrix_z != 0])
                break
            i+=1
            
        
    return(x_img, y_img, x_3d, y_3d, z_3d)

def transform_2D_only(images_folder, image, x, y, crop_file):
    #First check which subimage it is
    subimage =  int(image[26])
    if crop_file !='0':
        crop_file = open(crop_file, 'r')
        crop_lines = crop_file.readlines()
        y_min_crop = int(crop_lines[subimage-1].split()[0])
        x_min_crop = int(crop_lines[subimage-1].split()[2])

        
    #Transform image coordinates from %(yolo) to pixels
    im = cv2.imread(images_folder + '/' + image)
    y_size, x_size, c = im.shape
    
    x_img = x_size*x
    y_img = y_size*y
    if x_img>x_size-10 or x_img<10:#If detection is in the edge that bulldozer should be detected in overlapping image
        return False
    #Transform subimages coordinates to image coordinates
    if crop_file !='0':
        y_img = int(round(y_img + y_min_crop, 0))
        x_img = int(round(x_img + x_min_crop, 0))
              
    return(x_img, y_img)

def create_detected_file(images_folder, detected_file, points_3D_file, crop_file):

    detected_file = open(detected_file, 'w')
    labels_folder = images_folder + 'labels/'
    
    
    image_list = os.listdir(images_folder)
    label_list = os.listdir(labels_folder)
    dict_detections = {}
    for image in image_list:
        # print(image)
        date = image[2:12]
        date = date.replace('-', '/')
        hour = image[13:21]
        hour = hour.replace('_', ':')
        if image[:-3]+'txt' in label_list:
            label_file = open(labels_folder + image[:-3]+'txt', 'r')
            label_lines = label_file.readlines()
            i=0 #To distinguish different detections in the same image
            for line in label_lines:
                line=line.split()
                x = float(line[1])
                y = float(line[2])
                if points_3D_file !='0':
                    coord = transform_2Dto3D_coord(images_folder, image, x, y, points_3D_file, crop_file)
                    if coord !=False:
                        conf = line[5]
                        detected_file.write(date + ',' + hour + ',' + str(i) + ',' + conf + ',' + str(coord) +'\n')
                else:
                    coord = transform_2D_only(images_folder, image, x,y, crop_file)
                    if coord !=False:
                        conf = line[5]
                        detected_file.write(date + ',' + hour + ',' + str(i) + ',' + conf + ',' + str(coord) +'\n')
                i+=1
    detected_file.close()


if __name__ == "__main__":
    #File path for the detections, it should be in yolov5/runs/detect
    images_folder=sys.argv[1]
    #Output path for created file
    detected_file=sys.argv[2]
    #Matrix with corresponding 3D points for each pixel in the image, can be 0 to obtain only 2D coordinates
    points_3D_file=sys.argv[3]
    #Crop file, can be 0
    crop_file=sys.argv[4]
    create_detected_file(images_folder+'/', detected_file, points_3D_file, crop_file)
    sys.exit(0)