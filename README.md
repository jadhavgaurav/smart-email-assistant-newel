# 📬 Smart Email Assistant using ML, GenAI, and Agents

An end-to-end AI-powered assistant that classifies incoming emails, generates automatic responses using an open-source LLM, and escalates low-confidence queries for human review. Built using Python, Streamlit, Ollama (LLM), and Docker.

---

## 🚀 Features

- 📂 **Email Classification Agent (ML)** – Logistic Regression model trained to classify emails into HR, IT, or Other.
- 🤖 **Response Agent (LLM)** – Uses a local LLM via Ollama (LLaMA3 8B) to generate context-aware replies.
- ⚠️ **Escalation Agent** – Triggers if classification confidence is low or ambiguous.
- 🌐 **Streamlit UI** – Interactive web app for testing and managing emails.
- 📊 **Logging** – Saves every interaction and optionally uploads to AWS S3.
- 🐳 **Dockerized** – Fully containerized for local or cloud deployment.

---

```markdown
## 🧠 Agentic Workflow

```mermaid
graph TD
    A[Incoming Email] --> B[Email Classifier (ML)]
    B --> C{Confidence >= 0.6 and Category ≠ Other?}
    C -->|Yes| D[LLM Response Generator]
    C -->|No| E[Escalation Agent]
    D --> F[Return Response]
    E --> F
```
---

## 📦 Folder Structure

```
smart-email-assistant/
├── app/
│   ├── agents/
│   │   ├── email_classifier.py
│   │   ├── response_generator.py / crewai_response_agent.py
│   │   └── escalation_agent.py
│   ├── orchestrator.py
│   └── streamlit_ui.py
├── data/
│   └── emails.csv
├── notebooks/
│   └── data_cleaning.ipynb
├── logs/
│   └── history.csv
├── models/
│   └── model.pkl
├── Dockerfile
├── pyproject.toml
├── poetry.lock
├── requirements.txt
└── README.md
```

---

## 📊 ML Model Details

- Model: `RandomForestClassifier`
- Dataset: 900+
- Classes: HR, IT, Other
- Metrics:
  - Accuracy: ~94%
  - Confusion Matrix & classification report included in notebook
- Confidence Threshold: `0.6`

---

## 🤖 LLM Integration (Ollama)

- Model: `llama3:8b-instruct-q4_K_M`
- Backend: `Ollama` running on `localhost:11434`
- Framework: `LangChain + langchain-ollama`
- Base Prompt per category:
  - HR: "You are an HR assistant. Reply professionally..."
  - IT: "You are an IT assistant. Help with this issue..."

---

## 🌐 Streamlit UI

### Features
- Input email content
- Shows classification, confidence, action
- Returns LLM-generated reply or escalation
- Logs all results to CSV (and optionally uploads to S3)

### Run Locally
```bash
poetry install
poetry run streamlit run app/streamlit_ui.py
```

### Run with Docker
```bash
docker pull jadhavgaurav007/smart-email-assistant
docker run -p 8501:8501 jadhavgaurav007/smart-email-assistant
```
> Make sure `ollama serve` is running on host

---

## 🐳 Docker Deployment

### Build Locally
```bash
docker build -t smart-email-assistant .
```

### Tag & Push
```bash
docker tag smart-email-assistant jadhavgaurav007/smart-email-assistant
docker push jadhavgaurav007/smart-email-assistant
```

---

## 💡 Author
**Gaurav Vijay Jadhav**  
AI Engineer | Thane, Maharashtra  
📧 gaurav.vjadhav01@gmail.com