PYTHON_VERSION = 2.7.4
PYTHON_INCLUDE = /usr/local/Cellar/python/$(PYTHON_VERSION)/Frameworks/Python.framework/Headers/
PYTHON_LIB = /usr/local/Cellar/python/$(PYTHON_VERSION)/Frameworks/Python.framework/Versions/Current/lib/

NUMPY_INCLUDE = /usr/local/lib/python2.7/site-packages/numpy/core/include/

# location of the Boost Python include files and library
BOOST_LIB = /usr/local/lib/
BOOST_INC = /usr/local/include/boost

OPENCV_LIB = `pkg-config --libs opencv`
OPENCV_CFLAGS = `pkg-config --cflags opencv`

CFLAGS= -O3 -march=native -Wall -Wextra -Wfloat-equal -Wundef -Wstrict-prototypes -Wpointer-arith -Wwrite-strings -Winit-self

TARGET = cv_gpu
SRC = cv_gpu.cpp gpu.cpp
OBJ = cv_gpu.o gpu.o

$(TARGET).so: $(OBJ)
	g++ -shared $(OBJ) -L$(BOOST_LIB) -lboost_python-mt -L$(PYTHON_LIB) -lpython2.7 -o $(TARGET).so $(OPENCV_LIB)

$(OBJ): $(SRC)
	g++ -I$(PYTHON_INCLUDE) -I$(NUMPY_INCLUDE) -I$(BOOST_INC) $(OPENCV_CFLAGS) -fPIC -c $(SRC)

clean:
	rm -f $(OBJ)
	rm -f $(TARGET).so