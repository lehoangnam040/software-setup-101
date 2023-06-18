import grpc
import time
from grpc_health.v1.health_pb2 import HealthCheckRequest, HealthCheckResponse, _HEALTHCHECKRESPONSE_SERVINGSTATUS

from grpc_health.v1.health_pb2_grpc import HealthStub

channel = grpc.insecure_channel("localhost:50051")
stub = HealthStub(channel)
print("send request")
resp = stub.Check(
    HealthCheckRequest(),
)
print(resp)