# Change detection and YOLO for automatic characterization of anthropogenic changes in a sandy beach
IN PROCESS

This repository contains the code described in the paper "Change detection and YOLO for automatic characterization of anthropogenic changes in a sandy beach"
It contains
- The code for image preprocessing (cropping, image correction, change detection)
- The code for bulldozer detection on change images, including the pretrained weights
- The code for obtaining coordinates for the detected bulldozers
- The training dataset
- A demo dataset for testing

The code included here can be applied to a dataset of images previously, no code is providing for extraction of the required frames from video, as each dataset 
will be structured in a different way

## Creation of change images

crop_and_pca.py

Crops the images, creates the change images and saves them to an output file.

INPUTS: path to images folder, output path, path to crop file.

Path to crop file can be '0' if no cropping is required.
The format of the croping file is Y_min, Y_max, X_min, X_max, a subimage will be created for 
each line in the document. An example of the document can be found in demo_dataset/crop_file.txt.

Example for demo dataset:

`python crop_and_pca.py demo_dataset/images demo_dataset/change demo_dataset/crop_file.txt`

## Detection

The pretrained model for the bulldozer detection is located in model/bulldozer.pt

YOLOv5 can be downloaded from https://github.com/ultralytics/yolov5

For the following processes it is required to save the labels in txt.

Example for the demo dataset:

`python detect.py --weights models/bulldozer.pt --img 320 --conf 0.2 --source demo_dataset/changes --save-txt --save-conf`

##Create a file with a list of detected bulldozers


