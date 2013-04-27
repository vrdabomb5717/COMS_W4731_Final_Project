#include <boost/python.hpp>
#include "gpu.hpp"

using namespace boost::python;

BOOST_PYTHON_MODULE(cv_gpu)
{
    class_<GPU>("GPU")
	.def(init<>())
	.def("cvtColor", &GPU::cvtColor) // cvtColor is the method in class GPU you wish to expose. One line for each method (or function depending on how you structure your code). Note: You don't have to expose everything in the library, just the ones you wish to make available to python.
    ;
}