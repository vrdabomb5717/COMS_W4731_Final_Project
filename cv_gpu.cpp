#include <boost/python.hpp>
#include "gpu.hpp"

using namespace boost::python;

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(cvt_overloads, cvtColor, 2, 4)
BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(features_overloads, goodFeaturesToTrack, 4, 9)

BOOST_PYTHON_MODULE(cv_gpu)
{
	docstring_options local_docstring_options(true, false, false);

/*
	cvtColor is an example of a method in class GPU you wish to expose.
	One line for each method (or function depending on how you
	structure your code).

	Note: You don't have to expose everything in the library,
	just the ones you wish to make available to python.
*/

	class_<GPU>("GPU")
	.def(init<>())
	.def("cvtColor", &GPU::cvtColor, cvt_overloads(args("src", "code", "dst", "dstCn"),
	     "cvtColor(src, code[, dst[, dstCn]]) -> dst"))
	.def("goodFeaturesToTrack", &GPU::goodFeaturesToTrack, features_overloads(args("image", "maxCorners", "qualityLevel", "minDistance",
	     "corners", "mask", "blockSize", "useHarrisDetector", "k"),
	     "goodFeaturesToTrack(image, maxCorners, qualityLevel, minDistance[, corners[, mask[, blockSize[, useHarrisDetector[, k]]]]]) -> corners"))
	;
}