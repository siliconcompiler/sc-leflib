cmake_minimum_required(VERSION 3.15...3.30)

project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

# Need C++11 support
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find Python first
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

# Find Cython via cython-cmake
find_package(Cython MODULE REQUIRED VERSION 3.0)

# Include the Cython helper functions
include(UseCython)

# Transpile Cython to C++
cython_transpile(
    "${CMAKE_CURRENT_SOURCE_DIR}/sc_leflib/_leflib.pyx"
    LANGUAGE CXX
    OUTPUT_VARIABLE CYTHON_OUTPUT
    CYTHON_ARGS "-I${CMAKE_CURRENT_SOURCE_DIR}/sc_leflib"
)

# Build the Python extension module
Python_add_library(_leflib MODULE ${CYTHON_OUTPUT} WITH_SOABI)

# Include directories for C++ compilation
target_include_directories(_leflib PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/sc_leflib)

# Link against the LEF library
target_link_libraries(_leflib PRIVATE lef)

# Strict error checking (not on Windows)
if(NOT WIN32)
    target_compile_options(_leflib PRIVATE -Wall -Werror -Wno-error=deprecated-declarations)
endif()

# Install the extension module to the package directory
install(TARGETS _leflib DESTINATION ${SKBUILD_PROJECT_NAME})

# Build the LEF C++ library
set(LEF_DIR ${CMAKE_CURRENT_SOURCE_DIR}/lef)
include_directories(${LEF_DIR}/lef)
add_subdirectory(${LEF_DIR})

# The CMake config for the LEF parser sets a single compilation option,
# -Wno-class-memaccess, which is incompatible with Microsoft's compiler. I don't
# see any particular reason to enable this warning, so overwrite the flags here
# to ensure our Windows build passes.
set_target_properties(lef PROPERTIES COMPILE_OPTIONS "")
