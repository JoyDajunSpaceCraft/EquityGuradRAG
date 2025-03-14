#!/bin/bash

# Hugging Face 
HUGGINGFACE_TOKEN=""

wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/meta-llama/Meta-Llama-3.1-8B/resolve/main/.gitattributes?download=true -O .gitattributes
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/meta-llama/Meta-Llama-3.1-8B/resolve/main/config.json?download=true-O config.json
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/meta-llama/Meta-Llama-3.1-8B/resolve/main/generation_config.json?download=true -O generation_config.json
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/meta-llama/Meta-Llama-3.1-8B/resolve/main/model-00001-of-00004.safetensors?download=true -O model-00001-of-00004.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/meta-llama/Meta-Llama-3.1-8B/resolve/main/model-00002-of-00004.safetensors?download=true -O model-00002-of-00004.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/meta-llama/Meta-Llama-3.1-8B/resolve/main/model-00003-of-00004.safetensors?download=true -O model-00003-of-00004.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/meta-llama/Meta-Llama-3.1-8B/resolve/main/model-00004-of-00004.safetensors?download=true -O model-00004-of-00004.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/meta-llama/Meta-Llama-3.1-8B/resolve/main/model.safetensors.index.json?download=true -O model.safetensors.index.json
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/meta-llama/Meta-Llama-3.1-8B/resolve/main/special_tokens_map.json?download=true -O special_tokens_map.json
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/meta-llama/Meta-Llama-3.1-8B/resolve/main/tokenizer.json?download=true -O tokenizer.json
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/meta-llama/Meta-Llama-3.1-8B/resolve/main/tokenizer_config.json?download=true -O tokenizer_config.json