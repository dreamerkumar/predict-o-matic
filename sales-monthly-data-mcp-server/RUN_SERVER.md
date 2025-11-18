`python api_server.py` alone = Uses system Python ❌
After `source venv/bin/activate` → `python api_server.py` = Uses venv Python ✅
`./venv/bin/python api_server.py` = Uses venv Python directly ✅ (no activation needed)
Bottom line: You need to either activate the venv first, OR use the full path to the venv's Python!
