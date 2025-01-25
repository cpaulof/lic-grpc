#Lic gRPC
A backend system for scraping, processing, and serving legal/publication data from official sources like Brazil's DOU (Diário Oficial da União).

---

## ✨ Key Features
- **Automated Scraping**: Collect data from predefined government portals
- **ML Filtering**: Transformer-based model to flag relevant publications
- **gRPC API**: Serve filtered data with pagination and time-based queries
- **SQLite Storage**: Persistent storage for publications and metadata
- **Scheduled Tasks**: Daily auto-scraping via configurable scheduler

---

## 🛠 Technologies
- **gRPC** (Protocol Buffers)
- **SQLite** + **Peewee ORM**
- **PyTorch** (Transformer model)
- **BeautifulSoup** (HTML parsing)

---

## ⚙️ Quick Start

### Prerequisites
- Python 3.10+
- `requirements.txt` dependencies

```bash
# Install dependencies
pip install -r requirements.txt

# Compile Protobuf definitions
./compile_protos.bat

# Start server
python server/main_server.py

# Test client (in separate terminal)
python main_test_client.py
```

---

## 📚 Documentation
| Language      | Link                              |
|---------------|-----------------------------------|
| English       | [Full Documentation](DOC.md)     |
| Portuguese    | [Documentação Completa](DOC-PT_BR.md) |

---

## 📂 Project Structure
```
licscrap/
├── database/       # DB models & operations
├── ml/             # ML model & inference
├── scraper/        # Web scraping components
├── server/         # gRPC server implementation
└── tests/          # Unit/integration tests
```

---

## 🌟 Key Workflow
1. **Scraper** collects raw data → **ML Model** filters by relevance
2. **Database** stores processed publications
3. **gRPC Server** serves filtered results to clients
4. **Scheduler** triggers daily auto-scraping

