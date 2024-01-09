# Installation
## Install miniconda
## Create conda environment
```
conda create --name <yourenvironmentname> python==3.11
```
## Activate environment
```
conda activate <yourenvironmentname>
```
## Install requirements
### Install from requirements.txt
```
conda install --file requirements.txt
```
### or install the following packages manually
```
conda install jsonschema
pip install opencv-python
conda install click
```

# Running
## Introduction
This is a simple command line tool originally developed for masking out land from satellite RGB video files. The methodology used is a simple frame-by-frame processing procedure utilizing openCV. The pixels are masked with the application of an HSV filter. The user can define the HSV filter parameters along with some optional preprocessing operators such as Gaussial Blur, CLAHE equalization, as well as mask cleanup operators (hole and object removal). These parameters can be decided by the user through an input JSON file.
To fine-tune the masking parameters, the user can execute the tool in "guimode". Executing in "guimode" will launch four different windows: one window looping the original video, one window looping the video after frame preprocessing, one window looping the masked video after the application of the hsv filter, one window with trackbars of the HSV parameters. The user can adjust and test his prefered HSV parameters, the results will be displayed in the video windows in real-time. Once the user quits Guimode (default "q" keyboard shortcut), the tool will exit after saving a JSON file with the current HSV filter parameters to the input video parent directory.
The user can then mask the video by executing the tool again and passing the produced JSON into the -hsv variable.
If a JSON file with HSV parameters is provided and no Output folder is provided (-o), the masking tool will automatically save the masked video in the input video parent directory, appending "_masked" to the output file name.
The tool assumes the input video is an 8bit rgb video.

## Sample Run
Runs from conda command line:
1. get info on all arguements
```
python main.py --help
```
2. sample run
```
python main.py -i "<input video directory>" -guimode
python main.py -i "<input video directory>" -hsv "<Json directory>"

```
## Additional parameters
| Arguement full name | Arguement | type      | description                                  |
| ----------- | ------------ | --------- | -------------------------------------------- |
| --inputfile| `-i`           | DIRECTORY | Input video directory             |
| --outputfolder| `-o`           | DIRECTORY | Output folder to store masked video                                  |
| --hsv| `-r`           | DIRECTORY | Input JSON directory containing HSV filter parameters. Expected format: {"hMin": 0, "sMin": 0, "vMin": 0, "hMax": 179, "sMax": 255, "vMax": 255, "sAdd": 0, "sSub": 0, "vAdd": 0, "vSub": 0, "blur": 0, "close": 0, "object": 0, "hole": 0}. Filter parameters and value ranges: MinHue (0 to 179), MinSaturation (0 to 255), MinValue (0 to 255), MaxHue (0 to 179), MaxSaturation (0 to 255), MaxValue (0 to 255), SaturationAdd (0 to 255), SaturationSubtract (0 to 255), ValueAdd (0 to 255), ValueSubtract (0 to 255), Clahe (0 or 1, switch on CLAHE application per frame before masking), Blur (0 to 10, increases kernel size), Close (0 to 10, increases kernel size), Small Object Removal (0 to 25000 in pixels), Small Hole Removal (0 to 25000 in pixels)                   |
| --guimode| `-guimode/-no-guimode`     | BOOLEAN| Feature detection alg.[sift,orb,brisk,akaze] |
