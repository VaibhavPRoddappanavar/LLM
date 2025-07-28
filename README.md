# 🎬 Vector-Based Movie Recommendation System

A sophisticated movie recommendation engine that leverages vector embeddings and semantic search to find similar movies based on natural language queries. Built with MongoDB Atlas Vector Search and BERT-based Sentence Transformers.

## 🌟 Key Features

- **Natural Language Search**: Find movies using conversational queries
- **Semantic Understanding**: Discovers movies based on meaning, not just keywords
- **Vector Embeddings**: Powered by BERT-based embeddings (all-MiniLM-L6-v2)
- **Efficient Search**: MongoDB Atlas Vector Search for fast similarity matching
- **Rich Results**: Displays titles, years, plots, and similarity scores

## 🛠️ Tech Stack

- Python 3.x
- MongoDB Atlas with Vector Search
- Sentence Transformers
- PyMongo
- python-dotenv

## 📋 Prerequisites

1. MongoDB Atlas account with Vector Search enabled
2. Python 3.x installed
3. MongoDB connection string
4. Required Python packages

## ⚙️ Setup & Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd MovieRecVectEmb
```

2. **Install dependencies**
```bash
pip install pymongo sentence-transformers python-dotenv
```

3. **Configure environment**
Create `.env` file:
```
MONGODB_URL=your_mongodb_connection_string
```

4. **Create MongoDB Vector Index**
```json
{
  "fields": [{
    "type": "vector",
    "path": "vector_embedding",
    "numDimensions": 384,
    "similarity": "cosine"
  }]
}
```

## 🚀 Usage

1. **Generate Movie Embeddings**
```bash
python movie_recs.py
```

2. **Search Movies**
```bash
python movieSearchprog.py
```

Example queries:
- "Science fiction movie about time travel"
- "Romantic comedy with mistaken identity"
- "Adventure in space with aliens"

## 📝 Sample Output

```
🎬 Movie Recommendation System
Enter a description or keywords to find similar movies

🔍 Enter your search: time travel adventure with robots

✨ Found 5 matches in 0.25 seconds:

1. Back to the Future (1985)
   Similarity: 92.5%
   Plot: Marty McFly, a 17-year-old high school student, is accidentally sent thirty years into the past...
```

## 📂 Project Structure

```
MovieRecVectEmb/
├── movie_recs.py      # Embedding generation script
├── movieSearchprog.py  # Search interface
├── .env               # Environment configuration
└── README.md         # Documentation
```


---
Developed with ❤️ by Vaibhav P Roddappanavar
