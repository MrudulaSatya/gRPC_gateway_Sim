import grpc
import gateway_pb2
import gateway_pb2_grpc

def run():
    # Connect to the server on localhost
    channel = grpc.insecure_channel('localhost:50051')
    stub = gateway_pb2_grpc.GatewayStub(channel)

    # Send SetConfig
    config = gateway_pb2.Config(
        device_id="dev001",
        sample_rate=10,
        enable_wifi=True
    )
    response = stub.SetConfig(config)
    print(f"[SetConfig] Server Response: {response.message}")

    # Send TurnOnLight
    light_cmd = gateway_pb2.LightCommand(
        device_id="dev001",
        turn_on=True
    )
    response = stub.TurnOnLight(light_cmd)
    print(f"[TurnOnLight] Server Response: {response.message}")

    # Call GetStatus
    response = stub.GetStatus(gateway_pb2.Empty())
    print(f"[GetStatus] Device ID: {response.device_id}")
    print(f"           Uptime: {response.uptime}")
    print(f"           Light ON: {response.light_on}")
    print(f"           WiFi Connected: {response.wifi_connected}")

    # Call StreamTelemetry
    print("\n[StreamTelemetry] Receiving telemetry data...\n")
    stream = stub.StreamTelemetry(gateway_pb2.Empty())

    try:
        for reading in stream:
            print(f"[Telemetry] Timestamp: {reading.timestamp} | Humidity:{reading.humidity}% | Temmperature:{reading.temperature}F")
            binary_data = reading.SerializeToString()
    except KeyboardInterrupt:
        print("Telemetry stream stopped by user.")
      


if __name__ == '__main__':
    run()
