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
    PyObject* goodFeaturesToTrack(PyObject* image, int maxCorners, double qualityLevel, double minDistance,
                                  PyObject* corners=Py_None, PyObject* mask=Py_None, int blockSize=3,
                                  bool useHarrisDetector=false, double k=0.04);

private:
    bool isGPUEnabled;
};

#endif