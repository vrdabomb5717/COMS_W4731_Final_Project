#!/usr/bin/env python

import pdb
import cv2


def main():
    cap = cv2.VideoCapture("./data/video.mp4")

    while True:
        ret, im = cap.read()
        # blur = cv2.GaussianBlur(im, (0, 0), 5)
        cv2.imshow('video test', im)
        key = cv2.waitKey(10)
        if key == 27:
            break


if __name__ == '__main__':
    main()
