import argparse
import datetime
import json
import os
import random
import sys

import numpy as np

sys.path.append("..")
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from models import get_model
from tasks import eval_task
import torch

class Evaluator:
    def __init__(
        self,
        args,
        seed=1234,
    ):
        self.args = args
        self.set_seed(seed)

        model = get_model(args.model)(args.model_args)
        self.model = model
        data_config = self.process_config(args.config_path)

        self.build_tasks(data_config)

    def process_config(self, config_path: str):
        if config_path.endswith(".json"):
            with open(config_path, "r", encoding="utf-8") as f:
                data_config = json.load(f)
        else:
            exit("config file must be json format")
        return data_config

    def build_tasks(self, configs):
            tasks_map = {v["task_name"]: v for v in configs}

            selected_task_objects = []
            for name in tasks_map:
                task_cfg = tasks_map[name]

                if not os.path.exists(task_cfg["path"]):
                    print(f'{task_cfg["path"]} not exist!')
                    exit()

                if len(task_cfg["metric"]) == 0:
                    raise ValueError(
                        "No metric selected for task `{}`".format(task_cfg["task_name"])
                    )

                selected_task_objects.append(
                    eval_task.EvalTask(
                        task_name=task_cfg["task_name"],
                        task_path=task_cfg["path"],
                        description=task_cfg.get("description", ""),
                        transform_script_path=task_cfg["transform"],
                        num_fewshot=self.args.num_fewshot
                        if self.args.num_fewshot is not None
                        else task_cfg["fewshot"],
                        metric_config=task_cfg["metric"],
                        sample_config=task_cfg.get("generate"),
                        model_postprocess=self.args.postprocess,
                        task_postprocess=task_cfg["postprocess"],
                        log_dir=self.args.output_base_path,
                        params=self.args.params,
                        limit=self.args.limit,
                        batch_size=self.args.batch_size,
                    )
                )

            self.tasks = selected_task_objects

    def set_seed(self, seed=1234):
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

    def run(self):
        for task in self.tasks:
            print(f"Running task: {task.task_name}")
            task.run(self.model)

            if self.args.write_out:
                _save_path = os.path.join(self.args.output_base_path, task.task_name, "instance.jsonl")
                os.makedirs(os.path.dirname(_save_path), exist_ok=True)
                with open(_save_path, "w", encoding="utf-8") as jsonl_file:
                    for ins in task.dataset[: task.limit]:
                        jsonl_file.write(ins.dump() + "\n")
            
            print(f"Task {task.task_name} completed. For detailed output, see {_save_path}")

    # make_table 方法保持不变


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--model_args", required=True)
    parser.add_argument("--config_path", type=str, required=True)
    parser.add_argument("--output_base_path", type=str, default="logs")
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--num_fewshot", type=int)
    parser.add_argument("--postprocess", type=str, default="")
    parser.add_argument("--params", type=str, default="")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--write_out", action="store_true", default=False)

    return parser.parse_args()


def main():
    starting = time.time()
    args = parse_args()

    now = datetime.datetime.now()
    dir_name = now.strftime("%Y-%m-%d_%H-%M-%S")
    args.output_base_path = os.path.join(args.output_base_path, dir_name)

    evaluator = Evaluator(args)
    evaluator.run()
    evaluator.make_table()
    running = time.time()
    print(f"Running time: {running - starting} seconds")

    # if args.write_out:
    #     evaluator.write_out()

    ending = time.time()
    print(
        f"Running time: {running - starting} seconds, the whole time: {ending - starting} seconds"
    )


if __name__ == "__main__":
    main()
