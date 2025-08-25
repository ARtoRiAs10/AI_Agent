# memory.py
import chromadb
from chromadb.utils import embedding_functions
import os
import datetime
import json
import re

class MemoryManager:
    def __init__(self, collection_name="debate_memory"):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=embedding_functions.DefaultEmbeddingFunction()
        )
        self.transcript = []
        self.doc_counter = 0

    def add_to_memory(self, speaker, text):
        entry = f"{speaker}: {text}"
        self.transcript.append(entry)
        
        # Add to vector store for RAG
        self.collection.add(
            documents=[entry],
            ids=[f"doc_{self.doc_counter}"]
        )
        self.doc_counter += 1

    def retrieve_relevant_context(self, query, n_results=3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return "\n".join(results['documents'][0])

    def get_full_transcript(self):
        return "\n".join(self.transcript)

    # --- NEW METHOD TO SAVE THE TRANSCRIPT ---
    def save_transcript_to_file(self, topic, file_format='md'):
        """Saves the full debate transcript to a file."""
        
        # 1. Create a dedicated directory for transcripts if it doesn't exist
        output_dir = "transcripts"
        os.makedirs(output_dir, exist_ok=True)

        # 2. Create a safe filename from the topic and a timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        # Sanitize topic for filename: lowercase, replace spaces, remove unsafe chars
        safe_topic = re.sub(r'[^a-z0-9_]+', '', topic.lower().replace(' ', '_'))
        filename = f"debate_{safe_topic}_{timestamp}.{file_format}"
        filepath = os.path.join(output_dir, filename)

        # 3. Write the content based on the chosen format
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                if file_format == 'md':
                    f.write(f"# Debate Topic: {topic}\n\n")
                    for entry in self.transcript:
                        speaker, message = entry.split(":", 1)
                        f.write(f"**{speaker.strip()}:** {message.strip()}\n\n")
                
                elif file_format == 'json':
                    # Create a list of structured objects for JSON
                    json_data = []
                    for entry in self.transcript:
                        speaker, message = entry.split(":", 1)
                        json_data.append({"speaker": speaker.strip(), "message": message.strip()})
                    json.dump(json_data, f, indent=4)

                elif file_format == 'txt':
                    f.write(f"Debate Topic: {topic}\n\n")
                    f.write("\n".join(self.transcript))
                
                else:
                    print(f"Error: Unsupported file format '{file_format}'.")
                    return

            print(f"--- Transcript successfully saved to: {filepath} ---")

        except Exception as e:
            print(f"--- Error saving transcript: {e} ---")