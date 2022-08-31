# Change detection and YOLO for automatic characterization of anthropogenic changes in a sandy beach

This repository contains the code described in the paper "Change detection and YOLO for automatic characterization of anthropogenic changes in a sandy beach"
It contains
- The code for image preprocessing (cropping, image correction, change detection)
- The code for bulldozer detection on change images, including the pretrained weights
- The code for obtaining coordinates for the detected bulldozers
- The training dataset
- A demo dataset for testing

The code included here can be applied to a dataset of images previously, no code is providing for extraction of the required frames from video, as each dataset 
will be structured in a different way

## The structure of the image dataset

The structure of the data should be the same as for the provided demo dataset.

- Each folder must contain a continuous set of images. If there is a gap with no data (e.g. night hours) two folders should be made.
- The image names should follow the same structured as the images in the demo dataset, including date and time of acquisition.

The process is optimized to work with a time between images of 2.5 minutes, however, images with other frequencies can be used.

## Creation of change images

crop_and_pca.py

Crops the images, creates the change images and saves them to an output file.

INPUTS: path to images folder, output path, path to crop file.

Path to crop file can be '0' if no cropping is required.
The format of the croping file is Y_min, Y_max, X_min, X_max, a subimage will be created for 
each line in the document. An example of the document can be found in demo_dataset/crop_file.txt.
It is recommended to maintain an overlap of 20 pixels while cropping.

Example for demo dataset:

`python crop_and_pca.py demo_dataset/images demo_dataset/change demo_dataset/crop_file.txt`

## Detection

The pretrained model for the bulldozer detection is located in model/bulldozer.pt

YOLOv5 can be downloaded from https://github.com/ultralytics/yolov5

For the following processes it is required to save the labels in txt.

Example for the demo dataset:

`python detect.py --weights models/bulldozer.pt --img 320 --conf 0.2 --source demo_dataset/changes --save-txt --save-conf`

## Create file with the list of detected bulldozers

created_detected_file.py

INPUTS: 
- Path to detection results, should be yolov5/runs/detect/expX
- Path to save resulting file
- Matrix where each pixel in the image is linked to the 3D coordinates, in npy format, can be zero if we do not want to compute 3D coordinates 
(only image coordinates will be stored)
- Path to crop_file, same as for the crop_and_change function. Should be 0 if no cropping was done in previous steps.

Example for demo dataset:

`python create_detected_file.py yolov5\runs\detect\exp3 demo_dataset\detected.txt demo_dataset\3d_points_matrix.npy demo_dataset/crop_file.txt`

The resulting file will be structured as:
date, hour, id of detection for that image, YOLO confidence, coordinates

Coordinates will correspond to x_img, y_img, x_3D, y_3D, z_3D.

## Filtering

filter_detected.py

INPUT: inputfile, output_file, mask

Example for demo dataset:

`python filter_detected.py demo_dataset\detected.txt detected_filtered.txt demo_dataset\mask.jpg`


## Training dataset

Two training dataset can be found in https://drive.google.com/file/d/15ZjoaxWw2K5V4PEori5PXW4IlwyyhfPk/view?usp=sharing. The file contains one folder for the original RGB images and one for the change images.

