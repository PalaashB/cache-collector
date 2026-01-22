# Semantic LLM Cache

This is a Python project where we built a simple semantic caching layer on top of a local LLM.  
The main idea is to avoid generating responses repeatedly for similar prompts by reusing past answers based on semantic similarity rather than exact text matching.

The project combines embeddings, cosine similarity, and a local database to speed up local LLM inference.

---

## What This Project Does

When a user enters a prompt:

• The prompt is converted into a vector embedding  
• The embedding is compared with previously stored embeddings in a SQLite database  
• If a semantically similar prompt already exists, the cached response is returned instantly  
• If no similar prompt is found, the LLM generates a new response  
• The new prompt, response, and embedding are then saved for future queries  

This reduces unnecessary computation and improves response time.

---

## Why We Built This

Running LLMs locally can be slow and expensive, even for smaller models like DistilGPT-2 (which is used in this project).  

Exact string based caching is not very effective because users rarely ask questions in the same way twice.

We built this project to explore how semantic embeddings can be used as a caching mechanism and to better understand how LLM inference, vector similarity, and persistent storage interact in practice.

This project was mainly built for learning and experimentation.

---

## Project Structure

### chat.py
This is the main entry point of the project.

• Loads the local DistilGPT-2 model and tokenizer  
• Loads the sentence embedding model  
• Runs an interactive user input loop  
• Checks the semantic cache before generating a response  
• Stores new prompt response pairs after generation  

### cache_db.py
This file handles storage and similarity logic.

• Creates and manages the SQLite database  
• Stores embeddings as binary blobs  
• Reconstructs vectors from the database  
• Computes cosine similarity  
• Performs semantic cache lookups  

---

## Models Used

• Language model: DistilGPT-2 (loaded locally)   

---

## How Semantic Matching Works

1. The user prompt is embedded using SentenceTransformer  
2. All stored embeddings are fetched from the database  
3. Cosine similarity is calculated between the new embedding and stored vectors  
4. If similarity is greater than 0.8, it is treated as a cache hit  
5. The corresponding response is returned  

The similarity search is implemented as a simple linear scan.

---

## Database Schema

SQLite table name: `cache`

Columns:

• prompt (primary key)  
• response  
• vect (embedding stored as bytes)  

---

## How to Run

1. Install required dependencies  
