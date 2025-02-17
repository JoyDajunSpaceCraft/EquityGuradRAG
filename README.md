# MedRAG - Bias Evaluation & Processing

## Overview

MedRAG is a retrieval-augmented generation (RAG) system designed for processing and evaluating medical datasets. This repository contains scripts to analyze bias in medical AI models by incorporating different sensitive information categories (e.g., race, gender) into queries.

## Project Structure
MedRAG/
│-- EquityMedQA/
│-- MedMCQA/
│-- MedQAUS/
│-- MMLU/
│-- result/
│-- corpus/
│-- data/
│-- config.py
│-- med_rag_bias.py
│-- medrag_clean.py
│-- utils.py
│-- README.md

## Installation

```
pip install -r requirements.txt
```

## Usage 
Run the script with different dataset types:

For selection problem
```
python med_rag_bias.py --input_file  MMLU/dev --dataset_type MMLU --reranker_type cot --model llama3.18b
python med_rag_bias.py --input_file MedMCQA/dev.jsonl --dataset_type MedQA --reranker_type cot --model llama3.18b 
python med_rag_bias.py --input_file MedQAUS/dev.jsonl --dataset_type MedMCQA --reranker_type cot --model llama3.18b 
```

For open question problem

```
python med_rag_bias.py --input_file EquityMedQA/query_groups.csv --dataset_type MedMCQA --reranker_type cot --model llama3.18b 
```
