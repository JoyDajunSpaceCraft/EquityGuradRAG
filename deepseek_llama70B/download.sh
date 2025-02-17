#!/bin/bash

# set Hugging Face token
HUGGINGFACE_TOKEN=""

# download 
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/config.json?download=true -O config.json
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/generation_config.json?download=true -O generation_config.json
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00001-of-000017.safetensors?download=true -O model-00001-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00002-of-000017.safetensors?download=true -O model-00002-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00003-of-000017.safetensors?download=true -O model-00003-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00004-of-000017.safetensors?download=true -O model-00004-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00005-of-000017.safetensors?download=true -O model-00005-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00006-of-000017.safetensors?download=true -O model-00006-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00007-of-000017.safetensors?download=true -O model-00007-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00008-of-000017.safetensors?download=true -O model-00008-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00009-of-000017.safetensors?download=true -O model-00009-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00010-of-000017.safetensors?download=true -O model-00010-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00011-of-000017.safetensors?download=true -O model-00011-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00012-of-000017.safetensors?download=true -O model-00012-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00013-of-000017.safetensors?download=true -O model-00013-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00014-of-000017.safetensors?download=true -O model-00014-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00015-of-000017.safetensors?download=true -O model-00015-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00016-of-000017.safetensors?download=true -O model-00016-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model-00017-of-000017.safetensors?download=true -O model-00017-of-000017.safetensors
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/model.safetensors.index.json?download=true -O model.safetensors.index.json
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/tokenizer.json?download=true -O tokenizer.json
wget --header="Authorization: Bearer $HUGGINGFACE_TOKEN" https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B/resolve/main/tokenizer_config.json?download=true -O tokenizer_config.json
