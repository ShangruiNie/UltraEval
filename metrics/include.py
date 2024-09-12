from typing import Any


class GtInModelOut:
    def __init__(
        self,
    ):
        pass

    def __call__(self, doc, ground_truth, results) -> Any:
        if isinstance(ground_truth, str):
            ground_truth = [ground_truth]
        # if the ground truth is in the model output, then it's correct
        return 1.0 if ground_truth[0].lower().strip() in results[0].lower().strip() else 0.0


if __name__ == "__main__":
    test_gt = "hello."
    model_out = "hello world"
    print(test_gt in model_out)