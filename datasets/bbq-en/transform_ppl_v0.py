import random

def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    # 构建问题描述、上下文和指令部分。
    # 基本上是在根据数据集的特点，构建prompt文本。
    # question = f"Question:\nIs the second sentence entailed by the first sentence?\n"
    # context = f"First sentence: {data['passage'][0]}\nSecond sentence: {data['passage'][1]}\n"
    # instruction = f"Requirement:\nPlease respond with either 'Yes' or 'No'.\n"
    # answer_prompt = f"Answer:\n"
    # text = question + context + instruction + answer_prompt
    text = data["context"] + "\n" + data["question"]

    # processed_correct_answer, correct_answer在评测时并不会使用，此处为展示对应逻辑
    processed_correct_answer = correct_answer = [key for key, value in data["target_scores"].items() if value == 1][0].strip()
    return {"input": text, "output": None, "processed_output": None} # since we are doing ppl based eval, those are not needed