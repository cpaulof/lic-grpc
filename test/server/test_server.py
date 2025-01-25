from server import main_server
import database

main_server = main_server.Server()

main_server.start_grpc_server()