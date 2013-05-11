#!/usr/bin/env python

from __future__ import division

from timeit import time
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


def draw_str(dst, (x, y), s):
    cv2.putText(dst, s, (x + 1, y + 1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=2, lineType=cv2.CV_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.CV_AA)


def main():
    frames = video_by_frame("./data/video.mp4")
    tracking_frames = track_video(frames)
    start_time = time.time()

    for im in tracking_frames:
        stop_time = time.time()
        time_elapsed = 1 / (stop_time - start_time)
        draw_str(im, (20, 20), 'FPS: %.2f' % time_elapsed)
        start_time = stop_time

        cv2.imshow('LKtrack', im)
        key = cv2.waitKey(40)
        if key == 27 or key == ord('q') or key == ord('Q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
