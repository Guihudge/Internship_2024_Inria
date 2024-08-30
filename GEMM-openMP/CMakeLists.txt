cmake_minimum_required(VERSION 3.12)

project(Product CXX C Fortran)

# Need c++20
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_CXX_FLAGS_RELEASE "-O3")

set(maphyspp_DIR /home/guillaume/Documents/compose-mkl2023/lib/cmake/maphyspp)

#OpenMP
find_package(OpenMP)

#Maphys++
find_package(maphyspp REQUIRED)

add_executable(product main.cpp)

target_link_libraries(product PUBLIC OpenMP::OpenMP_CXX)
target_link_libraries(product PRIVATE MAPHYSPP::maphyspp)

