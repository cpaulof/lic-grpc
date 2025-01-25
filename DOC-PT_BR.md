## **Visão Geral do Projeto**  
Este é um **sistema backend em Python** projetado para coletar, processar, armazenar e servir dados estruturados de publicações (e.g., editais, artigos) de fontes como o Diário Oficial da União (DOU). Ele integra:  
- **Web Scraping**: Coleta dados brutos de URLs especificadas.  
- **Machine Learning (ML)**: Filtra publicações por relevância usando um modelo baseado em transformers.  
- **API gRPC**: Disponibiliza dados filtrados para clientes com paginação e consultas por período.  
- **Banco de Dados SQLite**: Armazena publicações e metadados de tarefas.  
- **Agendador**: Automatiza tarefas periódicas (e.g., coleta diária de dados).  

---

## **Arquitetura do Sistema**  
```  
┌──────────────┐       ┌──────────────────┐       ┌───────────────┐  
│   Scraper    │──────▶│ Banco de Dados   │──────▶│ Servidor gRPC │  
└──────────────┘       └──────────────────┘       └───────────────┘  
       │                       ▲                       │  
       │ Filtragem por ML      │ Agendador             │ Cliente  
       ▼                       │                       ▼  
┌──────────────┐       ┌──────────────────┐       ┌───────────────┐  
│ Modelo de ML │       │   Configuração   │       │ Cliente gRPC  │  
└──────────────┘       └──────────────────┘       └───────────────┘  
```  

---

## **Estrutura de Diretórios**  
| Diretório      | Componentes Principais                                                      |  
|----------------|-----------------------------------------------------------------------------|  
| **`database/`** | Modelos ORM (`Publication`, `UrlSource`), operações de banco (`service.py`). |  
| **`ml/`**      | Modelo pré-treinado (`model.pt`), tokenizador, lógica de inferência.        |  
| **`scraper/`** | Lógica de scraping (`scraper.py`), filtros (`filter.py`), utilitários (`utils.py`). |  
| **`server/`**  | Implementação do serviço gRPC, agendador, definições Protobuf.              |  
| **`test/`**    | Testes unitários e de integração.                                           |  

---

## **Detalhes dos Componentes**  

### **1. Servidor gRPC**  
**Objetivo**: Servir dados de publicações via gRPC com filtragem e paginação.  
**Arquivos**:  
- **`models_server.py`**: Implementa `ModelServiceServicer` para lidar com requisições `getPublications`.  
  - Métodos: `get_all`, `get_last_week`, `get_today` (suportam `page` e `amount` para paginação).  
- **`main_server.py`**: Inicia o servidor gRPC e a thread do agendador.  
- **`scheduler.py`**: Dispara tarefas periódicas (e.g., coleta diária).  

**Endpoints**:  
```proto  
service ModelService {  
  rpc getPublications(GetRequest) returns (stream Publication);  
}  
```  
**Requisição**:  
```python  
GetRequest(type="today", page=1, amount=10)  # type: today/week/month/all  
```  
**Resposta**: Fluxo de mensagens Protobuf do tipo `Publication`.  

---

### **2. Banco de Dados**  
**Objetivo**: Armazenar publicações coletadas e metadados de tarefas.  
**Modelos**:  
- **`Publication`**: Título, URL, conteúdo, data de publicação, confiança do ML (`prob`), status.  
- **`UrlSource`**: URLs de origem (e.g., DOU).  
- **`ScheduleSettings`**: Intervalos do agendador e última execução.  

**Operações** (`service.py`):  
- `create_pub_from_do3()`: Salva dados coletados após validação.  
- `get_publication_by_url()`: Verifica duplicatas.  
- `update_schedule()`: Gerencia tarefas periódicas.  

---

### **3. Machine Learning (ML)**  
**Objetivo**: Classificar publicações como relevantes (`prob >= 0.70`) ou irrelevantes.  
**Arquivos**:  
- **`model.py`**: Arquitetura do modelo baseada em transformers.  
- **`inference.py`**: Tokeniza texto e executa previsões.  
- **`llm_extraction.py`**: *Incompleto* – destinado à extração de metadados com LLMs.  

**Fluxo**:  
1. Texto coletado → Tokenizado → Ajustado para 350 tokens.  
2. Modelo prevê probabilidades → Atualiza campo `prob` no banco de dados.  

---

### **4. Scraper**  
**Objetivo**: Coletar e pré-processar dados do site do DOU.  
**Arquivos**:  
- **`scraper.py`**: Classe `SingleScrapper` gerencia a coleta para uma data específica.  
- **`filter.py`**: Aplica `PRE_FILTERS` (e.g., `artType="aviso de licitação"`).  
- **`utils.py`**: Busca dados JSON e processa conteúdo HTML.  

**Status de Publicação**:  
- `0`: Já existe no banco.  
- `1`: Falhou nos pré-filtros.  
- `2`: Baixa confiança do ML.  
- `3`: Salvo com sucesso.  

---

## **Configuração** (`config.py`)  
| Chave                      | Descrição                                  | Exemplo de Valor         |  
|----------------------------|--------------------------------------------|--------------------------|  
| `DATABASE_URL`             | Caminho do banco SQLite.                   | `./database/data/db.sqlite`|  
| `BASE_DOU3_URL`            | Template de URL para coleta.               | `https://www.in.gov.br/...`|  
| `PROB_THRESHOLD`           | Confiança mínima do ML para salvar.        | `0.70`                   |  
| `SCHEDULER_DEFAULT`        | Intervalos de tarefas (e.g., coleta diária). | `{'daily': 86400}`       |  
| `ML_MODEL_WEIGHTS_PATH`    | Caminho dos pesos do modelo pré-treinado.  | `./ml/model.pt`          |  

---

## **Configuração & Execução**  

### **Dependências**  
```bash  
pip install grpcio peewee torch requests beautifulsoup4 protobuf  
```  

### **1. Compilar Protobufs**  
```bash  
./compile_protos.bat  # Gera stubs gRPC em server/  
```  

### **2. Iniciar Servidor**  
```bash  
python server/main_server.py  # Inicia servidor gRPC na porta 50051  
```  

### **3. Testar Cliente**  
```bash  
python main_test_client.py  # Busca dados de exemplo via gRPC  
```  

### **4. Executar Scraper Manualmente**  
```python  
from scraper.scraper import SingleScrapper  
scrap = SingleScrapper("01-01-2023")  
scrap.filter()  
```  

---

## **Testes**  
- **Testes Unitários**: Execute `pytest test/`.  
- **Testes gRPC**: Use `main_test_client.py` para validar respostas do servidor.  

---

## **Suposições & Trabalhos Futuros**  
- **Funcionalidades Não Implementadas**:  
  - `ConfigService` (gRPC) para configuração dinâmica.  
  - `llm_extraction.py` para extração de metadados.  
- **Melhorias Propostas**:  
  - Adicionar retentativas para falhas em requisições HTTP.  
  - Paralelizar coleta para múltiplas datas.  
  - Expandir modelo de ML para classificação multiclasse.  
