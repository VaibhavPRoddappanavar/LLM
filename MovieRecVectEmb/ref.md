🧠 What is a Vector Search Index?
A vector search index is a special kind of index that allows fast similarity search over high-dimensional numeric vectors — like the embeddings you've generated from movie plots or titles.

🎯 Why Do We Need It?
When you convert text into embeddings (like with Sentence Transformers), each piece of text becomes a vector — a list of numbers (e.g., 384 floats). To find similar items (e.g., similar movies), you compute the distance (like cosine similarity) between these vectors.

But if you have thousands or millions of vectors, comparing every one of them manually becomes slow.

⚡ That's where a vector search index comes in — it speeds up this search using smart data structures like HNSW (Hierarchical Navigable Small World graphs).




