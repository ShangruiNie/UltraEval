import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = f"Here is a html body: \\n\
          {data['passage']}\\n\
          \\n\
          \\n\
          Please output the html snippet of an input box with placeholder=\"{data['question']}\""
    processed_correct_answer = correct_answer = data["answer"]
    return {
        "input": prompt,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
