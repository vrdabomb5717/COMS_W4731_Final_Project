from numpy import *
import cv2

# From Programming Computer Vision in Python

# some constants and default parameters
lk_params = dict(winSize=(15, 15), maxLevel=2,
                criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

subpix_params = dict(zeroZone=(-1, -1), winSize=(10, 10),
                     criteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 20, 0.03))

feature_params = dict(maxCorners=500, qualityLevel=0.01, minDistance=10)


class LKTracker(object):
    """Class for Lucas-Kanade tracking with
        pyramidal optical flow."""

    def __init__(self, image):
        """Initialize parameters, and store the first image. """

        self.image = image
        self.features = []
        self.tracks = []
        self.current_frame = 0

    def step(self, next_image):
        """Step to another frame."""

        self.current_frame += 1
        self.image = next_image

    def detect_points(self):
        """Detect 'good features to track' (corners) in the current frame
            using sub-pixel accuracy. """

        # load the image and create grayscale
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # search for good points
        features = cv2.goodFeaturesToTrack(self.gray, **feature_params)

        # refine the corner locations
        cv2.cornerSubPix(self.gray, features, **subpix_params)

        self.features = features
        self.tracks = [[p] for p in features.reshape((-1, 2))]

        self.prev_gray = self.gray

    def track_points(self):
        """Track the detected features. """

        if self.features != []:
            # use the newly loaded image and create grayscale
            self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            # reshape to fit input format
            tmp = float32(self.features).reshape(-1, 1, 2)

            # calculate optical flow
            features, status, track_error = cv2.calcOpticalFlowPyrLK(self.prev_gray,
                                                                     self.gray, tmp,
                                                                     None, **lk_params)

            # remove points lost
            self.features = [p for (st, p) in zip(status, features) if st]

            # clean tracks from lost points
            features = array(features).reshape((-1, 2))
            for i, f in enumerate(features):
                self.tracks[i].append(f)
            ndx = [i for (i, st) in enumerate(status) if not st]
            ndx.reverse()  # remove from back
            for i in ndx:
                self.tracks.pop(i)

            self.prev_gray = self.gray

    def track(self):
        """Generator for stepping through a sequence."""

        if self.features == []:
            self.detect_points()
        else:
            self.track_points()

        # create a copy in RGB
        f = array(self.features).reshape(-1, 2)
        im = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        yield im, f

    def draw(self):
        """Draw the current image with points using
            OpenCV's own drawing functions.
            Press ant key to close window."""

        # draw points as green circles
        for point in self.features:
            cv2.circle(self.image, (int(point[0][0]), int(point[0][1])), 3, (0, 255, 0), -1)

        return self.image
        # cv2.imshow('LKtrack', self.image)
