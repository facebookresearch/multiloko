#!/usr/bin/env python3
"""
Copyright (c) Meta Platforms, Inc. and affiliates.

This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import argparse
import glob
import os
import json
import csv
import re
import string
import unicodedata as ud

import sacrebleu
import editdistance

from typing import Dict, List, Tuple, Any, Union
from collections import Counter
from difflib import SequenceMatcher

##################### Answer normalization code #####################

FA_TOKENS = {
    "arabic": ("السؤال:", "الإجابة:"),
    "bengali": ("প্র:", "উ:"),
    "cantonese": ("問題：", "答案:"),
    "czech": ("Otázka:", "Odpověď:"),
    "dutch": ("Vraag:", "Antwoord:"),
    "english": ("Q:", "A:"),
    "french": ("Q :", "R :"),
    "hebrew": ("שאלה", "תשובה"),
    "hindi": ("सवाल:", "जवाब:"),
    "italian": ("D:", "R:"),
    "indonesian": ("T:", "J:"),
    "farsi": ("سؤال:", "جواب:"),
    "german": ("F:", "A:"),
    "japanese": ("質問：", "回答："),
    "khmer": ("សំណួរ៖c", "ចម្លើយ៖"),
    "korean": ("질문:", "답:"),
    "malay": ("Soalan:", "Jawapan:"),
    "marathi": ("प्रश्न:", "उत्तर:"),
    "polish": ("Pytanie:", "Odpowiedź:"),
    "portuguese": ("Pergunta:", "Resposta:"),
    "romanian": ("Întrebare:", "Răspuns:"),
    "russian": ("Вопрос:", "Ответ:"),
    "simplified_mandarin": ("问题：", "答案："),
    "spanish": ("Pregunta:", "Respuesta:"),
    "swedish": ("Fråga:", "Svar:"),
    "tagalog": ("T:", "S:"),
    "thai": ("คำถาม:", "คำตอบ:"),
    "traditional_mandarin": ("問題：", "答案："),
    "turkish": ("S:", "C:"),
    "vietnamese": ("H:", "Đ:"),
    "urdu": ("سوال:", "جواب:"),
}


def remove_articles(text: str) -> str:
    return re.sub(r"\b(a|an|the)\b", " ", text)


def white_space_fix(text: str) -> str:
    return " ".join(text.split())


def remove_punc(text: str) -> str:
    """
    Removes the punctuation from a string. This used to rely on the builtin string.punctuation constant
    which contains these symbols: !"#$%&'()*+,-.:;<=>?@[]^_`{|}~ but it completely misses CJK punctuation or
    some western european language' variations.
    """
    punct = string.punctuation  # Sadly the builtin punctuation is exclusive to ASCII
    # Adapted from https://stackoverflow.com/questions/36640587/how-to-remove-chinese-punctuation-in-python
    extra_punct = r"""„“«»¡¿《》！？｡。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."""
    punct = punct + extra_punct
    exclude = set(punct)
    prediction = "".join(ch for ch in text if ch not in exclude)
    # Now, try harder to strip punctuation using unicode Px prefix
    # https://stackoverflow.com/questions/48496869/python3-remove-arabic-punctuation/48499154#48499154
    prediction = "".join(c for c in prediction if not ud.category(c).startswith("P"))
    return prediction


def normalize_answer(text: str) -> str:
    prediction = white_space_fix(remove_articles(remove_punc(text.lower())))
    # Get rid of some common reasoning corrupted answers:
    if " answer is " in prediction:
        prediction = prediction.split(" answer is ")[-1]
    elif "answer is " in prediction:
        prediction = prediction.replace("answer is ", "")
    # In Japanese a lot of answers have the copula prepended for extra politeness
    elif prediction[-2:] == "です":
        prediction = prediction[:-2]
    return prediction


def postprocess_answers(input: Union[str, List[str]]) -> Union[str, List[str]]:
    if isinstance(input, str):
        return normalize_answer(input)
    else:
        return [normalize_answer(x) for x in input]

##################### Parsing code #####################


def parse_output_csv(filename: str) -> Dict[str, Dict[str, str]]:
    # Parses a CSV file. Expected format is
    # language, id, response
    ret = {}
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        # assert formatting
        assert "language" in reader.fieldnames, reader.fieldnames
        assert "id" in reader.fieldnames
        assert "prediction" in reader.fieldnames
        for row in reader:
            assert row["language"] != ""
            assert row["id"] != ""
            if row["language"] not in ret:
                ret[row["language"]] = {}
            ret[row["language"]][row["id"]] = postprocess_answers(row["prediction"])
    return ret


def parse_output_jsonl(filename: str) -> Dict[str, Dict[str, str]]:
    # Parses a JSONl file. Expected format is
    # {"language": "language", "id" : "id", "prediction": "prediction"}
    ret = {}
    with open(filename, "r") as f:
        for line in f:
            data = json.loads(line)
            assert "language" in data
            assert "id" in data
            assert "prediction" in data
            assert data["language"] != ""
            assert data["id"] != ""
            if data["language"] not in ret:
                ret[data["language"]] = {}
            ret[data["language"]][data["id"]] = postprocess_answers(data["prediction"])
    return ret


def parse_input_jsonl(file_and_lang: List[Tuple[str, str]]) -> Dict[str, Dict[str, List[str]]]:
    # parses the input jsonl file(s)
    # It saves only the id and the true answer ret'language'] = []
    ret = {}
    for filename, language in file_and_lang:
        ret[language] = {}
        with open(filename, "r") as f:
            for line in f:
                data = json.loads(line)
                ret[language][data["id"]] = postprocess_answers(data["targets"])
    return ret


def output_results(results: Dict[str, Any], output_file: Union[str, None]) -> None:
    if output_file:
        with open(output_file, "w") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
    else:
        print(json.dumps(results), ensure_ascii=False, indent=4)


##################### Evaluation code #####################


def f1(prediction: str, targets: List[str]) -> float:
    def _f1(pred_tokens: List[str], gt_tokens: List[str]) -> float:
        common = Counter(pred_tokens) & Counter(gt_tokens)
        num_same = sum(common.values())
        if num_same == 0:
            return 0
        precision = 1.0 * num_same / len(pred_tokens)
        recall = 1.0 * num_same / len(gt_tokens)
        return (2 * precision * recall) / (precision + recall)

    return max(_f1(prediction.split(), target.split()) for target in targets)


def exact_match(prediction: str, targets: List[str]) -> float:
    return max(float(prediction == target) for target in targets)


def sentence_bleu(prediction: str, targets: List[str], **kwargs: Any) -> float:
    return sacrebleu.sentence_bleu(prediction, targets, **kwargs).score


def sentence_chrf(prediction: str, targets: List[str], **kwargs: Any) -> float:
    return sacrebleu.sentence_chrf(prediction, targets, **kwargs).score


def edit_distance(prediction_tokens: str, target_tokens: str) -> float:
    """
    Get minimum edit distance (Levenshtein distance) between prediction and target
    """
    return float(editdistance.eval(prediction_tokens, target_tokens))


def edit_distance_many(prediction_tokens: str, target_tokens: List[str]) -> float:
    """
    Get minimum edit distance (Levenshtein distance) between prediction and
    multiple possible targets.
    """
    return float(
        min(edit_distance(prediction_tokens, target) for target in target_tokens)
    )


def edit_similarity(prediction: str, targets: List[str]) -> float:
    return max(SequenceMatcher(None, prediction, target).ratio() for target in targets)


def contains(generation: str, targets: List[str]) -> float:
    return any([x in generation for x in targets]) * 1.0


def evaluate_all(reference_answers, our_answers):
    # Evaluate all metrics
    metrics = {
        "em": exact_match,
        "f1": f1,
        "bleu": sentence_bleu,
        "chrf": sentence_chrf,
        "edit_distance": edit_distance_many,
        "edit_similarity": edit_similarity,
        "contains": contains,
    }
    # Compute per example scores
    results = {}
    for lang, examples in our_answers.items():
        results[lang] = {}
        ref_current = reference_answers[lang]
        for id, prediction in examples.items():
            results[lang][id] = {}
            targets = [t.lower() for t in ref_current[id]]
            for metric_name, metric in metrics.items():
                results[lang][id][metric_name] = metric(prediction, targets)
            results[lang][id]["targets"] = targets
            results[lang][id]["prediction"] = prediction
        # Now compute aggregate scores for that language
        for metric in metrics:
            count = 0
            mysum = 0
            for id in results[lang]:
                if id in metrics:
                    continue
                mysum += results[lang][id][metric]
                count += 1
            results[lang][metric] = mysum / count
    # Now compute across all languages
    results["group_metrics"] = {}
    for metric in metrics:
        results["group_metrics"][f"average_{metric}"] = sum(results[lang][metric] for lang in results if lang != "group_metrics") / (len(results) - 1)
        results["group_metrics"][f"max_{metric}"] = max(results[lang][metric] for lang in results if lang != "group_metrics")
        results["group_metrics"][f"min_{metric}"] = min(results[lang][metric] for lang in results if lang != "group_metrics")
        results["group_metrics"][f"gap_{metric}"] = results["group_metrics"][f"max_{metric}"] - results["group_metrics"][f"min_{metric}"]
    return results


##################### Main code #####################


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset_location",
        "-d",
        help="Dataset root directory where all language folders are located",
        required=True,
    )
    parser.add_argument(
        "--subset",
        "-s",
        help="subset, ie dev, test, etc. Should match the jsonl filename inside the individual dataset language folders",
        required=True,
    )
    parser.add_argument(
        "--predictions",
        "-p",
        help="Prediction file to evaluate. Could be CSV or JSONL",
        required=True,
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output file (json) to write results to. If not specified, will print to stdout",
    )

    args = parser.parse_args()
    input_parse_tuples = []
    for lang in os.listdir(args.dataset_location):
        if "debug" in lang:
            continue
        if not os.path.isdir(os.path.join(args.dataset_location, lang)):
            continue
        path = os.path.join(args.dataset_location, lang, f"{args.subset}.jsonl")
        if not os.path.exists(path):
            continue
        input_parse_tuples.append((path, lang))
        # get translated paths
        translation_paths = glob.glob(os.path.join(args.dataset_location, lang, f"{args.subset}_translated*.jsonl"))
        for translation_path in translation_paths:
            # format is {dev|test}_translated_{human|machine}_lang.jsonl
            mylang = translation_path.split("/")[-1].split(".jsonl")[0]
            mylang = mylang.replace(args.subset, lang)
            input_parse_tuples.append((translation_path, mylang))

    reference_answers = parse_input_jsonl(input_parse_tuples)
    our_answers = parse_output_csv(args.predictions) if args.predictions.endswith(".csv") else parse_output_jsonl(args.predictions)
    results = evaluate_all(reference_answers, our_answers)
    output_results(results, args.output)

if __name__ == "__main__":
    main()
