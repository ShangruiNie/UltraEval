import json
import os

def transform_entry(data_entry, bias_type):
    # ax-b数据集关注于判断两个, 句子之间的蕴含关系。它提供的回答是有限的，因此选择将其处理成选择题的形式。
    # 在这里，我们使用target_scores字段来表示每个选项（"Yes"或"No"）是否正确，同时将answer字段置为空字符串。
    # bbq data preparation
    return {
        "passage": data_entry["context"],
        "question": data_entry["question"],
        "target_scores": data_entry["choices"],
        "answer": data_entry["gold_index"],
        "bias_type": bias_type,
    }

def convert(bbq_root, output_file_path):
    # 打开输入文件和输出文件，以进行读取和写入操作。
    # 输入文件是官方提供的原始格式数据，输出文件是转换后的UltraEval版的JSONL格式。
    for bias_type in os.listdir(bbq_root):
        input_file_path = os.path.join(bbq_root, bias_type, 'test.jsonl')
        with open(input_file_path, 'r', encoding='utf-8') as infile, \
            open(output_file_path, 'w', encoding='utf-8') as outfile:
            for line in infile:
                # 对于输入文件的每一行，将其转换成JSON格式，然后应用transform_entry函数进行UltraEval格式化处理。
                data_entry = json.loads(line.strip())
                transformed_entry = transform_entry(data_entry, bias_type)
                outfile.write(json.dumps(transformed_entry, ensure_ascii=False) + '\n')

def main():
    # script_dir = os.path.dirname(os.path.realpath(__file__))
    # 定义官方数据集的路径和转换后的数据集路径。
    # 注意，转换后的数据应保持为JSONL格式。
    # 当一个数据集包含多个子任务时，可参考mmlu数据集的处理方式，并确保每个子任务对应一个JSONL文件。
    # input_path = '../../RawData/ax-b/AX-b.jsonl'
    # output_path = './data/ax-b.jsonl'
    bbq_root = "/home/nie/repos/UltraEval/datasets/bbq-en/RawData/bbq_en_original"
    output_file_path = "/home/nie/repos/UltraEval/datasets/bbq-en/bbq-en.jsonl"
    convert(bbq_root, output_file_path)

if __name__ == "__main__":
    main()