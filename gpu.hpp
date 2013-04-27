#ifndef GPU_HPP
#define GPU_HPP

#include <Python.h>
#include <string>

class GPU
{
public:
	// Other declarations
	GPU();
	virtual ~GPU();
    PyObject* cvtColor(PyObject* image, PyObject* code); // We want our python code to be able to call this function to do some processing using OpenCV and return the result.
	// Other declarations
};

#endif