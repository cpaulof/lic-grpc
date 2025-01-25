import datetime
import sys
import os
sys.path.append(os.getcwd())
from database import models
import config


class Service:
    def __init__(self):
        self.db = models.db
        try:
            self.db.connect()
            self.db.create_tables([models.UrlSource, models.Publication, models.TaskCompletion, models.ScheduleSettings ], safe=True)
        except: pass
    
    def validate_do3_pub(self, pub):
        try:
            date = pub['pubDate']
            date = date.split('/')[::-1]
            assert len(date) == 3
            
            title = pub['title']
            assert title and isinstance(title, str)
            
            url = pub['urlTitle']
            assert url and isinstance(url, str)
            
            description = pub['content']
            assert description and isinstance(description, str)
            
            hierarchy = pub['hierarchyStr']
            assert hierarchy and isinstance(hierarchy, str)
            
            art_type = pub['artType']
            assert art_type and isinstance(art_type, str)
            
            return date, title, url, description, hierarchy, art_type

        except Exception as e:
            if config.DEBUG:
                print("[DEBUG] error on 'create_pub_from_do3' ->", e.__class__, e)
            
    def create_pub_from_do3(self, json, prob, content=None, status=3, due_date=None):
        try:
            cleaned_data = self.validate_do3_pub(json)
            if cleaned_data is None: return
            
            date, title, url, description, hierarchy, art_type = cleaned_data
            date = datetime.datetime.fromisoformat('{}-{:0>2}-{:0>2}'.format(*date))
            
            # print(date, title, url, description, hierarchy, art_type)
            url_source, just_created = models.UrlSource.get_or_create(name="do3", url=config.BASE_DOU3_URL)
            if just_created and config.DEBUG:
                print('Created URL SOURCE:', url_source)
                
            if due_date is None:
                due_date = datetime.datetime.now()
            pub = models.Publication(title=title,
                                    url=url,
                                    description=description,
                                    hierarchy=hierarchy,
                                    url_source=url_source,
                                    pub_date=date,
                                    art_type=art_type,
                                    prob=str(prob),
                                    status=status,
                                    due_date=due_date)
            
            if content and isinstance(content, str):
                pub.content = content
                pub.content_fetched = True
                
            pub.save()
            return True
        
            
        except Exception as e:
            if config.DEBUG:
                print("[DEBUG] error on 'create_pub_from_do3' ->", e.__class__, e)
        
        return False
    
    def get_publication_by_url(self, url):
        try:
            pub = models.Publication.get(url=url)
        except models.Publication.DoesNotExist:
            pub = None
        return pub
    
    def set_publication_content(self, url, content):
        pub = self.get_publication_by_url(url)
        try:
            pub.content = content
            pub.content_fetched = True
            pub.save()
            
        except Exception as e:
            if config.DEBUG:
                print("[DEBUG] error on 'set_publication_content' ->", e.__class__, e)
    
    ## scheduler    
    def update_schedule(self, type, interval, default_time_of_day=config.SCHEDULER_DEFAULT_TIME_OF_DAY, callback=None):
        
        try: 
            sch = self.get_schedule(type)
            sch.last_executed = datetime.datetime.now()
            sch.interval = interval
            hour, minute, second = (int(i) for i in default_time_of_day.split(':'))
            sch.last_executed = sch.last_executed.replace(hour=hour, minute=minute, second=second)
            sch.save()
            if callback is not None:
                return callback(sch)
        except Exception as e:
            print(e)
        
    
    def create_schedule(self, type, interval, default_time_of_day=config.SCHEDULER_DEFAULT_TIME_OF_DAY, callback=None):
        try: 
            default_date=datetime.datetime.fromtimestamp(0)
            sch = models.ScheduleSettings(type=type, interval=interval, last_executed=default_date)
            hour, minute, second = (int(i) for i in default_time_of_day.split(':'))
            sch.last_executed = sch.last_executed.replace(hour=hour, minute=minute, second=second)
            sch.save()
            if callback is not None:
                return callback(sch)
        except Exception as e:
            print(e)
        
    
    def get_schedule(self, type):
        try: return models.ScheduleSettings.get(type=type)
        except: return None
    
    def get_schedules(self):
        return models.ScheduleSettings.select()
    
    def create_task_completion(self, date, desc=""):
        try:
            t = models.TaskCompletion(
                date=date,
                description=desc
            )
            t.save()
        except:
            pass
    
    def is_task_complete(self, date):
        try:
            t = models.TaskCompletion.get(date=date)
        except models.TaskCompletion.DoesNotExist:
            t = None
        return t != None

if __name__ == "__main__":
    db = Service()
    
    sch = db.create_or_update_schedule("daily2", 86400, config.SCHEDULER_DEFAULT_TIME_OF_DAY)
    print(list(db.get_schedules()))
    