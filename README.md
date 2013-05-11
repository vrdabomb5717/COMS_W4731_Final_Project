Title: COMS W4731 Final Project    
Author: Varun Ravishankar    
        Dan Mercado     
Email:  vr2263@columbia.edu    
       dm2497@columbia.edu   
Date: May 11th, 2013     

# Tracking Suspicious Behavior in Videos in Real Time
## COMS W4731 Final Project

This program tracks suspicious behavior in videos in real time.

### Dependencies

This program was tested on OS X 10.8.3 and Ubuntu 12.04 LTS using Python 2.7. The program may run on older versions of Python; however, these are untested and unsupported.

Dependency versions that have been tested are listed here. Older versions of Python modules such as numpy or OpenCV may work as well; however, these are untested and unsupported.

* Python 2.7 or greater
* numpy 1.7.1
* OpenCV 2.4.5.0 or greater
* ffmpeg support [optional]
* Nvidia GPU with CUDA support [optional]
* gcc [optional]
* Boost.Python [optional]

The optional dependencies allow for GPU support, but you must build the provided GPU module first. You must also enable GPU support in your OpenCV build.

### Usage

First, clone the repository and add it to your ```PYTHONPATH```. Then, copy the path to a video you would like to analyze and pass it as an argument to ```read_video.py```.

Next, you can run the Python scripts.

See an example below that starts off in the cloned repo:

```
$ pip install -r requirements.txt
$ make
$ python -O read_video.py data/video.mp4
```
