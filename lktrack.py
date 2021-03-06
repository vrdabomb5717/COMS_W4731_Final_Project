from functools import partial
from multiprocessing import Pool

import numpy as np
import cv2

try:
    import cv_gpu
    use_gpu = True
except ImportError:
    use_gpu = False


# From Programming Computer Vision in Python

# some constants and default parameters
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

subpix_params = dict(zeroZone=(-1, -1), winSize=(10, 10),
                     criteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 20, 0.03))

feature_params = dict(maxCorners=500, qualityLevel=0.4, minDistance=7, blockSize=7)


def hulls_from_features(tr, hulls):
    point = tr[0]
    x, y = point

    distances_gen = (cv2.pointPolygonTest(h, (x, y), True) for h in hulls)
    distances = np.fromiter(distances_gen, np.float, count=len(hulls))

    max_hull_index = np.argmax(distances)
    return max_hull_index


def test_in_hull(h, x, y):
    return cv2.pointPolygonTest(h, (x, y), True)


class LKTracker(object):
    """Class for Lucas-Kanade tracking with
        pyramidal optical flow."""

    def __init__(self, image):
        """Initialize parameters, and store the first image. """

        self.image = image
        self.features = []
        self.tracks = []
        self.track_len = 10
        self.current_frame = 0
        self.interval = 5
        self.mser = cv2.MSER()
        self.cvh = cv_gpu.GPU() if use_gpu else cv2
        self.pool = Pool()

    def step(self, next_image):
        """Step to another frame."""

        self.current_frame += 1
        self.image = next_image

    def detect_points(self):
        """Detect 'good features to track' (corners) in the current frame
            using sub-pixel accuracy. """

        # load the image and create grayscale
        self.gray = self.cvh.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # search for good points
        features = self.cvh.goodFeaturesToTrack(self.gray, **feature_params)

        # refine the corner locations
        cv2.cornerSubPix(self.gray, features, **subpix_params)

        self.features = features
        self.tracks = [[p] for p in features.reshape((-1, 2))]

        self.prev_gray = self.gray

    def track_points(self):
        """Track the detected features."""

        if self.features != []:
            # use the newly loaded image and create grayscale
            self.gray = self.cvh.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            # reshape to fit input format
            tmp = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)

            # calculate optical flow using forwards-backwards algorithm
            features, status, track_error = cv2.calcOpticalFlowPyrLK(self.prev_gray,
                                                                     self.gray, tmp,
                                                                     None, **lk_params)

            features_r, status1, track_error = cv2.calcOpticalFlowPyrLK(self.gray,
                                                                        self.prev_gray,
                                                                        features, None,
                                                                        **lk_params)

            d = abs(tmp - features_r).reshape(-1, 2).max(-1)
            good = d < 1
            new_tracks = []

            for tr, (x, y), good_flag in zip(self.tracks, features.reshape(-1, 2), good):
                if not good_flag:
                    continue
                tr.append((x, y))
                if len(tr) > self.track_len:
                    del tr[0]
                new_tracks.append(tr)

                cv2.circle(self.image, (x, y), 2, (0, 255, 0), -1)

            self.tracks = new_tracks
            cv2.polylines(self.image, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))

        # replenish lost points every self.interval steps
        if self.current_frame % self.interval == 0:
            mask = np.zeros_like(self.gray)
            mask[:] = 255
            for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                cv2.circle(mask, (x, y), 5, 0, -1)
            p = self.cvh.goodFeaturesToTrack(self.gray, mask=mask, **feature_params)

            # Refine the features using cornerSubPix.
            # Takes time to compute, and makes the video choppy, so only enable if you need it.
            cv2.cornerSubPix(self.gray, p, **subpix_params)

            if p is not None:
                for x, y in np.float32(p).reshape(-1, 2):
                    self.tracks.append([(x, y)])

        self.prev_gray = self.gray

    def track(self):
        """Generator for stepping through a sequence."""

        if self.features == []:
            self.detect_points()
        else:
            self.track_points()

        # create a copy in RGB
        f = np.array(self.features).reshape(-1, 2)
        im = self.cvh.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        yield im, f

    def draw(self):
        """Draw the current image with points using
            OpenCV's own drawing functions."""

        mask = np.zeros_like(self.gray)
        mask[:] = 255
        for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
            cv2.circle(mask, (x, y), 5, 0, -1)

        # do blob detection
        regions = self.mser.detect(self.gray, mask=mask)
        hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
        hull_test = partial(hulls_from_features, hulls=hulls)
        hulls1 = self.pool.map(hull_test, self.tracks)
        hulls1 = [hulls[i] for i in hulls1]

        # for tr in self.tracks:
        #     point = tr[0]
        #     x, y = point
        #     # hull_test = partial(test_in_hull, x=x, y=y)
        #     # distances = self.pool.map(hull_test, hulls, chunksize=20)
        #     # distances = np.float64(distances)

        #     distances_gen = (cv2.pointPolygonTest(h, (x, y), True) for h in hulls)
        #     distances = np.fromiter(distances_gen, np.float)

        #     max_hull_index = np.argmax(distances)
        #     max_hull = hulls[max_hull_index]
        #     hulls1.append(max_hull)
        cv2.polylines(self.image, hulls1, 1, (0, 255, 255))

        return self.image
