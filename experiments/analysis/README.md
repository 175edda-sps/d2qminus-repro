# Analysis Experiments

The code provided below allows partial reproduction of our analysis experiments.

## 1. Preprocessing
To perform the new and copied terms analysis, it is required to perform preprocessing on the original text and expansion queries, and then keep the unique terms of the original text. 
To achieve so,  you can run the following command:

```
python experiments/analysis/preproces_corpus.py --input "path_to_the_input_scored_file.jsonl" \
                               --output "path_to_save_the_processed_file.jsonl"
```
