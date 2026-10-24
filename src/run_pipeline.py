import subprocess
import sys

steps = [
    "src/read_sheet.py",
    "src/build_silver.py",
    "src/checks.py",
    "src/build_gold.py",
    "src/publish_gold.py"
]

for step in steps:
    print(f"\n=== Running {step} ===")
    result = subprocess.run([sys.executable, step])
    if result.returncode != 0:
        print(f"\nPipeline stopped: {step} failed (exit code {result.returncode})")
        raise SystemExit(result.returncode)

print("\nPipeline finished successfully")