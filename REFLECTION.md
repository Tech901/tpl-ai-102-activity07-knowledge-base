# Reflection -- Neighborhood Knowledge Base

Answer these questions after completing the activity (2-3 sentences each).

## 1. Chunking Strategy
How did your chunk size and overlap settings affect retrieval quality? What tradeoffs did you observe?

## 2. RAG Quality
Which evaluation metric (faithfulness, relevance, groundedness) was hardest to improve? Why?

## 3. Adversarial Defense
How does your grounding prompt prevent the model from answering questions outside the knowledge base? What attack patterns were most challenging?

## 4. Cost Awareness
Based on your cost tracking, what would you estimate the monthly cost of running this RAG pipeline for 1,000 daily queries?

## 5. RAG vs Keyword Search
When would a simple keyword search (BM25) be sufficient, and when does the full RAG pipeline (embed, retrieve, generate) add value? Consider factors like corpus size, query complexity, and user expectations.

## 6. Corpus Size and Retrieval Quality
How might retrieval quality change if your corpus grew from 20 documents to 2,000? What architectural changes would you need to make to the chunking, indexing, and retrieval steps?
