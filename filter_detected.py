# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 08:47:05 2022

@author: Innes
"""

import os
from datetime import datetime
from matplotlib import image

import sys



def filter_detected(in_file, out_file, mask_file):


    '''Detections per day'''
    detections = open(in_file, 'r')
    output_file = open(out_file, 'w')
    mask = image.imread(mask_file)
    
    detections_lines = detections.readlines()
    detections_list = []
    for line in detections_lines:
        line=line.split(',')
        detections_list.append(line)
    i=0
    
    while i<len(detections_list)-1:
        detection = detections_list[i]
        previous = detections_list[i-1]
        posterior = detections_list[i+1]
        
        #Check if previous and posterior acquisition have more than one hour difference
        detection_time = datetime(int(detection[0].split('/')[0]), int(detection[0].split('/')[1]), int(detection[0].split('/')[2]), int(detection[1].split(':')[0]), int(detection[1].split(':')[1]), int(detection[1].split(':')[2]))
        previous_time = datetime(int(previous[0].split('/')[0]), int(previous[0].split('/')[1]), int(previous[0].split('/')[2]), int(previous[1].split(':')[0]), int(previous[1].split(':')[1]), int(previous[1].split(':')[2]))
        posterior_time = datetime(int(posterior[0].split('/')[0]), int(posterior[0].split('/')[1]), int(posterior[0].split('/')[2]), int(posterior[1].split(':')[0]), int(posterior[1].split(':')[1]), int(posterior[1].split(':')[2]))
        
        x = int(detection[4].replace('(', ''))
        y = int(detection[5].replace(')\n', ''))
        
        #Check if 3 previous acquisitions are too close coordinates
        j=1
        repeated=False
        while j<4:
            detection = detections_list[i]
            previous = detections_list[i-j]
            
            x_pre = int(previous[4].replace('(', ''))
            y_pre = int(previous[5].replace(')\n', ''))
    
            distance = ((x-x_pre)**2+(y-y_pre)**2)**0.5
            if distance < 5: 
                repeated=True
                break
            j+=1
            
        #Check detection is in not masked area
        
        if mask[y][x][0]==255:
            if (((detection_time - previous_time).total_seconds()/3600)<1 or ((posterior_time - detection_time).total_seconds()/3600)<1) and not repeated:
                #Minimum confidence filter
                if float(detection[3])>0.2:
                    output_file.write(detections_lines[i])
    
        i+=1
        
    output_file.close()
    
if __name__ == "__main__":
    #File path for the detections, it should be in yolov5/runs/detect
    detected_file = sys.argv[1]
    out_file = sys.argv[2]
    mask_file = sys.argv[3]
    filter_detected(detected_file, out_file, mask_file)
