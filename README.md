# Socket Chatroom

## Introduction

A simple program that enables client to chat with each other through a server, which broadcast the message to all clients with encoding. Client needs to enter correct code to decode the encoded message.

## Demo

[![DEMO video](http://img.youtube.com/vi/n9ZCqZMH89c/0.jpg)](http://www.youtube.com/watch?v=n9ZCqZMH89c "Socket Chatroom")

## Usage

Open one terminal for server and others for client.

In the server terminal, run the following command:

```{bash}
python3 server.py
```

In the client terminal, run the following command:

```{bash}
python3 client.py {server_ip} {server_port}
```
The default server ip is localhost(127.0.0.1) and port is 5002
