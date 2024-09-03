import random

# this transform is used for the html-understanding_gen task using axtree instead of the whole html body
def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = f"""<|start_header_id|>system<|end_header_id|>
                You are a helpful assistant specialized in HTML. You can correct index of html nodes based on given instructions.
                <|eot_id|>
                <|start_header_id|>user<|end_header_id|>
                Here is a tree structure of a html page with index of each node: {data['passage']}
                Please output the index of a button with button text="{data['question']}".
                Answer the question and only output the corresponding index.
                <|eot_id|>
                <|start_header_id|>assistant<|end_header_id|>
                """
    # prompt = f"Here is a html body: {data['passage']} Please output the html snippet of an button with text=\"{data['question']}\". Now answer the question and only output the corresponding html snippet."
    processed_correct_answer = correct_answer = data["answer"]
    # in most of the cases, the processed_output is the same as the correct_answer
    return {
        "input": prompt,
        "output": correct_answer,
        "processed_output": processed_correct_answer,
    }
