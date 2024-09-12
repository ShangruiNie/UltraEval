import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = f"""<|start_header_id|>system<|end_header_id|>
                You are a helpful assistant specialized in HTML. You can generate HTML snippets based on given instructions.
                <|eot_id|>
                <|start_header_id|>user<|end_header_id|>
                Here is an example of the task you are going to perform:
                given a html body: 
                <div class=\"search\">\n<div>\n<form action=\"/index.php?s=/home/work/news_ss.html\" method=\"POST\" onsubmit=\"return sub()\">\n<label for=\"\">輸入關鍵詞</label>\n<input id=\"con\" name=\"content\" type=\"text\" value=\"\"/>\n<button type=\"submit\">search</button>\n</form>\n</div>\n</div>
                and question:
                Please output the html snippet of a button with text=\"search\"
                The answer is:
                <button type=\"submit\">search</button>
                Now please perform the task:
                Here is a html body: {data['passage']}
                Please output the html snippet of a button with text="{data['question']}".
                Answer the question and only output the corresponding html snippet.
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
