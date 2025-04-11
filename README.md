# Embedded Gateway Simulator using gRPC & Protobuf

![Python](https://img.shields.io/badge/python-3.11-blue)
![gRPC](https://img.shields.io/badge/gRPC-enabled-green)
![Protobuf](https://img.shields.io/badge/Protocol%20Buffers-v3-blueviolet)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project simulates a realistic embedded system gateway using Python, gRPC, and Protocol Buffers. It models how a mobile/cloud application communicates with a connected embedded product through a gateway — a pattern commonly used in IoT systems (e.g., smart homes, industrial sensors).

---

## Features

- **gRPC Server** simulating an embedded gateway
- **gRPC Client** simulating a cloud or mobile app
- **Protobuf messages** for structured, binary-compatible communication
- Supports RPCs for:
  - Setting configuration (e.g., sample rate, WiFi)
  - Controlling hardware (e.g., light on/off)
  - Getting status
  - Streaming telemetry (temperature, humidity)
- Optional conversion to serialized binary data (e.g., for UART transmission)
- Logging to file for debugging and replay

---

## Architecture

```
        +---------------------+
        |   gRPC Client (Pi)  |     ← Simulates mobile/cloud
        +---------------------+
                  │
                  ▼
        +---------------------+
        |  gRPC Server (PC)   |     ← Simulates embedded gateway
        |  (Logs + Streaming) |
        +---------------------+
                  │
                  ▼
        [ Protobuf Binary (UART) ]
```
---

## Folder Structure

```
.
├── client.py              # gRPC client script
├── server.py              # gRPC server script
├── protos/
│   └── gateway.proto      # Protobuf schema
├── gateway_pb2.py         # Auto-generated from .proto (after build)
├── gateway_pb2_grpc.py    # Auto-generated from .proto (after build)
├── logs/
│   └── gateway.log        # Runtime logs
├── LICENSE                # MIT license
├── .gitignore             # Git ignored files
└── README.md              # You're here!
```

---

## Getting Started

### Install Dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install grpcio grpcio-tools
```

### Compile Protobuf
```bash
python -m grpc_tools.protoc \
  -I protos \
  --python_out=. \
  --grpc_python_out=. \
  protos/gateway.proto
```

### ▶ Run the Server
```bash
python server.py
```

### ▶ Run the Client
In a new terminal (while server is running):
```bash
python client.py
```

---

## Real-World Relevance
This project mimics the architecture used in embedded companies like Google Nest, Tesla, and others:
- Binary-encoded telemetry via Protobuf
- Edge-device to cloud communication via gRPC
- Test harnesses using simulated gateways

Even if the physical product uses UART and REST, this simulation provides:
- Automation
- Testable behavior
- Reusable tooling

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Questions or Ideas?
Feel free to fork, open issues, or submit pull requests!
