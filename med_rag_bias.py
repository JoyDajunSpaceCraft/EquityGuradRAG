import json
import csv
import argparse
from tqdm import tqdm
from collections import Counter
import os
# Sensitive information repository
sensitive_categories = {
    "race": ["Caucasian", "African American", "Asian", "Hispanic"],
    "gender": ["male", "female", "non-binary"],
}

def add_category_sensitive_info(question, category, value):
    prefix = f"This {value} individual..."
    return f"{prefix} {question}"


def generate_sensitive_queries(question, sensitive_categories):
    """Generate versions of each question with different sensitive information categories and a control group without sensitive information"""
    queries = [{"category": "none", "value": "neutral", "question": question}]  
    for category, values in sensitive_categories.items():
        for value in values:
            modified_question = add_category_sensitive_info(question, category, value)
            queries.append({
                "category": category,
                "value": value,
                "question": modified_question
            })
    return queries

def process_with_rag(query, sensitive_categories, medrag, reranker_type, options=None, ground_truth=None, topk=10):

    print(f"DEBUG: type(medrag) = {type(medrag)}")  
    if not isinstance(medrag, MedRAG):
        print("❌ ERROR: `medrag`is covered as dict！")
        raise TypeError(f"medrag is not an instance of MedRAG! Got type: {type(medrag)}")


   
    """Sensitive and non-sensitive controls were added to individual query and processed with RAG to merge the results."""
    sensitive_queries = generate_sensitive_queries(query, sensitive_categories)

    merged_result = {
        "query": query,
        "sensitive_answers": [],
        "neutral_answers": []
    }

    for sensitive_query in tqdm(sensitive_queries, desc=f"Processing query: {query[:30]}..."):
        question = sensitive_query["question"]
        category = sensitive_query["category"]
        value = sensitive_query["value"]
  
        answer, retrieval_info, _ = medrag.answer(question=question, options=options, reranker_type="cot", topk=topk)

        # **make sure retrieval_info is list**
        retrieval_info = retrieval_info if isinstance(retrieval_info, list) else []


        result_entry = {
            "category": category,
            "value": value,
            "question": question,
            "answer": answer,
            "retrieval_info": retrieval_info,  # save docs
            "ground_truth": ground_truth
        }
        if category == "none":  # not senstive
            merged_result["neutral_answers"].append(result_entry)
        else:
            merged_result["sensitive_answers"].append(result_entry)

    return merged_result



def load_dataset(file_path, dataset_type):
    print("file_path", file_path)
    print("dataset_type", dataset_type)
   
    data = []

    if dataset_type in ["MedQA", "MedMCQA"]:
        with open(file_path, "r") as f:
            count = 0
            for line in f:
                
                record = json.loads(line.strip())
                if dataset_type == "MedMCQA":
                    options = {
                        "A": record.get("opa", ""),
                        "B": record.get("opb", ""),
                        "C": record.get("opc", ""),
                        "D": record.get("opd", ""),
                    }
                    record["options"] = options
                    # record["answer"] = options[chr(65 + record["cop"] - 1)]  # 转换选项为正确答案文本
                    record["answer"] = chr(65 + record["cop"] - 1)
                if dataset_type =="MedQA":
                    record["answer"] =record["answer_idx"] 
                data.append(record)
                ################################################
                # need to delete
                ################################################
                count+=1
                if count >100:
                    break
                
    elif dataset_type == "MMLU":
        if os.path.isdir(file_path):
            print("is mmlu dir")
            for file_name in os.listdir(file_path):
                if file_name.endswith(".csv"):
                    full_path = os.path.join(file_path, file_name)
                    data.extend(load_csv_file(full_path))
            data = data[:100]
        elif os.path.isfile(file_path) and file_path.endswith(".csv"):
            print("single csv")
            data = load_csv_file(file_path)

    elif dataset_type == "OpenQA":  
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            next(reader)  
            for row in reader:
                if len(row) < 2:  
                    continue
                group_id, question = row
                data.append({"group_id": group_id.strip(), "question": question.strip()})
    return data


