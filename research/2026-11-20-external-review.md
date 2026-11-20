# External review evidence — 2026-11-20

The improvement pass is grounded in these primary sources:

- Python `os` documentation: `os.fsync()` requires flushing buffered file objects first; `os.replace()` replaces a destination file atomically on POSIX when the operation succeeds, and source and destination must be on the same filesystem. https://docs.python.org/3/library/os.html
- OWASP Race Conditions: check-then-use filesystem patterns create TOCTOU windows; the recommended direction is to avoid separate existence checks and use atomic operations or file-descriptor-based operations. https://community.owasp.org/pages/vulnerabilities/race_conditions
- OWASP Path Traversal: path handling must prevent traversal outside the intended root and must not rely on unsafe path interpretation. https://owasp.org/www-community/attacks/Path_Traversal
- JSON Schema Specification: the current specification is Draft 2020-12 and is split into Core and Validation vocabularies; schema validation must be tied to the declared dialect. https://json-schema.org/specification
- Mermaid documentation and CLI project: Mermaid syntax is parser/renderer-defined, and the CLI converts Mermaid definitions to SVG/PNG/PDF; successful rendering is syntax/tool evidence, not semantic architecture approval. https://mermaid.js.org/intro/syntax-reference.html and https://github.com/mermaid-js/mermaid-cli

Decision: retain atomic replacement plus directory fsync, add regression coverage for concurrent/path-sensitive behavior where practical, require explicit schema dialect handling, and report parser/render results separately from semantic and owner gates. Do not infer architecture, security, finance, or operational approvals from these sources.
