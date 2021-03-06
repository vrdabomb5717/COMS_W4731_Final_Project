import numpy as np
import cv2
import pdb
import math

# From Programming Computer Vision in Python

# some constants and default parameters
lk_params = dict(winSize=(15, 15), maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

subpix_params = dict(zeroZone=(-1, -1), winSize=(10, 10),
                     criteria = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 20, 0.03))

feature_params = dict(maxCorners=500, qualityLevel=0.4, minDistance=7, blockSize=7)


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
        """Track the detected features."""

        if self.features != []:
            # use the newly loaded image and create grayscale
            self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            # reshape to fit input format
            # tmp = np.float32(self.features).reshape(-1, 1, 2)
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
            p = cv2.goodFeaturesToTrack(self.gray, mask=mask, **feature_params)

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
        im = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
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

        #for h in hulls:
        #    for tr in self.tracks:
        #        point = tr[0]
        #        if cv2.pointPolygonTest(h, (point[0], point[1]), False) > 0:
        #            hulls1.append(h)
        #            break
        if self.current_frame > 450:
            mu = [cv2.moments(h, 0) for h in hulls]

            mc = [[mu[i]["m10"] / mu[i]["m00"] , mu[i]["m01"] / mu[i]["m00"]] for i, h in enumerate(hulls)]
            #  ///  Get the mass centers:
            #  vector<Point2f> mc( contours.size() );
            #  for( int i = 0; i < contours.size(); i++ )
            #     { mc[i] = Point2f( mu[i].m10/mu[i].m00 , mu[i].m01/mu[i].m00 ); }
            #hulls2 = []
            def get_min_hull(tr):
	            minimum = float('inf')
	            index = None
	            for i, center in enumerate(mc):
		            current_min = np.linalg.norm(tr - np.array(center))
		            if current_min < minimum:
			            #pdb.set_trace()				
			            minimum = current_min
			            index = i
	            return hulls[index]

            hulls1 = [get_min_hull(tr) for tr in self.tracks]
            #pdb.set_trace()
            cv2.polylines(self.image, hulls1, 1, (0, 255, 255))

        return self.image
