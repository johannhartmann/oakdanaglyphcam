# Oak-D Anaglyph Camera

This short script allows you to use your oak-d camera for 3D videoconferencing. 
Ok, it's the 3D of the 50ies, using anaglyph glasses. However, it's still fun. 
Currently it's working on linux only, feel free to add support for other platforms. 


# INSTALL
First install v4l2loopback. On Ubuntu this would look like
```sh
sudo apt install v4l2loopback-dkms
sudo modprobe v4l2loopback devices=1
```
Please create a video device that can be used. 
```sh
sudo modprobe -r v4l2loopback && sudo modprobe v4l2loopback devices=1 video_nr=23 card_label="Anaglyph camera" exclusive_caps=1 max_buffers=2
```
Please not that the parameter **exclusive_caps=1** is needed to support the camera in google chrome.

Install python dependencies: 
```sh
pip3 install -r requirements.txt 
```
And, finally, run the code: 
```sh 
python anaglyphcam.py
```
