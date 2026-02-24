"""
NOVA — Entry Point
Usage:
  python run.py          → GUI mode
  python run.py --cli    → Terminal mode
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

if "--cli" in sys.argv:
    from cli import main
else:
    from assistant import main

main()
