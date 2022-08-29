# Change detection and YOLO for automatic characterization of anthropogenic changes in a sandy beach
IN PROCESS

This repository contains the code described in the paper "Change detection and YOLO for automatic characterization of anthropogenic changes in a sandy beach"
It contains
- The code for image preprocessing (cropping, image correction, change detection)
- The code for bulldozer detection on change images, including the pretrained weights
- The code for obtaning coordinates for the detected bulldozers
- The training dataset
- A demo dataset for testing

The code included here can be applied to a dataset of images previously, no code is providing for extraction of the required frames from video, as each dataset 
will be structured in a different way

python crop_and_pca.py \demo_dataset/images \demo_dataset/change \demo_dataset/crop_file.txt
