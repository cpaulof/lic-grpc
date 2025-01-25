import datetime
import threading

from database import service
import config

class Scheduler:
    def __init__(self, run_func, run_async=True):
        self.db_service = service.Service()
        self.run = run_func
        self.run_async = run_async
        
        # first time/intial check
        for sch_type, sch_interval in config.SCHEDULER_DEFAULT.items():
            self.db_service.create_schedule(sch_type, sch_interval)

    def check_schedules(self):
        
        for sch in self.db_service.get_schedules():
            now = datetime.datetime.now()
            if (now - sch.last_executed).total_seconds() >= sch.interval:
                print("Executing scraper due to scheduler:", sch, type(sch))
                self.run()
                self.db_service.update_schedule(sch.type, sch.interval)
      
    
    def _run(self):
        t = threading.Thread(target=self.run)
        t.start()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    