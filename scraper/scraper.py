from scraper import filter, utils
import database
from ml.inference import InferenceModel

import config


db_service = database.db_service
model = InferenceModel()

class SingleScrapper:
    '''realiza o download, processamento e armazenamento de um único dia.'''
    def __init__(self, date, report_status_callback=None):
        self.date = date
        self.data =  utils.get_diario_as_json(date)['jsonArray']
        print(len(self.data), len(str(self.data)))
        self.total_pubs = len(self.data)
        
        self.report_status_callback = report_status_callback
        if report_status_callback is None:
            self.report_status_callback = lambda *x: None
        
        self.pub_status_count = [0]*4
    
    def filter(self):
        i = -1
        for pub in self.data:
            i+=1
            url_id = pub['urlTitle']
            status = 0
            print(r'\r'+str(self.pub_status_count)+" i="+str(i), end='               ')
            existing_pub = db_service.get_publication_by_url(url_id)
            #print(existing_pub, pub)
            if existing_pub is not None:
                self.pub_status_count[status]+=1
                # url already searched for, skipping if not forced to reprocess
                if not config.FILTER_FORCE_SEARCHED_URL_IDS:
                    self.report_status_callback(pub,            # pub data
                                                None,           #
                                                -1,
                                                self.total_pubs,# total size
                                                i,              # current
                                                status,               # status,
                                                self.pub_status_count 
                                                )
                    
                    continue
            print('12')
            status = 1   
            if not filter.handle_pre_filters(config.PRE_FILTERS, pub):
                self.pub_status_count[status]+=1
                self.report_status_callback(pub,            # pub data
                                            None,           # pub content
                                            -1,
                                            self.total_pubs,# total size
                                            i,              # current
                                            1,               # status,
                                            self.pub_status_count 
                                            )
                continue
            print('13')
            # only fetch rest of pub content if pre filters pass
            status = 2 
            content = utils.get_pub_complete_content(url_id)
            print('content')
            print(content)
            prob = model(content)[1]
            print(prob)
            if prob < config.PROB_THRESHOLD:
                self.pub_status_count[status]+=1
                self.report_status_callback(pub,            # pub data
                                            content,        # pub content
                                            prob,           # prob
                                            self.total_pubs,# total size
                                            i,              # current
                                            2,               # status,
                                            self.pub_status_count 
                                            )
                continue
            print('14')
            status = 3
            self.pub_status_count[status]+=1
            self.report_status_callback(pub,            # pub data
                                        content,        # pub content
                                        prob,           # prob
                                        self.total_pubs,# total size
                                        i,              # current
                                        3,               # status,
                                        self.pub_status_count
                                        )
            print('15')
            
                
                
    





# status breakdown
# 0 -> ignored 'cause already searched
# 1 -> didnt pass pre filters
# 2 -> passed filters but probability was lower than PROB_THRESHOLD
# 3 -> good prob, saved! 
















