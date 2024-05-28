cmake_minimum_required(VERSION 3.10)
project(server_socket)

set(CMAKE_C_STANDARD 11)

# Find the Winsock2 library
#find_library(WS2_32_LIBRARY NAMES ws2_32)
set(WS2_32_LIBRARY "D:/Programming_Library/mingw64/x86_64-w64-mingw32/lib/libws2_32.a")
# Find the cJSON library (assuming you have it installed or you can specify the path)
find_library(CJSON_LIBRARY NAMES cjson PATHS .)

add_executable(server_socket server_socket.c)

# Link the required libraries
target_link_libraries(server_socket ${WS2_32_LIBRARY} ${CJSON_LIBRARY})
