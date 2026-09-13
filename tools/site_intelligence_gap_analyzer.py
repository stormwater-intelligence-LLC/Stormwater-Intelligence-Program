#!/usr/bin/env python3
"""Site Intelligence Gap Analyzer.

Reviews a JSON description of site/project data and identifies information gaps
that may prevent a defensible stormwater or BMP analysis.

This tool is analytical only. It does not determine permit compliance and does
not replace QSD/QSP professional judgment.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


@dataclass(frozen=True)
class Requirement:
    key: str
    label: str
    critical: bool
    verify_when_present: bool
    next_action: str


REQUIREMENTS: List[Requirement] = [
    Requirement("site_boundary", "Site boundary / project footprint", True, True, "Confirm the current project limits and coordinate reference."),
    Requirement("terrain_elevation", "Terrain / elevation surface", True, True, "Obtain or validate a terrain/elevation surface suitable for drainage analysis."),
    Requirement("slope", "Slope information", True, True, "Derive slope from validated terrain or provide design-grade slope data."),
    Requirement("drainage_paths", "Drainage pathways / flow direction", True, True, "Trace and verify surface flow paths, concentrated flow, and discharge points."),
    Requirement("receiving_water", "Receiving water / downstream connection", True, True, "Identify and verify the receiving water or downstream drainage connection."),
    Requirement("storm_input", "Storm / precipitation input", True, True, "Select and document the storm input used for the analysis."),
    Requirement("disturbed_area", "Disturbed area", True, True, "Quantify the currently disturbed area using current plans or mapped limits."),
    Requirement("impervious_area", "Impervious area", False, True, "Quantify impervious surfaces relevant to runoff generation."),
    Requirement("soil_infiltration", "Soil / infiltration information", True, True, "Obtain field, design, or authoritative soil/infiltration information before infiltration-dependent analysis."),
    Requirement("storm_drain_infrastructure", "On-site storm-drain infrastructure", True, True, "Map inlets, pipes, culverts, outlets, and known conveyance structures."),
    Requirement("grading_surface", "Grading / design surface", False, True, "Obtain the latest grading/design surface where proposed conditions matter."),
    Requirement("bmp_inventory", "Existing / proposed BMP inventory", True, True, "Identify BMP type, location, status, and intended function."),
    Requirement("bmp_dimensions_capacity", "BMP dimensions / capacity", True, True, "Provide dimensions, storage, flow capacity, or other design parameters needed for evaluation."),
    Requirement("access_constructability", "Access / constructability constraints", False, True, "Document access, equipment, staging, utility, and physical constraints."),
    Requirement("maintenance_constraints", "Maintenance constraints", False, True, "Document inspection, sediment removal, replacement, and access requirements."),
    Requirement("project_design_criteria", "Project-specific design criteria", True, True, "Provide the project criteria the BMP analysis must satisfy."),
    Requirement("regulatory_context", "Applicable permit / regulatory context", True, True, "Identify the controlling permit/order and project-specific applicability before compliance conclusions."),
]


def _present(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) > 0
    return True


def _verified(value: Any) -> bool:
    if isinstance(value, dict):
        return value.get("verified") is True
    return False


def analyze(site: Dict[str, Any]) -> Dict[str, Any]:
    available: List[Dict[str, Any]] = []
    missing: List[Dict[str, Any]] = []
    verify: List[Dict[str, Any]] = []
    blockers: List[Dict[str, Any]] = []
    actions: List[str] = []

    earned = 0.0
    possible = 0.0

    for req in REQUIREMENTS:
        weight = 2.0 if req.critical else 1.0
        possible += weight
        value = site.get(req.key)

        if not _present(value):
            entry = {"key": req.key, "label": req.label, "critical": req.critical}
            missing.append(entry)
            actions.append(req.next_action)
            if req.critical:
                blockers.append(entry)
            continue

        available.append({"key": req.key, "label": req.label, "critical": req.critical})
        earned += weight

        if req.verify_when_present and not _verified(value):
            verify.append({
                "key": req.key,
                "label": req.label,
                "reason": "Present but not explicitly marked verified.",
            })

    readiness = round((earned / possible) * 100, 1) if possible else 0.0

    if blockers:
        classification = "BLOCKED"
    elif verify:
        classification = "CONDITIONAL"
    else:
        classification = "READY_FOR_ANALYTICAL_REVIEW"

    return {
        "tool": "Stormwater Intelligence Site Intelligence Gap Analyzer",
        "status": classification,
        "readiness_score_percent": readiness,
        "summary": {
            "available_count": len(available),
            "missing_count": len(missing),
            "verification_count": len(verify),
            "critical_blocker_count": len(blockers),
        },
        "available_inputs": available,
        "missing_inputs": missing,
        "verification_items": verify,
        "critical_blockers": blockers,
        "recommended_next_actions": list(dict.fromkeys(actions)),
        "limitations": [
            "This output is an analytical readiness screen, not a permit-compliance determination.",
            "A present data field may still be unsuitable because of age, scale, accuracy, provenance, or project mismatch.",
            "Regulatory conclusions require review of the controlling permit/order and applicable project-specific requirements.",
            "QSD/QSP or other qualified professional judgment may still be required.",
        ],
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python tools/site_intelligence_gap_analyzer.py <site.json>", file=sys.stderr)
        return 2

    input_path = Path(sys.argv[1])
    try:
        site = json.loads(input_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        print(f"Unable to read input JSON: {exc}", file=sys.stderr)
        return 1

    report = analyze(site)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
