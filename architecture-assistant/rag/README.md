# Local Retrieval-Augmented Generation (RAG) evidence layer

This repository includes a working local retrieval layer, not a hosted embedding service. It ingests Markdown, text and JSON; splits records into bounded chunks; indexes tokens; and ranks results with BM25. It works offline, has no third-party dependencies, supports English and Arabic token matching, and returns source paths/chunk citations. It is a retrieval/evidence subsystem, not a generative model. An agent/LLM should use returned evidence with citations and state when nothing relevant is retrieved.

## Use
From the assistant directory:

```bash
python3 rag/cli.py index examples/sample-system --output .rag/sample-index.json
python3 rag/cli.py search 'carrier booking idempotency' --index .rag/sample-index.json -k 5
```

Index each target system separately to avoid cross-project knowledge leakage. Rebuild after changes. Do not index secrets, credentials, or information the current task is not authorized to use. Ignore stale/generated reports where appropriate by selecting a narrower source folder. The index includes the source root and text; protect it like the source documentation.

## Retrieval limitations
BM25 is lexical, not semantic embedding search; synonyms and conceptual paraphrases may be missed. The current adapter is intentionally replaceable. To add embeddings, implement an alternate indexer/ranker behind this interface, version the index format, preserve source metadata, and rerun retrieval tests. No LLM call or cloud data transfer occurs here.
