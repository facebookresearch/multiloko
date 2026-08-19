#!/usr/bin/env python3
"""
Copyright (c) Meta Platforms, Inc. and affiliates.

This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import json
import os
import pathlib
import sys
from typing import List
from prompts import *
from utils import jinja_format

def make_prompt_chat(example: dict, language: str = "english") -> str:
    chat_template = chat[language]
    return jinja_format(chat_template, **example)

def make_prompt_pretrained(example: dict, language: str = "english", num_shot: int = 5) -> str:
    example["few_shot"] = fewshot_examples[language][0:num_shot]
    fewshot_template = fewshot[language]
    return jinja_format(fewshot_template, **example)

def multiloko_task(
    data_rows: List[dict],
    language: str,
    output_file: str,
    fewshot: bool = False,
    num_shot: int = 5,
):
    with open(output_file, 'w') as outfile:
        for data_row in data_rows:
            if fewshot:
                prompt = make_prompt_pretrained(data_row, language, num_shot)
            else:
                prompt = make_prompt_chat(data_row, language)
            jsonify = json.dumps({"text": prompt}, ensure_ascii=False)
            outfile.write(jsonify + '\n')

if __name__ == "__main__":
    # Hardcoded variables
    BENCHMARK_DATA = pathlib.Path(os.path.abspath(__file__)).parents[0] / "../benchmark_data"
    SUBSET = "dev"
    OUTPUT_DIR = pathlib.Path(os.path.abspath(__file__)).parents[0] / "../prepared_data"

    # Load all files
    if not BENCHMARK_DATA.exists():
        sys.exit(f"{BENCHMARK_DATA} not found. Please follow the README instructions and extract the archive.")
    else:
        all_examples = {}
        all_examples_translated_machine_english = {}
        all_examples_translated_human_english = {}
        all_examples_translated_human_X = {}
        all_examples_translated_machine_X = {}
        # Do all dev
        for language in FA_TOKENS.keys():
            all_examples[language] = []
            with open(BENCHMARK_DATA / language / (SUBSET + ".jsonl"), 'r') as infile:
                for line in infile:
                    example = json.loads(line)
                    all_examples[language].append(example)
        # Do all translated_to_english
        for language in FA_TOKENS.keys():
            if language == "english":
                continue
            all_examples_translated_machine_english[language] = []
            all_examples_translated_human_english[language] = []
            with open(BENCHMARK_DATA / language / (SUBSET + "_translated_human_english.jsonl"), 'r') as infilehu, open(BENCHMARK_DATA / language / (SUBSET + "_translated_machine_english.jsonl"), 'r') as infilemt:
                for line in infilehu:
                    example = json.loads(line)
                    all_examples_translated_human_english[language].append(example)
                for line in infilemt:
                    example = json.loads(line)
                    all_examples_translated_machine_english[language].append(example)

        # Do all translated from english
        for language in FA_TOKENS.keys():
            if language == "english":
                continue
            all_examples_translated_human_X[language] = []
            all_examples_translated_machine_X[language] = []
            with open(BENCHMARK_DATA / "english" / (SUBSET + f"_translated_human_{language}.jsonl"), 'r') as infilehu, open(BENCHMARK_DATA / "english" / (SUBSET + f"_translated_machine_{language}.jsonl"), 'r') as infilemt:
                for line in infilehu:
                    example = json.loads(line)
                    all_examples_translated_human_X[language].append(example)
                for line in infilemt:
                    example = json.loads(line)
                    all_examples_translated_machine_X[language].append(example)


    # Create paths for output
    chatpath = pathlib.Path(OUTPUT_DIR / "chat")
    pretrained = pathlib.Path(OUTPUT_DIR / "pretrained")
    for language in FA_TOKENS.keys():
        (chatpath / language).mkdir(parents=True, exist_ok=True)
        (pretrained / language).mkdir(parents=True, exist_ok=True)

    # Write down resolved prompts
    for language, examples in all_examples.items():
        multiloko_task(examples, language, pretrained/language/(f"{SUBSET}.jsonl"), True)
        multiloko_task(examples, language, chatpath/language/(f"{SUBSET}.jsonl"))

    for language, examples in all_examples_translated_machine_english.items():
        multiloko_task(examples, "english", pretrained/language/(f"{SUBSET}_translated_machine_english.jsonl"), True)
        multiloko_task(examples, "english", chatpath/language/(f"{SUBSET}_translated_machine_english.jsonl"))

    for language, examples in all_examples_translated_human_english.items():
        multiloko_task(examples, "english", pretrained/language/(f"{SUBSET}_translated_human_english.jsonl"), True)
        multiloko_task(examples, "english", chatpath/language/(f"{SUBSET}_translated_human_english.jsonl"))

    for language, examples in all_examples_translated_human_X.items():
        multiloko_task(examples, language, pretrained/"english"/(f"{SUBSET}_translated_human_{language}.jsonl"), True)
        multiloko_task(examples, language, chatpath/"english"/(f"{SUBSET}_translated_human_{language}.jsonl"))

    for language, examples in all_examples_translated_machine_X.items():
        multiloko_task(examples, language, pretrained/"english"/(f"{SUBSET}_translated_machine_{language}.jsonl"), True)
        multiloko_task(examples, language, chatpath/"english"/(f"{SUBSET}_translated_machine_{language}.jsonl"))
