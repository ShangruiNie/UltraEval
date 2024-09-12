import random

# this transform is used for the html-understanding_gen task using axtree instead of the whole html body
def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    prompt = f"""<|start_header_id|>system<|end_header_id|>
                You are a helpful assistant specialized in HTML. You can correct index of html nodes based on given instructions.
                <|eot_id|>
                <|start_header_id|>user<|end_header_id|>
                Here is an example of the task you are going to perform:
                given a html structure tree:
                [0] <html>\n [1] <body>\n  [2] <div class=\"['search_combo_top']\">\n   [4] <form action=\"/places/str:\" class=\"['search']\">\n    [6] <div class=\"['input', 'search', 'append']\">\n     [8] <label for=\"field_2894\">\n      [9] <span style=\"font-size:1rem;position:absolute;z-index:0;\"> Search Term\n      [12] <input autocapitalize=\"off\" autocomplete=\"off\" autocorrect=\"off\" id=\"field_2894\" name=\"str\" placeholder=\"Search ...\" style=\"z-index:1;\" value=\"\">\n     [15] <button class=\"['icon-search']\" style=\"overflow:hidden;\" type=\"submit\"> Search\n      [16] <span style=\"position:absolute;left:50px;\"> Search\n   [21] <div class=\"['clearBoth']\">\n
                and question:
                Please output the index of a button with button text=\"Search\"
                The answer is:
                15
                Now please perform the task:
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
