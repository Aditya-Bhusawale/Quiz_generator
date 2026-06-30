
# 📚 RAG-Based AI Quiz Generator

An AI-powered Quiz Generator that creates **Multiple Choice Questions (MCQs)** from uploaded PDF documents using **Retrieval-Augmented Generation (RAG)**. The application retrieves only the most relevant content from the document before generating questions, resulting in accurate and context-aware quizzes.

---

## 🚀 Features

* 📄 Upload any PDF document
* ✂️ Automatically split documents into chunks
* 🧠 Generate vector embeddings using HuggingFace
* 💾 Store embeddings in Chroma Vector Database
* 🔍 Retrieve the most relevant content using semantic search
* 🤖 Generate high-quality MCQs using an LLM
* ✅ Four options (A, B, C, D) for every question
* 🎯 Exactly one correct answer for each question
* 📊 Structured quiz output using Pydantic
* 🎨 Clean and responsive web interface

---

## 🛠️ Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Flask
* Python

### AI & RAG

* LangChain
* HuggingFace Embeddings (`sentence-transformers/all-MiniLM-L6-v2`)
* ChromaDB
* PyPDFLoader
* RecursiveCharacterTextSplitter
* Groq LLM

### Data Validation

* Pydantic

---

## 📂 Project Structure

```text
AI-Quiz-Generator/
│
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
├── uploads/
├── chroma_db/
├── src/
│   ├── rag.py
│   ├── quiz_schema.py
│   ├── prompt.py
│   └── generator.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ How It Works

### 1. Upload PDF

The user uploads a PDF document.

↓

### 2. Load Document

The PDF is loaded using **PyPDFLoader**.

↓

### 3. Split Document

The document is divided into smaller chunks using **RecursiveCharacterTextSplitter**.

↓

### 4. Create Embeddings

Each chunk is converted into vector embeddings using

```
sentence-transformers/all-MiniLM-L6-v2
```

↓

### 5. Store in Chroma

The embeddings are stored in a unique Chroma collection.

↓

### 6. Retrieve Relevant Chunks

When quiz generation is requested, the retriever fetches the most relevant chunks based on semantic similarity.

↓

### 7. Generate Quiz

The retrieved context is sent to the LLM, which generates structured multiple-choice questions.

---

## 🧠 RAG Pipeline

```text
               PDF
                │
                ▼
         PyPDFLoader
                │
                ▼
   RecursiveCharacterTextSplitter
                │
                ▼
          Text Chunks
                │
                ▼
     HuggingFace Embeddings
                │
                ▼
      Chroma Vector Database
                │
                ▼
      Semantic Retriever (Top-K)
                │
                ▼
         Retrieved Context
                │
                ▼
             Groq LLM
                │
                ▼
         Structured Quiz Output
```

---

## 📋 Quiz Output Format

Each generated question follows this structure:

```python
Question(
    question="What is Python?",
    option_a="Snake",
    option_b="Programming Language",
    option_c="Database",
    option_d="Browser",
    answer="B"
)
```

The complete quiz is returned as:

```python
Quiz(
    questions=[
        Question(...),
        Question(...),
        ...
    ]
)
```

---

## ▶️ Installation

### Clone the repository

```bash
git clone https://github.com/your-username/AI-Quiz-Generator.git
```

```bash
cd AI-Quiz-Generator
```

### Create a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key
```

### Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 📌 Future Improvements

* Difficulty levels (Easy, Medium, Hard)
* True/False question generation
* Fill-in-the-blanks generation
* Support for DOCX and TXT files
* Export quizzes to PDF
* Timer-based quiz mode
* Student score analysis
* Question filtering by topic
* Multi-language quiz generation

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Aditya Gangadhar Bhusawale**

Computer Engineering Student | AI & Machine Learning Enthusiast
