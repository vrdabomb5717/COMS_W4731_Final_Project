#include <boost/python.hpp>
#include "gpu.hpp"

using namespace boost::python;

BOOST_PYTHON_MEMBER_FUNCTION_OVERLOADS(gpu_overloads, cvtColor, 2, 4)

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
	.def("cvtColor", &GPU::cvtColor, gpu_overloads(args("src", "code", "dst", "dstCn"),
	     "cvtColor(src, code[, dst[, dstCn]]) -> dst"))
	;
}