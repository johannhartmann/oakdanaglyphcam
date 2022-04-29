#!/usr/bin/env python3

import cv2
import numpy as np
import depthai as dai
import pyvirtualcam 
from pyvirtualcam import PixelFormat 


pipeline = dai.Pipeline()

Left = pipeline.create(dai.node.MonoCamera)
Right = pipeline.create(dai.node.MonoCamera)
stereo = pipeline.create(dai.node.StereoDepth)
xoutLeft = pipeline.create(dai.node.XLinkOut)
xoutRight = pipeline.create(dai.node.XLinkOut)
xoutRectifLeft = pipeline.create(dai.node.XLinkOut)
xoutRectifRight = pipeline.create(dai.node.XLinkOut)
xoutMerged = pipeline.create(dai.node.XLinkOut)

Left.setBoardSocket(dai.CameraBoardSocket.LEFT)
Left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)
Right.setBoardSocket(dai.CameraBoardSocket.RIGHT)
Right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_720_P)

stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
stereo.initialConfig.setMedianFilter(dai.StereoDepthProperties.MedianFilter.KERNEL_7x7)  # KERNEL_7x7 default

xoutLeft.setStreamName("left")
xoutRight.setStreamName("right")
xoutRectifLeft.setStreamName("rectifiedLeft")
xoutRectifRight.setStreamName("rectifiedRight")
xoutMerged.setStreamName("merged")

Left.out.link(stereo.left)
Right.out.link(stereo.right)
stereo.syncedLeft.link(xoutLeft.input)
stereo.syncedRight.link(xoutRight.input)
stereo.rectifiedLeft.link(xoutRectifLeft.input)
stereo.rectifiedRight.link(xoutRectifRight.input)

streams = ["left", "right", "rectifiedLeft", "rectifiedRight"]

blackImg = np.full((720,1280,1), (0), np.uint8)

camera = pyvirtualcam.Camera(1280, 720, 20, fmt=PixelFormat.BGR, print_fps=True, device='/dev/video23')

with dai.Device(pipeline) as device:
    qList = [device.getOutputQueue(stream, 8, blocking=False) for stream in streams]

    while True:
        for q in qList:
            name = q.getName()
            frame = q.get().getCvFrame()
            if name == "rectifiedLeft":
                frameleft = frame
            elif name == "rectifiedRight":
                frameright = frame
                framemerged = cv2.merge((frameright, blackImg, frameleft))
                cv2.imshow("Anaglyph View", framemerged)
                camera.send(framemerged)

        if cv2.waitKey(1) == ord("q"):
            break

cv2.destroyAllWindows()
camera.close()
