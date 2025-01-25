## **Project Overview**  
This is a **Python-based backend system** designed to scrape, process, store, and serve structured publication data (e.g., legal notices, articles) from sources like Brazil’s Official Gazette (DOU). It integrates:  
- **Web Scraping**: Collects raw data from specified URLs.  
- **Machine Learning (ML)**: Filters publications by relevance using a transformer-based model.  
- **gRPC API**: Serves filtered data to clients with pagination and time-based queries.  
- **SQLite Database**: Stores publications and task metadata.  
- **Scheduler**: Automates periodic tasks (e.g., daily scraping).  

---

## **System Architecture**  
```  
┌──────────────┐       ┌──────────────┐       ┌──────────────┐  
│   Scraper    │──────▶│   Database   │──────▶│  gRPC Server │  
└──────────────┘       └──────────────┘       └──────────────┘  
       │                       ▲                       │  
       │ ML Filtering          │ Scheduler             │ Client  
       ▼                       │                       ▼  
┌──────────────┐       ┌──────────────┐       ┌──────────────┐  
│   ML Model   │       │   Config     │       │   gRPC Client│  
└──────────────┘       └──────────────┘       └──────────────┘  
```  

---

## **Directory Structure**  
| Directory      | Key Components                                                                 |  
|----------------|-------------------------------------------------------------------------------|  
| **`database/`** | ORM models (`Publication`, `UrlSource`), database operations (`service.py`). |  
| **`ml/`**      | Pretrained model (`model.pt`), tokenizer, inference logic.                   |  
| **`scraper/`** | Scraping logic (`scraper.py`), filters (`filter.py`), utilities (`utils.py`).|  
| **`server/`**  | gRPC service implementation, scheduler, Protobuf definitions.                |  
| **`test/`**    | Unit and integration tests.                                                  |  

---

## **Component Details**  

### **1. gRPC Server**  
**Purpose**: Serve publication data via gRPC with filtering and pagination.  
**Files**:  
- **`models_server.py`**: Implements `ModelServiceServicer` to handle `getPublications` requests.  
  - Methods: `get_all`, `get_last_week`, `get_today` (supports `page` and `amount` for pagination).  
- **`main_server.py`**: Starts the gRPC server and scheduler thread.  
- **`scheduler.py`**: Triggers periodic tasks (e.g., daily scraping).  

**Endpoints**:  
```proto  
service ModelService {  
  rpc getPublications(GetRequest) returns (stream Publication);  
}  
```  
**Request**:  
```python  
GetRequest(type="today", page=1, amount=10)  # type: today/week/month/all  
```  
**Response**: Stream of `Publication` Protobuf messages.  

---

### **2. Database**  
**Purpose**: Store scraped publications and task metadata.  
**Models**:  
- **`Publication`**: Title, URL, content, publication date, ML confidence (`prob`), status.  
- **`UrlSource`**: Source URLs (e.g., DOU).  
- **`ScheduleSettings`**: Scheduler intervals and last execution time.  

**Operations** (`service.py`):  
- `create_pub_from_do3()`: Saves scraped data after validation.  
- `get_publication_by_url()`: Checks for duplicates.  
- `update_schedule()`: Manages periodic tasks.  

---

### **3. Machine Learning (ML)**  
**Purpose**: Classify publications as relevant (`prob >= 0.70`) or irrelevant.  
**Files**:  
- **`model.py`**: Transformer-based model architecture.  
- **`inference.py`**: Tokenizes text and runs predictions.  
- **`llm_extraction.py`**: *Incomplete* – intended for metadata extraction using LLMs.  

**Workflow**:  
1. Scraped text → Tokenized → Padded to 350 tokens.  
2. Model predicts class probabilities → Updates `prob` field in the database.  

---

### **4. Scraper**  
**Purpose**: Collect and preprocess data from the DOU website.  
**Files**:  
- **`scraper.py`**: `SingleScrapper` class handles scraping for a single date.  
- **`filter.py`**: Applies `PRE_FILTERS` (e.g., `artType="aviso de licitação"`).  
- **`utils.py`**: Fetches JSON data and parses HTML content.  

**Status Tracking**:  
- `0`: Already exists.  
- `1`: Failed pre-filters.  
- `2`: Low ML confidence.  
- `3`: Saved successfully.  

---

## **Configuration** (`config.py`)  
| Key                        | Description                                  | Example Value              |  
|----------------------------|----------------------------------------------|----------------------------|  
| `DATABASE_URL`             | SQLite database path.                        | `./database/data/db.sqlite`|  
| `BASE_DOU3_URL`            | URL template for scraping.                   | `https://www.in.gov.br/...`|  
| `PROB_THRESHOLD`           | Minimum ML confidence to save publications.  | `0.70`                     |  
| `SCHEDULER_DEFAULT`        | Task intervals (e.g., daily scraping).       | `{'daily': 86400}`         |  
| `ML_MODEL_WEIGHTS_PATH`    | Path to pretrained model weights.            | `./ml/model.pt`            |  

---

## **Setup & Execution**  

### **Dependencies**  
```bash  
pip install grpcio peewee torch requests beautifulsoup4 protobuf  
```  

### **1. Compile Protobufs**  
```bash  
./compile_protos.bat  # Generates gRPC stubs in server/  
```  

### **2. Start Server**  
```bash  
python server/main_server.py  # Starts gRPC server on port 50051  
```  

### **3. Test Client**  
```bash  
python main_test_client.py  # Fetches sample data via gRPC  
```  

### **4. Run Scraper Manually**  
```python  
from scraper.scraper import SingleScrapper  
scrap = SingleScrapper("01-01-2023")  
scrap.filter()  
```  

---

## **Testing**  
- **Unit Tests**: Execute `pytest test/`.  
- **gRPC Tests**: Use `main_test_client.py` to validate server responses.  

---

## **Assumptions & Future Work**  
- **Unimplemented Features**:  
  - `ConfigService` (gRPC) for dynamic configuration.  
  - `llm_extraction.py` for metadata extraction.  
- **Improvements**:  
  - Add retries for failed HTTP requests.  
  - Parallelize scraping for multiple dates.  
  - Expand ML model to support multi-class classification.  
