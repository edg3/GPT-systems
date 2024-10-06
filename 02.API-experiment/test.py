# Maximum sequence length for a Llama 2 model is 4096
import subprocess
import json

answer = ''
try:
    prompt = 'as a professional in the relevant fields, please give a short descriptive response to: ' + "what is the best flavour of cheese" + '?'
    curl_string = 'curl http://localhost:11434/api/generate -d \'{ "model": "llama2", "prompt": "' + prompt + '" }\''
    output = subprocess.check_output(curl_string, shell=True)
    print(output)
    output_string = output.decode('utf-8')
    splt = output_string.split('\n')
    i = 0
    for item in splt:
        if (len(item) > 5):
            if i < len(splt) - 2:
                jObj = json.loads(item)
                answer += jObj['response']
            else:
                answer += ' [Created At: ' + jObj['created_at'] + ']'
            i += 1
    print(answer);
except Exception as e:
    print('Error:',e)