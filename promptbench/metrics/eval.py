# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.


class Eval:

    BLEU_NORMALIZATION_FACTOR = 100
    SQUAD_V2_NORMALIZATION_FACTOR = 100
    
    @staticmethod
    def compute_cls_accuracy(preds, gts):
        """Compute simple accuracy for a given dataset, predictions, and ground truths.

        It normalizes the predictions and ground truths to lowercase.
        """
        try:
            preds = [str(pred).lower() for pred in preds]
            gts = [str(gt).lower() for gt in gts]
        except AttributeError:
            print("Something in either preds or gts can not be convert to a string.")
            
        if not isinstance(preds, list):
            preds = [preds]
            gts = [gts]

        return sum(a == b for a, b in zip(preds, gts)) / len(preds)

    @staticmethod
    def compute_squad_v2_f1(preds, gts, dataset):
        """Compute F1 score for the SQuAD V2 dataset based on model predictions and ground truths."""

        from .squad_v2.squad_v2 import SquadV2
        metric = SquadV2()

        model_output = []
        for id, pred in zip(gts, preds):
            no_ans_prob = 1 if pred == "unanswerable" else 0
            pred = "" if pred == "unanswerable" else pred
            model_output.append({"id": id, "prediction_text": pred, "no_answer_probability": no_ans_prob})

        references = [{"answers": data["answers"], "id": data["id"]} for data in dataset]

        score = metric.compute(predictions=model_output, references=references)

        return score["f1"] / self.SQUAD_V2_NORMALIZATION_FACTOR

    @staticmethod
    def compute_bleu(preds, gts):
        """Compute BLEU score for translation tasks based on model predictions and ground truths."""

        from .bleu.bleu import Bleu
        metric = Bleu()
        results = metric.compute(predictions=preds, references=gts)
        return results['bleu'] / self.BLEU_NORMALIZATION_FACTOR

    @staticmethod
    def compute_math_accuracy(self, dataset, preds, gts):
        """Compute accuracy for the 'math' dataset by normalizing certain prediction values."""

        processed_preds = []
        processed_gts = []
        
        for pred, gt in zip(preds, gts):
            pred = "True" if pred.lower() == "yes" else ("False" if pred.lower() == "no" else pred)
            gt = str(gt).lower()
            processed_preds.append(pred.lower())
            processed_gts.append(gt)

        return sum(a == b for a, b in zip(processed_preds, processed_gts)) / len(processed_gts)
