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

	// We want our python code to be able to call this function to do some processing using OpenCV and return the result.
    PyObject* cvtColor(PyObject* image, int code, PyObject* dst=Py_None, int dstCn=0);
};

#endif