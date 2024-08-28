"""
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("/home/nie/models/lamarr_org_2.7B_EN/iter_2.7B_EN_MLM_HF")
tokenizer = AutoTokenizer.from_pretrained("/home/nie/models/lamarr_org_2.7B_EN/iter_2.7B_EN_MLM_HF")

tokenized = tokenizer(["Hello, my dog is cute.", "hello, I have a cat in my apartment, but my cat is not cute."], padding=True, return_tensors="pt")
"""

from flask import Flask, request, jsonify
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from gevent.pywsgi import WSGIServer
from URLs.dispatcher import GPUDispatcher as gdp
gdp.bind_worker_gpus()

app = Flask(__name__)

print("Initializing model and tokenizer...")

# Set the device to GPU if available
device = 'cuda' if torch.cuda.is_available() else 'cpu'

model_name = os.environ.get('HF_MODEL_NAME')
port = os.environ.get('PORT')

# Load the model and tokenizer
####模型初始化####
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
####tokenizer初始化####
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 此处为transformers库部署模型的特殊适配
if tokenizer.pad_token is None:
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    model.resize_token_embeddings(len(tokenizer))

print("Model and tokenizer initialized.")

#参数字典可根据自有模型特点自定义
params_dict = {
    "max_new_tokens": 100,
    "temperature": 0.3,
    "top_p": 0.8
}

@app.route('/infer', methods=['POST'])
def main():
    datas = request.get_json()
    params = datas["params"]
    prompt = datas["instances"]

    for key, value in params.items():
        if key == "max_tokens":
            params_dict["max_new_tokens"] = value
        elif key in params_dict:
            params_dict[key] = value
    if prompt == "":
        return jsonify({'error': 'No prompt provided'}), 400
    
    #调用tokenizer，需自定义接口
    inputs = tokenizer(prompt, padding=True, return_tensors="pt").to(device)  # Prepare the input tensor

    #调用模型的推理函数，需自定义接口
    generate_ids = model.generate(inputs.input_ids, **params_dict)

    # Decoding the generated ids to text
    generated_text = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
    assert len(prompt) == len(generated_text)
    for j in range(len(prompt)):
        generated_text[j] = generated_text[j][len(prompt[j]):]
    return jsonify(generated_text)

if __name__ == '__main__':
    # Run the Flask app
    http_server = WSGIServer(('127.0.0.1', port), app)
    http_server.serve_forever()