#!/usr/bin/env python

import pdb
import cv2
import lktrack


def video_by_frame(video):
    """Read a video frame by frame."""
    cap = cv2.VideoCapture(video)

    while True:
        ret, im = cap.read()
        yield im


def track_video(frames):
    """Create a generator around the Lucas-Kanade optical flow class."""
    first_frame = next(frames)
    lkt = lktrack.LKTracker(first_frame)
    lkt.detect_points()
    yield lkt.draw()

    for im in frames:
        lkt.step(im)
        lkt.track_points()
        yield lkt.draw()


def main():
    frames = video_by_frame("./data/video.mp4")
    tracking_frames = track_video(frames)

    for im in tracking_frames:
        cv2.imshow('LKtrack', im)
        key = cv2.waitKey(10)
        if key == 27:
            break


if __name__ == '__main__':
    main()
