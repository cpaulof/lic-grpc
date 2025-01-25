import grpc

from server.models_pb2 import GetRequest
from server.models_pb2_grpc import ModelServiceStub

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ModelServiceStub(channel)
        get_request = GetRequest(id=1, type="week", page=1, amount=1)
        r = stub.getPublications(get_request)
        # while not r.done():
            
        print(r)
        for i in r: print(i)
        
run()





