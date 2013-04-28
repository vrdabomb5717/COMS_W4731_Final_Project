#include <Python.h>
#include <boost/python.hpp>
#include "gpu.hpp"

using namespace boost::python;

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
	.def("cvtColor", &GPU::cvtColor, (arg("src"), arg("code"), arg("dst")=object(), arg("dstCn")=0),
	     "cvtColor(src, code[, dst[, dstCn]]) -> dst")
	.def("goodFeaturesToTrack", &GPU::goodFeaturesToTrack, (arg("image"), arg("maxCorners"), arg("qualityLevel"), arg("minDistance"),
	     arg("corners")=object(), arg("mask")=object(), arg("blockSize")=3, arg("useHarrisDetector")=false, arg("k")=0.04),
	     "goodFeaturesToTrack(image, maxCorners, qualityLevel, minDistance[, corners[, mask[, blockSize[, useHarrisDetector[, k]]]]]) -> corners")
	;
}