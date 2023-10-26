set(BUILD_SHARED_LIBS OFF)
set(BUILD_TEST OFF)
set(BUILD_TESTING OFF)
set(BOOST_ENABLE_MPI OFF)
set(BOOST_ENABLE_PYTHON OFF)
set(BOOST_USE_MULTITHREADED ON)
set(BOOST_USE_STATIC_LIBS ON)
set(INSTALL_TEST OFF)
set(SKIP_BUILD_TEST ON)

set(BOOST_IOSTREAMS_ENABLE_ZLIB ON)

set(CMAKE_BUILD_TYPE Release)

add_compile_options(-Wno-everything)

add_subdirectory(boost)

include_directories(PUBLIC contrib/boost)
