# In WSL - my WSL isn't set up standard; sudo might not be needed
cd ./content
sudo apt-get -y install -qq aria2

sudo git clone -b V20230720 https://github.com/Troyanovsky/text-generation-webui
cd ./text-generation-webui
pip install -r requirements.txt
pip install -U gradio==3.32.0

pip uninstall -y llama-cpp-python
CMAKE_ARGS="-DLLAMA_CUBLAS=on" FORCE_CMAKE=1 pip install llama-cpp-python==0.1.78 --no-cache-dir

aria2c --console-log-level=error -c -x 16 -s 16 -k 1M https://huggingface.co/TheBloke/Llama-2-13B-chat-GGML/resolve/main/llama-2-13b-chat.ggmlv3.q2_K.bin -d ./models/ -o llama-2-13b-chat.ggmlv3.q2_K.bin

python server.py --share --chat --n-gpu-layers 200000 --model llama-2-13b-chat.ggmlv3.q2_K.bin