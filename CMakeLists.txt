cmake_minimum_required(VERSION 3.15...3.19)

project(sc-leflib)

# Need C++11 support
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Packages we rely on
find_package(PythonInterp)
find_package(PythonLibs)
find_package(PythonExtensions)
find_package(Cython REQUIRED)

set(TOOLS_SCRIPT ${CMAKE_CURRENT_LIST_DIR}/siliconcompiler/siliconcompiler/toolscripts/_tools.py)

execute_process(
  COMMAND python3 ${TOOLS_SCRIPT} --tool openroad --field git-url
  OUTPUT_VARIABLE openroad_URL
)
string(STRIP ${openroad_URL} openroad_URL)
execute_process(
  COMMAND python3 ${TOOLS_SCRIPT} --tool openroad --field git-commit
  OUTPUT_VARIABLE openroad_COMMIT
)
string(STRIP ${openroad_COMMIT} openroad_COMMIT)

include(FetchContent)
FetchContent_Declare(openroad
  GIT_REPOSITORY    ${openroad_URL}
  GIT_TAG           ${openroad_COMMIT}
  CONFIGURE_COMMAND ""
  BUILD_COMMAND     ""
)

# Needed to find *.pxd file
include_directories(${CMAKE_CURRENT_LIST_DIR}/sc_leflib)

# Build Cython module
# source: https://github.com/scikit-build/scikit-build-sample-projects/blob/master/projects/hello-cython/hello/CMakeLists.txt
add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/sc_leflib)
add_cython_target(_leflib ${CMAKE_CURRENT_LIST_DIR}/sc_leflib/_leflib.pyx CXX)
add_library(_leflib MODULE ${_leflib})
python_extension_module(_leflib)

# Link in lef library
target_link_libraries(_leflib lef)

# We want to be extra strict about error checking -- enable all warnings and
# treat them as errors. We only apply this to the _leflib target since the LEF
# parser library has warnings under -Wall -pedantic, but there's not much we can
# do about those.
#
# We exempt deprecated-declarations since Cython uses something deprecated in at
# least one of the Python versions we support, and there's not much we can do
# about that either.
#
# Microsoft's compiler uses a totally different set of flags, so we just set
# these for MacOS/Linux (which will be using GCC or clang).
if(NOT WIN32)
    target_compile_options(_leflib PRIVATE -Wall -Werror -Wno-error=deprecated-declarations)
endif()

FetchContent_Populate(openroad)
# Stuff to include Si2 LEF library
set(LEF_DIR ${openroad_SOURCE_DIR}/src/odb/src/lef)

# this lets us include lef headers
include_directories(${LEF_DIR}/lef)
# this causes cmake to build lef/
add_subdirectory(${LEF_DIR})

# The CMake config for the LEF parser sets a single compilation option,
# -Wno-class-memaccess, which is incompatible with Microsoft's compiler. I don't
# see any particular reason to enable this warning, so overwrite the flags here
# to ensure our Windows build passes.
set_target_properties(lef PROPERTIES COMPILE_OPTIONS "")

install(TARGETS _leflib DESTINATION .)
