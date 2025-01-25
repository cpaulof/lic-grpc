import datetime

from peewee import SqliteDatabase
from peewee import (Model,
                    CharField,
                    ForeignKeyField,
                    TextField,
                    DateTimeField,
                    BooleanField,
                    DateField,
                    DecimalField,
                    IntegerField)

import config


db = SqliteDatabase(config.DATABASE_URL)

class BaseModel(Model):
    class Meta:
        database = db

class UrlSource(BaseModel):
    name = TextField()
    url = TextField()
    
class Publication(BaseModel):
    title = TextField()
    url = TextField(unique=True)
    description = TextField()
    content = TextField(default="")
    hierarchy = TextField()
    url_source = ForeignKeyField(UrlSource, backref='publications')
    pub_date = DateTimeField()
    art_type = TextField()
    prob = TextField()
    content_fetched = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now)
    
    #
    mark = IntegerField(default=0)
    status = IntegerField()
    
    due_date = DateTimeField(default=datetime.datetime.now)
    due_reason = IntegerField(default=0) #0=DEFAULT(+10dias) 1=detected
    
    #
    # uid = TextField(default="")
    


class ScheduleSettings(BaseModel):
    type = TextField(unique=True)
    interval = IntegerField()
    last_executed = DateTimeField()
    
    def __repr__(self):
        return f"<Scheduler type={self.type} last_time={self.last_executed}>"
    
    def __str__(self):
        return f"<Scheduler type={self.type} last_time={self.last_executed}>"

class TaskCompletion(BaseModel):
    date = TextField()
    description = TextField(default="")
    
 
    
    
