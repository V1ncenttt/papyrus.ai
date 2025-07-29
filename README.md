# 🧠 ScholarMind

> AI-powered academic assistant that lets you **chat with your papers** — figures included.

ScholarMind is a multimodal research tool that allows users to upload PDFs and ask natural language questions about their academic documents. It leverages **Mistral OCR**, **BLIP-2**, **LangChain**, and **LangGraph** to extract, understand, and retrieve both **text** and **figure-based insights** from papers.

## 🎯 Features

- 📄 Upload PDFs with structured metadata (BibTeX, author, title, etc.)
- 🔎 Extract both text and figures using **Mistral OCR**
- 🧠 Generate semantic descriptions of figures with **BLIP-2** or **GPT-4V**
- 📚 Embed everything into a **vector database** (Chroma or Qdrant)
- 🤖 Ask open-ended questions and receive context-aware answers powered by **LangChain + LangGraph**
- 🧵 Maintains conversational memory with dynamic branching (text vs figure answers)
- ⚡ Live token streaming with a FastAPI backend + React frontend

---

## 🧱 Architecture

```mermaid
graph LR
    A[PDF Upload] --> B[Mistral OCR (text + figures)]
    B --> C1[Text Chunks]
    B --> C2[Figure Captions + Images]
    C2 --> D1[BLIP-2 Description]
    C1 --> E[Embedding]
    D1 --> E
    E --> F[Vector DB]
    G[User Query] --> H[LangGraph DAG]
    H --> I[LangChain Retriever]
    I --> F
    I --> J[LLM Answer]
    J --> K[Frontend (Streaming)]
```
