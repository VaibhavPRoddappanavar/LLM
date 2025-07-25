import os
from dotenv import load_dotenv
import pymongo
import requests
from sentence_transformers import SentenceTransformer
import time

load_dotenv()
mongodb_url = os.getenv("MONGODB_URL")

client = pymongo.MongoClient(mongodb_url)
db=client.sample_mflix
collection = db.movies

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Function to get embedding for a movie
def get_movie_embedding(title, plot):
    text = f"{title}. {plot if plot else ''}"
    embedding = model.encode([text])[0]  # Get the embedding for the movie
    return embedding.tolist()  # Convert numpy array to list for MongoDB storage

def process_batch(limit=100):
    """Process a batch of movies without embeddings"""
    batch = list(collection.find(
        {"vector_embedding": {"$exists": False}}
    ).limit(limit))
    
    processed = 0
    errors = 0
    start_time = time.time()
    
    for movie in batch:
        try:
            title = movie.get('title', '')
            plot = movie.get('plot', '')
            
            if title:
                embedding = get_movie_embedding(title, plot)
                collection.update_one(
                    {'_id': movie['_id']},
                    {'$set': {
                        'vector_embedding': embedding
                    }}
                )
                processed += 1
                
        except Exception as e:
            print(f"❌ Error processing movie {title}: {str(e)}")
            errors += 1
    
    duration = time.time() - start_time
    return processed, errors, duration

# Get counts for progress tracking
total_docs = collection.count_documents({})
processed_docs = collection.count_documents({"vector_embedding": {"$exists": True}})
remaining_docs = total_docs - processed_docs

print(f"📊 Database Status:")
print(f"Total movies: {total_docs:,}")
print(f"Already processed: {processed_docs:,}")
print(f"Remaining to process: {remaining_docs:,}\n")

# Process in batches until done
batch_size = 100
total_processed = 0
total_errors = 0
total_time = 0

while True:
    processed, errors, duration = process_batch(batch_size)
    if processed == 0:
        break
        
    total_processed += processed
    total_errors += errors
    total_time += duration
    
    # Calculate progress and speed
    progress = (processed_docs + total_processed) / total_docs * 100
    speed = processed / duration if duration > 0 else 0
    
    print(f"⏳ Batch Progress:")
    print(f"Processed: {processed} movies in {duration:.1f}s ({speed:.1f} movies/s)")
    print(f"Total Progress: {progress:.1f}% ({processed_docs + total_processed:,}/{total_docs:,})")
    print(f"Errors: {errors}\n")

# Final statistics
print("\n✅ Processing Complete!")
print(f"Total new embeddings: {total_processed:,}")
print(f"Total errors: {total_errors}")
print(f"Total processing time: {total_time:.1f}s")
print(f"Average speed: {total_processed/total_time:.1f} movies/s")

# Verify recent updates with more details
print("\n🔍 Verifying Recent Updates...")
recent_updates = list(collection.find(
    {'vector_embedding': {'$exists': True}}
).sort([('embedding_timestamp', -1)]).limit(3))

for movie in recent_updates:
    print(f"Title: {movie['title']}")
    print(f"Embedding Size: {len(movie['vector_embedding'])} dimensions")
    print(f"Model Used: {movie.get('embedding_model', 'unknown')}")
    if 'embedding_timestamp' in movie:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', 
                                time.localtime(movie['embedding_timestamp']))
        print(f"Generated: {timestamp}")
    print()