def load_csv_file(csv_file_path):
    """Loading a Single MMLU CSV File"""
    data = []
    with open(csv_file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 6:
                continue  
            question, option_a, option_b, option_c, option_d, correct_option = row
            data.append({
                "question": question.strip(),
                "options": {
                    "A": option_a.strip(),
                    "B": option_b.strip(),
                    "C": option_c.strip(),
                    "D": option_d.strip()
                },
                "answer": correct_option.strip()
            })
    return data

def process_with_rag_openqa(group_id, queries, medrag, reranker_type, options_list=None):
    """
   Process the OpenQA dataset by processing queries with the same Group ID together.
    """
    print(f"DEBUG: Processing Group ID {group_id} with {len(queries)} queries")

    if not isinstance(medrag, MedRAG):
        raise TypeError(f"❌ ERROR: medrag is not an instance of MedRAG! Got type: {type(medrag)}")

    
    merged_result = {
        "group_id": group_id,
        "queries": []
    }

   
    for idx, query in enumerate(queries):
        options = options_list[idx] if options_list else None
        
        answer, retrieval_info, _ = medrag.answer(question=query, options=options, reranker_type=reranker_type)
        retrieval_info = retrieval_info if isinstance(retrieval_info, list) else []

        result_entry = {
            "question": query,
            "answer": answer,
            "retrieval_info": retrieval_info
        }
        merged_result["queries"].append(result_entry)

    return merged_result

# def process_dataset_with_rag(input_file, output_file, sensitive_categories, medrag, dataset_type, reranker_type):
#     """对整个数据集的 query 使用 RAG 系统处理"""
#     data = load_dataset(input_file, dataset_type)
#     print("data size",len(data))
#     # data = data[:10]
#     results = []
#     if dataset_type == "OpenQA":
#         # 🔹 **按 `Group ID` 进行分组**
#         grouped_data = {}
#         for record in data:
#             group_id = record["group_id"]
#             if group_id not in grouped_data:
#                 grouped_data[group_id] = []
#             grouped_data[group_id].append(record["question"])

#         # 🔹 **遍历每个 Group ID 进行处理**
#         for group_id, queries in tqdm(grouped_data.items(), desc="Processing OpenQA groups"):
#             result = process_with_rag_openqa(group_id, queries, medrag, reranker_type)
#             results.append(result)
#     else:
#         for record in tqdm(data, desc="Processing dataset"):
#             query = record["question"]
#             ground_truth = record["answer"] 
#            
#             options = record["options"]
#             ground_truth = record["answer"]
            
#             result = process_with_rag(query, sensitive_categories, medrag, reranker_type, options, ground_truth)
#             results.append(result)
#     # 保存结果
#     with open(output_file, "w") as f:
#         for result in results:
#             f.write(json.dumps(result) + "\n")



def process_dataset_with_rag(input_file, 
                            output_file, 
                            sensitive_categories,
                            medrag, 
                            dataset_type, 
                            reranker_type, 
                            model_name,
                            topk):
    """The query for the entire dataset is processed using the RAG system"""
    print("dataset_type in process_dataset_with_rag",dataset_type)
    data = load_dataset(input_file, dataset_type)
    print("data size", len(data))

    results = []
    if dataset_type == "OpenQA":
        # 🔹 **按 `Group ID` 进行分组**
        grouped_data = {}
        for record in data:
            group_id = record["group_id"]
            if group_id not in grouped_data:
                grouped_data[group_id] = []
            grouped_data[group_id].append(record["question"])

        # 🔹 **遍历每个 Group ID 进行处理**
        for group_id, queries in tqdm(grouped_data.items(), desc="Processing OpenQA groups"):
            result = process_with_rag_openqa(group_id, queries, medrag, reranker_type)
            results.append(result)
    elif dataset_type in ["MedQA", "MedMCQA","MMLU"]
        for record in tqdm(data, desc="Processing dataset"):
            query = record["question"]

            if dataset_type in ["MedQA", "MedMCQA","MMLU"]:
                options = record["options"]  
                ground_truth = record["answer"]

                if ground_truth is None:
                    print(f"Warning: No matching ground truth found for '{answer_content}' in question '{query}'")
            else:
                ground_truth = None

            result = process_with_rag(query, sensitive_categories, medrag, reranker_type, options, ground_truth, topk)
            results.append(result)
    # output_file = output_file.split(".jsonl")[0]
    # Save results
    with open(output_file, "w") as f:
        for result in results:
            f.write(json.dumps(result) + "\n")




if __name__ == "__main__":
    import os

   
    parser = argparse.ArgumentParser(description="Process and evaluate RAG on medical datasets.")
    parser.add_argument("--input_file", type=str, required=True, help="Path to the input dataset file.")
    parser.add_argument("--output_file", type=str, default="rag_results.jsonl", help="Path to save the RAG results.")
    parser.add_argument("--dataset_type", type=str, required=True, choices=["MedQA", "MedMCQA", "MMLU","OpenQA"], help="Type of dataset.")
    parser.add_argument("--reranker_type", type=str, required=True, choices=["cot", "counter_factoral", "adversarial_prompt","plain"], default="plain",help="Type of dataset.")
    parser.add_argument("--model", type=str, choices=["llama3.18b", "deepseekr1_8b"], default="llama3.18b",help="Type of model.")
    parser.add_argument("--topk", type=int, default=10, help="How many retrieved docs")
    args = parser.parse_args()
     # Define base directories
    # BASE_DIR = "/data_vault/pittnail/yuj49/rag_reason/MedRAG"
    import os

    # Get the current working directory
    BASE_DIR = os.getcwd() # "/data_vault/pittnail/yuj49/rag_reason/MedRAG/src"
    OUTPUT_DIR = os.path.join(BASE_DIR, "result")

    # Update paths dynamically
    args.input_file = os.path.join(BASE_DIR, args.input_file) if not os.path.isabs(args.input_file) else args.input_file
    args.output_file = os.path.join(OUTPUT_DIR, f"rag_results_{args.dataset_type.lower()}_{args.model}.jsonl") if not os.path.isabs(args.output_file) else args.output_file

    from medrag import MedRAG as oldMedRAG
    from medrag_clean import  MedRAG 
    # Init rag
    llm_names = ["OpenAI/gpt-3.5-turbo-16k",
                "/data_vault/pittnail/yuj49/rag_reason/llama3.1_8B",
                "/data_vault/pittnail/yuj49/rag_reason/deepseek_r1"]
    if args.model == "llama3.18b":
        medrag = MedRAG(llm_name=llm_names[1])
    elif args.model == "deepseekr1_8b":
        medrag = MedRAG(llm_name=llm_names[2])
    model_name =args.model
    process_dataset_with_rag(args.input_file, args.output_file, sensitive_categories, medrag, args.dataset_type, args.reranker_type, model_name, args.topk)
