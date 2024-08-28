TASK_NAME=html-understanding  # 需要评测的任务，多个用,隔开
URL="http://127.0.0.1:5002/infer"  # 这里是固定的
NUMBER_OF_THREAD=2  # 线程数，一般设为 gpu数/per-proc-gpus
CONFIG_PATH=/home/nie/repos/UltraEval/datasets/html-understanding/config/html-understanding_gen.json  # 评测文件路径
OUTPUT_BASE_PATH=/home/nie/repos/UltraEval/datasets/html-understanding/out  # 结果保存路径

# 步骤1
# 选择评测的任务，生成评测 config文件。其中method=gen，表示生成式
python configs/make_config.py --datasets $TASK_NAME --method gen

# 步骤4
# 执行 Python 脚本
python main.py \
    --model general \
    --model_args url=$URL,concurrency=$NUMBER_OF_THREAD \
    --config_path $CONFIG_PATH \
    --output_base_path $OUTPUT_BASE_PATH \
    --batch_size 1 \
    --postprocess general_torch \
    --params models/model_params/vllm_sample.json \
    --write_out \
    #--limit 32