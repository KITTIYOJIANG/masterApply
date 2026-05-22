CXX := g++
CXXFLAGS := -std=c++17 -Wall -Wextra -O2
INCLUDES := -I include

.PHONY: all clean test

all: test

test: test_vec2.exe test_vec3.exe
	./test_vec2.exe
	./test_vec3.exe

test_vec2.exe: tests/test_vec2.cpp include/mini_robotics/vec2.h
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ tests/test_vec2.cpp

test_vec3.exe: tests/test_vec3.cpp include/mini_robotics/vec3.h
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ tests/test_vec3.cpp

clean:
	rm -f test_vec2.exe test_vec3.exe
