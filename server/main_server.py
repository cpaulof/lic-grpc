import os
import sys
sys.path.append(os.getcwd())

import time
import datetime
import threading
import grpc
from concurrent import futures

from scraper import utils, scraper
from database.service import Service
from database  import models
import config

from server import models_pb2_grpc
from server.models_server import ModelServiceServicer


class Server:
    def __init__(self):
        self.db:Service = Service()
    
    def pub_filter_status_callback(self, pub, content, prob, total_pbs, current, status, status_count):
        if status >= config.SERVER_MIN_STATUS_LEVEL_TO_SAVE:
            self.db.create_pub_from_do3(pub, prob, content, status)
        if current % config.SERVER_SEND_REPORT_EVERY == 0 or current+1==total_pbs: # send every N step or if it's the last
            self.send_filter_status(total_pbs, current, status, status_count)
            
    def process_today(self):
        print('processing today')
        today = datetime.date.today()
        return self.process_date(today)
    
    def process_date(self, date):
        date = utils.format_date(date)
        scrap = scraper.SingleScrapper(date, self.pub_filter_status_callback)
        scrap.filter()
        self.db.create_task_completion(date)
    
    def process(self, initial_date, days):
        dates = utils.format_multiple_dates(initial_date, days)
        for date in dates:
            scrap = scraper.SingleScrapper(date, self.pub_filter_status_callback)
            scrap.filter()
            
    #
    def send_filter_status(self, total_pbs, current, status, status_count):
        pass
    
    def start_watch_for_schedules(self, scheduler):
        t = threading.Thread(target=self.watch_for_schedules, args=(scheduler,))
        t.start()
        print("Watching for schedules THREAD started!")
        
    def watch_for_schedules(self, scheduler):
        while True:
            try:
                scheduler.check_schedules()
                time.sleep(config.SCHEDULER_CHECK_INTERVAL)
            except Exception as e: 
                print(e)
                return
    
    def start_grpc_server(self):
        print('Configuring GRPC Server')
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        print('...adding services')
        models_pb2_grpc.add_ModelServiceServicer_to_server(ModelServiceServicer(), server)
        server.add_insecure_port("[::]:50051")
        print('...binding to port 50051')
        server.start()
        print('...server started!')
        server.wait_for_termination()
  