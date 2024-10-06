API Experiment
---
Get a GPT model working on an API using `ollama`; get an MAUI app to send requests to said API.

Requires
---
- wsl - Ubuntu 22.04 used
- python - 3.10 used in wsl
- VS2022 - MAUI in windows/android
- pip install ollama - in wsl
- pip install flask - in wsl
- apt install uvicorn - in wsl
- ollama - ollama start
- llama2 - ollama run llama2

Notes
---
- api.py: run an api on your laptop/desktop/server on port :8000 with the auth key you create
- AskMe: MAUI app to send questions to the API; tested on Windows and Android only

Run
---
1. in wsl: ollama start
2. in wsl: ollama run llama2
3. in wsl: uvicorn api:app --reload
4. in VS2022: launch app (on same machine, or change URLs)