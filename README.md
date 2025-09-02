# MultiLoKo: a multilingual local knowledge benchmark for LLMs

* [Introduction](#introduction)
* [Leaderboard](#leaderboard)
* [Data](#data)
* [Evaluation](#evaluation)

## Introduction <a id="introduction">

MultiLoKo is a multilingual knowledge benchmark, covering 30 languages plus English.
The questions are separately sourced for each language, with an annotation protocol designed to target locally relevant topics for the respective language.
MultiLoKo contains the original data for each language, as well as both human and machine-authored translations of each non-English subset into English and vice versa, facilitating studies into a variety of research questions relating to multilinguality.
More information about the benchmark design can be found in the release paper of the benchmark:

* Dieuwke Hupkes and Nikolay Bogoychev.
[MultiLoKo: a multilingual local knowledge benchmark for LLMs spanning 31 languages](https://arxiv.org/abs/2504.10356).

```
@article{hupkes2025multiloko,
      title={MultiLoKo: a multilingual local knowledge benchmark for LLMs spanning 31 languages
},
      author = {Dieuwke Hupkes and Nikolay Bogoychev},
      year = {2025},
      journal = {CoRR},
      volume = {abs/2504.10356},
      eprinttype = {arXiv},
      eprint = {2504.10356},
      url = {https://doi.org/10.48550/arXiv.2504.10356},
}
```

## Leaderboard <a id="leaderboard">
In the paper, we report scores on the public development set.
Below, we report scores on the private test set of MultiLoKo, which will be released at a later time.
We include average exact match across languages as average performance metric, the gap between the best and worst performing languages as a parity metric, and the average mother tongue effect (EM on locally sourced data in local language - EM on local data translated to English) as a metric of transfer. 
The prompts that were used to obtain these results can be found in [examples/prompts.py](examples/prompts.py); detailed post processing steps can be found in our [paper](https://arxiv.org/pdf/2504.10356), Appendix C.
± indicates 2 times standard error across languages.

| Rank | Model Name           | Average EM (↑ better) | Gap (↓ better) | MTE (↓ better) | Min EM (↑ better) | Max EM (↑ better) |
| ---  | ---                  | ---                   | ---            | ---            | ---               | ---               |
| 1    | Llama 3.1 405B       | 31.03 ± 2.8           | 33.60          | 5.57 ± 1.6     | 16.40             | 50.00             |
| 2    | GPT4-o               | 30.97 ± 3.5           | 43.20          | 2.76 ± 2.0     | 12.00             | 55.20             |
| 3    | Gemini 2.0 Flash     | 30.61 ± 2.9           | 36.00          | 5.74 ± 2.0     | 12.80             | 48.80             |
| 4    | Llama 3.1 405B Chat  | 25.07 ± 3.2           | 34.80          | 4.25 ± 2.6     | 8.80              | 43.60             |
| 5    | Llama 3.1 70B        | 24.28 ± 2.8           | 35.20          | 3.30 ± 1.5     | 12.40             | 47.60             |
| 6    | Claude 3.5 Sonnet    | 23.19 ± 4.1           | 40.40          | 20.75 ± 3.9    | 0.00              | 40.40             |
| 7    | Llama 3.1 70B Chat   | 19.73 ± 2.7           | 34.40          | 0.88 ± 1.8     | 7.20              | 41.60             |
| 8    | Mixtral 8x22B        | 19.32 ± 3.9           | 42.80          | -1.64 ± 2.9    | 3.60              | 46.40             |
| 9    | Qwen2.5 72B          | 16.37 ± 2.6           | 32.80          | 1.15 ± 1.9     | 7.60              | 40.40             |
| 10   | Mixtral 8x22B-it     | 7.99 ± 2.6            | 30.80          | -5.74 ± 2.0    | 0.00              | 30.80             |
| 11   | Qwen2.5 72B instruct | 2.14 ± 0.7            | 6.80           | -0.65 ± 0.8    | 0.40              | 7.20              |

If you would like to obtain scores for your model on the set, please upload your model on HuggingFace and send us a request to compute scores through the creation of an issue on this github page.
We will return the full set of results to you, and put the test results of your model on the leaderboard on this page.
If it is not possible to upload your model on HuggingFace, please reach out to either one of the authors to discuss other options.

## Data <a id="data">

MultiLoKo's data can be found in the the password protected archive `benchmark_data.tar.gz.enc` which when extracted will produce the `benchmark_data` directory which the script relies on in order to function. 
We password protect the data to prevent its accidental ingestion by LLMs when crawling.
While the data is released under a [permissive license](LICENSE), we therefore ask you to please do not mirror it to prevent inadvertent contamination.
To extract the archive do:
```bash
# the password is multiloko
openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -d -in benchmark_data.tar.xz.enc | tar -xJ
```
Each language has its own subdirectory, containing:
- A jsonl file `dev.jsonl` containing  the 250 locally sourced questions for the respective language.
- A jsonl file `knowledge_fewshot.jsonl`, containing five fewshot examples for the language.
- A jsonl file `dev_translated_human_english.jsonl` with the human translations of the file into English (for English, instead there will be 30 files `dev_translated_human_{language}.jsonl`, for each of the respective languages).
- A jsonl file `dev_translated_machine_english.jsonl` with the machine translations of the file into English (for English, instead there will be 30 files `dev_translated_machine_{language}.jsonl`, for each of the respective languages).

Multilingual prompts are contained [examples/prompts.py](examples/prompts.py)

You can assemble the prompts to query the model with yourself, or you can run [examples/create_examples.py](examples/create_examples.py) once which will produce the `prepared_data` folder which now contains fully assembled fewshot and chat prompts for all languages in a jsonl format. Each individual line is trivial dictionary with a single `text` key which is the prompt that needs to be submitted to the model.

MultiLoKo also has a secret test set with 250 examples for each languages, which will be released later on, blindly.
The split is similar to the dev split, apart from the fact that the topics it includes are more obscure.
If you would like to know how well your model fares on the test set, please provide us with a HuggingFace implementation of your model.
We will return the full set of results to you, and put you on the [leaderboard](#leaderboard) on this page.

### Data format <a id="data_format">

The benchmark data is stored in jsonl files, containing a separate json object for each question. 
Each such objects has six fields:
- `text`: the paragraph from which the question was created. The answer to the question can be derived from this text. It is possible to transform the benchmark into a reading comprehension benchmark by preceeding the question itself from this text.
- `question`: the question itself.
- `targets`: a list of acceptable (short) answers to the question.
- `target`: a long answer to the question, which could potentially be used for COT. Note that the long answers have not been checked as extensively as the questions and short answers.
- `id`: the wikipedia page that the text is sourced from, along with the rank of that page in the relevant locale.
- `output_type`: the expected type of the output (e.g.\ number, date, year, word, etc)

## Evaluation <a id="evaluation">
We provided an evaluation script [eval.py](eval.py) that can be ran directly on a model's output, provided in jsonl or csv.
The script postprocesses and normalises the model answers and computes f1 score, exact match score, sentence chrf, edit distance between the closest target, edit distance between the first target, and max edit similarity between the targets.
It also computes five aggregate metrics for each of the metrics above: the average score, the maximum and minimum scores (across languages), and the gap between the best and worst performing language. We support both CSV and JSONL. 
Examples can be found in [examples/test.csv](examples/test.csv) and [examples/test.jsonl](examples/test.jsonl)

### Usage
```
$ ./eval.py --help
usage: eval.py [-h] --dataset_location DATASET_LOCATION --subset SUBSET --predictions PREDICTIONS [--output OUTPUT]

options:
  -h, --help            show this help message and exit
  --dataset_location, -d DATASET_LOCATION
                        Dataset root directory where all language folders are located
  --subset, -s SUBSET   subset, ie dev, test, etc. Should match the jsonl filename inside the individual dataset language folders
  --predictions, -p PREDICTIONS
                        Prediction file to evaluate. Could be CSV or JSONL
  --output, -o OUTPUT   Output file (json) to write results to. If not specified, will print to stdout
./eval.py -d benchmark_data -s dev -p examples/test.jsonl -o testscore.json
```

### Metric cheat sheet

| Metric | Description |
| --- | --- |
| Average EM | The first main metric we use to quantify performance for MultiLoKo is the average Exact Match score across languages, which expresses how many of the answers match one of the gold standard answers verbatim (after post-processing the answers). |
| Gap | The second main metric is the gap between a model’s best and worst performing language. We gap to quantify the extent to which a model has achieved parity across languages. Because a small gap can be achieved both through parity on high scores as parity on low scores, it is most informative in combination with average benchmark performance. |
| Mother tongue effect (MTE) | MTE expresses the impact of asking questions in a language in which the requested information is locally salient, compared to asking it in English. A positive MTE indicates information is more readily available in the language it was (likely) present in the training data, whereas a negative mother tongue effect indicates the information is more easily accessible in English. |
|Locality effect (LE) | LE quantifies the effect of using locally sourced vs translated data. It is measured by computing the difference between scores for locally sourced data and translated English-sourced data. A positive LE implies that using translated English data underestimates performance on a language, a negative LE that using translated English data overestimates performance. |

## For developers
Spotted an error in the data? Inconsistency? Please, feel free to submit a PR. Don't forget to compress the data back:
```bash
tar -cJ --no-xattrs benchmark_data | openssl enc -aes-256-cbc -pbkdf2 -iter 100000 -out benchmark_data.tar.xz.enc
```
If you're running MacOS don't forget to clear any temporary files before creating the archive and maybe exporting `COPYFILE_DISABLE=1` to prevent addition of Apple specific headers.


