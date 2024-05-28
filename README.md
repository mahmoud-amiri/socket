# socket

developing a general socket server and client in python and c

## build in windows

### build client

```sh
cd ./c/client
mkdir build
cmake ..
cmake --build .
```

### build server

```sh
cd ./c/server
mkdir build
cmake ..
cmake --build .
```

## run in windows

```sh
./c/client/build/client_socket.exe 127.0.0.1 5000
./c/server/build/server_socket.exe
```
