import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, List

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from tqdm import tqdm

from utils import utils

data_prompt = {
    "params": {},
    "instances": [],
}

class GeneralModel:
    def __init__(self, arg_string):
        args = utils.simple_parse_args_string(arg_string)
        self.model_name = args.get("model_name", "")
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def generate(self, request):
        results = []
        for instance in request.instances:
            input_text = instance["input"]
            input_ids = self.tokenizer.encode(input_text, return_tensors="pt").to(
                self.device
            )
            output = self.model.generate(input_ids)
            decoded_output = self.tokenizer.decode(output[0], skip_special_tokens=True)
            results.append(decoded_output)
        return results

    def loglikelihood(self, request):
        pass
