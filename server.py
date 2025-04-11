import os
import sys

import gateway_pb2_grpc

import random

# Add project root to the module path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import time
import logging
from concurrent import futures

import grpc
import gateway_pb2


# Setup logging
logging.basicConfig(
    filename='logs/gateway.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

product_state = {
    "device_id": "dev001",
    "sample_rate": 10,
    "wifi_enabled": True,
    "light_on": False,
    "uptime_start": time.time()
}

class GatewayService(gateway_pb2_grpc.GatewayServicer):
    def SetConfig(self, request, context):
        product_state["sample_rate"] = request.sample_rate
        product_state["wifi_enabled"] = request.enable_wifi
        logging.info(f"[SetConfig] Received: {request}")
        return gateway_pb2.Status(success=True, message="Config applied")

    def GetStatus(self, request, context):
        uptime_sec = int(time.time() - product_state["uptime_start"])
        logging.info("[GetStatus] Request received.")
        return gateway_pb2.DeviceStatus(
            device_id=product_state["device_id"],
            uptime=f"{uptime_sec}s",
            light_on=product_state["light_on"],
            wifi_connected=product_state["wifi_enabled"]
        )

    def TurnOnLight(self, request, context):
        product_state["light_on"] = request.turn_on
        logging.info(f"[TurnOnLight] Light {'ON' if request.turn_on else 'OFF'}")
        return gateway_pb2.Status(success=True, message="Light command received")
    
    def StreamTelemetry(self, request, context):
        device_id = product_state["device_id"]
        logging.info("[StreamTelemetry] Telemetry stream started.")

        while True:
            data = gateway_pb2.TelemetryData(
                device_id=device_id,
                temperature=50,
                humidity=60,
                timestamp=10
            )
            logging.info(f"[Telemetry] Sent: {data}")
            yield data
            time.sleep(product_state["sample_rate"])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    gateway_pb2_grpc.add_GatewayServicer_to_server(GatewayService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("gRPC server started on port 50051")
    print("🚀 Gateway gRPC Server is running on port 50051...")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
