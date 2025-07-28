# Description

This directory contains example projects demonstrating how to use the Hudiy API.

Examples are provided in both **Python** and **HTML/JavaScript**.

## HTML/JavaScript

**HTML/JavaScript** examples located in the `api/js` directory must be accessed via an HTTP server.

The easiest way to start an HTTP server on a Raspberry Pi is by using `node-http-server`. To install it, run:

```bash
sudo apt install -y node-opener node-http-server
```

Once installed, navigate to the `api/js` directory and start the server with:

```bash
http-server -p 12345
```

This will launch a local web server. You can then access the examples at: `http://127.0.0.1:12345`

All HTML/JavaScript examples can be used as **overlays**, **widgets**, or **applications** in Hudiy.

If your HTML/JavaScript does not refresh after changes, consider removing the cache in $HOME/.hudiy/cache/web

## Python

For Python examples, please install the required dependencies using the `requirements.txt` file.


To generate Python files from the Api.proto definition, you need to install the Protocol Buffers compiler:

```bash
sudo apt install -y protobuf-compiler
```

Then generate the Python files by running:

```bash
protoc --python_out=python/common ../api/Api.proto
```