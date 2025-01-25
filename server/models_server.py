from google.protobuf.timestamp_pb2 import Timestamp
import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from server import models_pb2
from server import models_pb2_grpc

from database import models


class ModelServiceServicer(models_pb2_grpc.ModelServiceServicer):
    def __init__(self):
        self.get_functions = {
            'all': self.get_all,
            'month': self.get_last_month,
            'week': self.get_last_week,
            'today': self.get_today,
        }
    
    def pub_model_to_message(self, pub:models.Publication):
        pub_date = Timestamp()
        created_at = Timestamp()
        due_date = Timestamp()
        pub_date.FromDatetime(pub.pub_date)
        created_at.FromDatetime(pub.created_at)
        due_date.FromDatetime(pub.due_date)
        
        return models_pb2.Publication(
            name = pub.title,
            url = pub.url,
            description = pub.description,
            content = pub.content,
            hierarchy = pub.hierarchy,
            pub_date = pub_date,
            art_type = pub.art_type,
            prob = float(pub.prob),
            content_fetched = pub.content_fetched,
            created_at = created_at,
            mark = pub.mark,
            status = pub.status,
            due_date = due_date,
            due_reason = pub.due_reason,
            id = pub.id)
        
    # get
    def get_all(self, request:models_pb2.GetRequest):
        for pub in models.Publication.select().paginate(request.page, request.amount).iterator():
            pub_message = self.pub_model_to_message(pub)
            #print(pub_message)
            yield pub_message
        
    def get_from_timedelta(self, request, days):
        timedelta = datetime.date.today() - datetime.timedelta(days=days)
        for pub in models.Publication.select().where(models.Publication.pub_date >= timedelta).paginate(request.page, request.amount).iterator():
            yield self.pub_model_to_message(pub)
        
    def get_last_month(self, request:models_pb2.GetRequest):
        return self.get_from_timedelta(request, days=30)
            
    def get_last_week(self, request:models_pb2.GetRequest):
        return self.get_from_timedelta(request, days=7)
            
    def get_today(self, request:models_pb2.GetRequest):
        return self.get_from_timedelta(request, days=0)
    
    def getPublications(self, request:models_pb2.GetRequest, context):
        if request.type not in self.get_functions.keys():
            return iter(())
        return self.get_functions[request.type](request)
    
    def setInterest(self, request:models_pb2.MarkRequest, context):
        if request.type not in self.get_functions.keys():
            return iter(())
        return self.get_functions[request.type](request)



if __name__ == "__main__":
    m = ModelServiceServicer()
    get_request = models_pb2.GetRequest(id=1, type="all", page=1, amount=10)
    print(list(m.get_all(get_request)))