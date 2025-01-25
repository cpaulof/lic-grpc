import server
import server.main_server
import server.scheduler

grpc_server = server.main_server.Server()
scheduler = server.scheduler.Scheduler(grpc_server.process_today)
grpc_server.start_watch_for_schedules(scheduler)