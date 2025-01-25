DEBUG = True


DATABASE_URL = "./database/data/db.sqlite"

BASE_DOU3_URL = "https://www.in.gov.br/leiturajornal?data={date}&secao=do3"
BASE_PUB_DETAIL_URL = 'https://www.in.gov.br/web/dou/-/'

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5454

PROB_THRESHOLD = 0.70

PRE_FILTERS = [
    ('artType', 'contains_any', ['aviso de licitação']),
    ('hierarchyStr', 'contains_any', ['Maranhão'])
    ]

FILTER_FORCE_SEARCHED_URL_IDS = False

ML_TOKENIZER_PATH = "./ml/byte-level-bpe.tokenizer.json"
ML_MODEL_WEIGHTS_PATH = "./ml/model.pt"

SERVER_MIN_STATUS_LEVEL_TO_SAVE = 3
SERVER_SEND_REPORT_EVERY = 100


# scheduler
SCHEDULER_CHECK_INTERVAL = 5
SCHEDULER_DEFAULT = {
    'daily':1*60*60*24
}
SCHEDULER_DEFAULT_TIME_OF_DAY = "14:00:00"