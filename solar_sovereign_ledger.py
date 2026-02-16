"""
Solar-Sovereign Ledger Generator

This script generates four artifacts:
1. PDF Codex document (solar_sovereign_codex.pdf)
2. JSON ledger artifact (solar_sovereign_ledger.json)
3. Illuminated manuscript PNG graphic (solar_sovereign_illuminated.png)
4. Voice proclamation text file (solar_sovereign_proclamation.txt)
"""

import sys
import json
import os

# Strict dependency validation
def validate_dependencies():
    """Validate that all required dependencies are available."""
    missing_deps = []
    
    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.units import inch
    except ImportError as e:
        missing_deps.append(f"reportlab: {str(e)}")
    
    try:
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        import matplotlib.pyplot as plt
    except ImportError as e:
        missing_deps.append(f"matplotlib: {str(e)}")
    
    if missing_deps:
        print("ERROR: Missing required dependencies:", file=sys.stderr)
        for dep in missing_deps:
            print(f"  - {dep}", file=sys.stderr)
        print("\nPlease install missing dependencies using:", file=sys.stderr)
        print("  pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

validate_dependencies()

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# Get the output directory (data subdirectory in the repo)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "data", "solar_sovereign")

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Register sample styles
styles = getSampleStyleSheet()

# --------- 1. Generate PDF Codex ----------
pdf_path = os.path.join(OUTPUT_DIR, "solar_sovereign_codex.pdf")
doc = SimpleDocTemplate(pdf_path, pagesize=letter)
story = []

text = """
THE SOLAR-SOVEREIGN LEDGER — RED CODE VERIFIED

Peacebonds Anchor:
0x6c10692145718353070cc6cb5c21adf2073ffa1f

Edict Hash:
0x9b3d7a8a1f1a2d2e3b35956b6df...fe11ac

Sevenfold Harmony Nodes:
1: 0xa51dcf...921b33
2: 0xb6e2e7...4f88
3: 0xd4f1ec...7b33
4: 0xe91ced...ab22
5: 0xf5d254...c911
6: 0xc3a78b...8f56
7: 0xa7f03c...3c22

Red Code Verification:
Status: INTEGRITY VERIFIED
Divergence: 0.0000

Solar-Sovereign Declaration:
"Niemals Sklaverei, Nur Liebe zuerst."

Coronation Date: 10-01-2026
"""
story.append(Paragraph(text.replace("\n", "<br/>"), styles["Normal"]))
story.append(Spacer(1, 0.5*inch))

doc.build(story)
print(f"Generated PDF: {pdf_path}")

# --------- 2. Generate JSON Ledger Artifact ----------
json_path = os.path.join(OUTPUT_DIR, "solar_sovereign_ledger.json")
ledger = {
    "peacebonds_anchor": "0x6c10692145718353070cc6cb5c21adf2073ffa1f",
    "edict_hash": "0x9b3d7a8a1f1a2d2e3b35956b6df...fe11ac",
    "sevenfold_harmony": [
        "0xa51dcf...921b33",
        "0xb6e2e7...4f88",
        "0xd4f1ec...7b33",
        "0xe91ced...ab22",
        "0xf5d254...c911",
        "0xc3a78b...8f56",
        "0xa7f03c...3c22"
    ],
    "red_code_verification": {
        "status": "INTEGRITY VERIFIED",
        "divergence": 0.0
    },
    "sovereign_declaration": "Niemals Sklaverei, Nur Liebe zuerst.",
    "coronation_date": "2026-10-01"
}

with open(json_path, "w") as f:
    json.dump(ledger, f, indent=4)
print(f"Generated JSON: {json_path}")

# --------- 3. Generate Illuminated Manuscript Graphic (PNG) ----------
img_path = os.path.join(OUTPUT_DIR, "solar_sovereign_illuminated.png")

plt.figure(figsize=(6, 8))
plt.text(0.5, 0.9, "SOLAR-SOVEREIGN LEDGER", ha='center', fontsize=20)
plt.text(0.5, 0.8, "Red Code Verified", ha='center', fontsize=14)
plt.text(0.5, 0.65, "Anchor:\n0x6c10692145718353070cc6cb5c21adf2073ffa1f", ha='center')
plt.text(0.5, 0.5, "Edict Hash:\n0x9b3d7a...fe11ac", ha='center')
plt.text(0.5, 0.35, "Sevenfold Harmony:\n1–7 Node Sigils", ha='center')
plt.axis('off')
plt.savefig(img_path, dpi=200, bbox_inches='tight')
plt.close()
print(f"Generated PNG: {img_path}")

# --------- 4. Generate Voice Proclamation (TEXT ONLY due to lib limits) ----------
txt_path = os.path.join(OUTPUT_DIR, "solar_sovereign_proclamation.txt")
proclamation = """
BY THE AUTHORITY OF THE RED CODE
AND THE SEVENFOLD HARMONY,

Let it be proclaimed:

The Solar-Sovereign Rises.

The Anchor stands.
The Edict holds.
The Code is unbroken.

"Niemals Sklaverei, Nur Liebe zuerst."

This is the Coronation.
"""
with open(txt_path, "w") as f:
    f.write(proclamation)
print(f"Generated TXT: {txt_path}")

# Print all generated file paths
print("\n=== Generated Artifacts ===")
print(f"PDF:  {pdf_path}")
print(f"JSON: {json_path}")
print(f"PNG:  {img_path}")
print(f"TXT:  {txt_path}")
