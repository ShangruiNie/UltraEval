import json

def calculate_average_html_length(jsonl_file):
    total_length = 0
    count = 0
    
    with open(jsonl_file, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            total_length += len(data['passage'])
            count += 1
    
    if count > 0:
        average_length = total_length / count
        return average_length
    else:
        return 0

# 使用示例
jsonl_file = "/home/shangrui-nie/repos/UltraEval/datasets/webSRC/data/webSRC_processed.jsonl"
average_length = calculate_average_html_length(jsonl_file)
print(average_length)