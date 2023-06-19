from grpc_health.v1 import health as grpc_heath, health_pb2_grpc
import grpc
from concurrent import futures
import prometheus_client


if __name__ == '__main__':
    grpc_options = [
        ("grpc.max_send_message_length", 256 * 1024 * 1024),
        ("grpc.max_receive_message_length", 256 * 1024 * 1024),
    ]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=grpc_options,
        interceptors=[],
    )
    health_pb2_grpc.add_HealthServicer_to_server(grpc_heath.HealthServicer(), server)
    server.add_insecure_port("[::]:%d" % 50054)
    server.start()
    prometheus_client.start_http_server(50053)
    server.wait_for_termination()