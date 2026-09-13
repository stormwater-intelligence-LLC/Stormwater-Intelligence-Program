# Stormwater Intelligence Program

**Role:** Private experimental and analytical utility development  
**StormAI Use:** SUPPORTING TOOL — EXPLICIT INVOCATION ONLY  
**Source Status:** SUPPORTING

This repository contains private analytical utilities for Stormwater Intelligence.

Tools in this repository are not regulatory authorities, policies, SOPs, or autonomous system permissions. They may support analysis when explicitly invoked, but controlling regulatory sources, ARCSEC, approved policies, SOPs, skills, and workflows remain authoritative.

## Site Intelligence Gap Analyzer

The first utility in this repository identifies what site information is available, what is missing, what still requires verification, and what gaps could block defensible stormwater/BMP analysis.

It intentionally does **not** determine permit compliance or replace QSD/QSP professional judgment.

### Run

```bash
python tools/site_intelligence_gap_analyzer.py examples/site_input.json
```

### Output

The tool returns structured JSON containing:

- readiness score
- available inputs
- missing inputs
- verification items
- blockers
- recommended next actions
