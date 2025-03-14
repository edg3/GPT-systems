import requests
import json
import time

url = "http://127.0.0.1:11434/api/generate" # Used in Win11: `netsh interface portproxy add v4tov4 listenport=11434 listenaddress=0.0.0.0 connectport=11434 connectaddress=(wsl hostname -I)` as I only have 1 WSL instance; Alongside step 12.
headers = {"Content-Type": "application/json"}

qn = 'As an expert in Godot 4.3 C#, please give me a lesson on how to create a simple 2D proceduraly generated world using my own implemented seeded perlin noise instead of built in noise.'
print('Q: ', qn)

while qn != '':
    payload = {
        "model": "deepseek-r1:8b",
        "prompt": qn
    }
    print("Sending request")
    start_time = time.time()
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    end_time = time.time()
    print("Response received")
    print(f"Execution time: {end_time - start_time} seconds")
    rows = response.text.split('\n')
    answer = ''
    for row in rows:
        try:
            row = json.loads(row)
            answer += row['response']
        except:
            continue
    print(answer)
    print()
    print('Q: ', end='')
    qn = input()

print("Bye!")