import os
from dotenv import load_dotenv
import pymongo
from sentence_transformers import SentenceTransformer
import time

# Load environment variables and setup MongoDB connection
load_dotenv()
mongodb_url = os.getenv("MONGODB_URL")
client = pymongo.MongoClient(mongodb_url)
db = client.sample_mflix
collection = db.movies

# Initialize the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def get_movie_recommendations(query_text, num_results=5):
    """
    Get movie recommendations based on text similarity
    """
    # Generate embedding for the query text
    query_embedding = model.encode([query_text])[0].tolist()
    
    # Perform vector search
    pipeline = [
        {
            "$vectorSearch": {
                "index": "vector_index",  # The name of your vector index
                "path": "vector_embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,     # Internal limit for similarity search
                "limit": num_results      # Number of results to return
            }
        },
        {
            "$project": {
                "title": 1,
                "plot": 1,
                "year": 1,
                "score": {"$meta": "vectorSearchScore"}  # Get similarity score
            }
        }
    ]
    
    results = list(collection.aggregate(pipeline))
    return results

def main():
    print("🎬 Movie Recommendation System")
    print("Enter a description or keywords to find similar movies")
    print("Type 'quit' to exit\n")
    
    while True:
        # Get user input
        query = input("\n🔍 Enter your search: ").strip()
        if query.lower() == 'quit':
            break
            
        if not query:
            print("Please enter a search query")
            continue
            
        print("\nSearching for similar movies...")
        start_time = time.time()
        
        try:
            # Get recommendations
            results = get_movie_recommendations(query, num_results=5)
            
            # Display results
            duration = time.time() - start_time
            print(f"\n✨ Found {len(results)} matches in {duration:.2f} seconds:\n")
            
            for i, movie in enumerate(results, 1):
                score = movie.get('score', 0)
                similarity = (1 - score) * 100  # Convert cosine distance to similarity percentage
                
                print(f"{i}. {movie['title']} ({movie.get('year', 'N/A')})")
                print(f"   Similarity: {similarity:.1f}%")
                if movie.get('plot'):
                    print(f"   Plot: {movie['plot'][:200]}...")
                print()
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            
        print("\n" + "-"*50)

if __name__ == "__main__":
    main()