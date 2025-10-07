from llama_index.embeddings.ollama import OllamaEmbedding

ollama_embedding = OllamaEmbedding(
    model_name="embeddinggemma",
    base_url="http://localhost:11434",
    # Can optionally pass additional kwargs to ollama
    # ollama_additional_kwargs={"mirostat": 0},
)

embeddings = ollama_embedding.get_text_embedding_batch(
    ["This is a passage!", "This is another passage"], show_progress=True
)
print(f"Got vectors of length {len(embeddings[0])}")
print(embeddings[0][:10])