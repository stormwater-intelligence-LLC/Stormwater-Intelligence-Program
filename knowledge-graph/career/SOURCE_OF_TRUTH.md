# Career Knowledge Graph — Single Source of Truth

**Status: CANONICAL**

**Authoritative file:** `career_unified_knowledge_graph_v3.json`
**SHA-256:** `622cd3cc53e06688d11ba5aa55358c189aa862423e34e7c7e14e4120e3af2658`

## Governance
- Version 3 JSON is the only authoritative record for the professional knowledge graph.
- The interactive viewer (`.html`) and 3D geometry (`.glb`) are derivative presentation artifacts, not separate data authorities.
- Version 1 and Version 2 are historical references, **ARCHIVED / NON-AUTHORITATIVE**. They must not be used as current source data.
- All changes begin in the canonical JSON. Then regenerate and verify all derivatives before publishing a new package.
- This is a professional knowledge graph, not a verified live runtime architecture. No changes were made to Stormwater Intelligence.

## Graph
- 24 nodes
- 22 directed semantic relationships
- 23 category edges

## Consistency note
This update establishes authority and packaging, but does not independently prove the existing viewer and GLB can be regenerated deterministically from the JSON. Existing viewer and GLB are preserved as supplied, pending a renderer rebuild/validation.