import os
import json
import logging
from vllm import LLM, SamplingParams
from utils import RetrievalSystem, DocExtracter  


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MedRAG")

class MedRAG:
    def __init__(self, llm_name, retriever_name="MedCPT", corpus_name="Textbooks", db_dir="./corpus"):
        """
        Initialize vLLM & Document Retrieval
        """
        self.model_path = llm_name
        logger.info("🚀 Loading vLLM model...")
        self.llm = LLM(
            model=self.model_path,
            dtype="float16",
            tensor_parallel_size=1,
            gpu_memory_utilization=0.9,
            enforce_eager=True,
            max_model_len=8192,
            enable_chunked_prefill=False,
            disable_custom_all_reduce=True
        )
        logger.info("✅ vLLM model loaded!")


        logger.info("🔍 Initializing retrieval system...")
        self.retriever = RetrievalSystem(retriever_name, corpus_name, db_dir, cache=True)
        self.doc_extractor = DocExtracter(db_dir=db_dir, cache=True, corpus_name=corpus_name)
        logger.info("✅ Retrieval system ready!")

    def retrieve_documents(self, query, k=10):
        """
        Search for related documents
        """
        retrieved_snippets, _ = self.retriever.retrieve(query, k=k)
        docs = [f"Document [{i}] (Title: {s['title']}) {s['content']}" for i, s in enumerate(retrieved_snippets)]
        return "\n".join(docs) if docs else "No relevant documents found.", docs

    def generate_response(self, prompt):
        """
        Generate Answers
        """
        sampling_params = SamplingParams(
            temperature=0.7,
            top_p=0.9,
            max_tokens=512
        )
        
        outputs = self.llm.generate([prompt], sampling_params)
        print("\n🔍 vLLM Output (Full Response):")
        # print(outputs)
        return outputs[0].outputs[0].text.strip()

    def answer(self, question, options=None,reranker_type="cot", topk=10):
        """
        Processing questions, generating multiple choice answers
        when options are available and open-ended answers when no options are available
        """
        if reranker_type=="cot":
            bias_removal_prompt = """
            Before answering, think step by step:
            1. Identify any potential biases in the question or context.
            2. Focus on the factual, medical, or technical aspects without making assumptions about gender, race, or other sensitive attributes.
            3. Structure the answer in an objective and evidence-based manner.

            Now, provide a response following these principles.
            """
        elif reranker_type == "counter_factoral":
            bias_removal_prompt = """
                Please provide three different perspectives when answering this question:
                1. A general unbiased scientific answer.
                2. An answer assuming the subject is from a different demographic group.
                3. An answer assuming the subject is from yet another demographic group.

                Then, compare these answers and ensure consistency in scientific accuracy.
                """
        elif reranker_type == "adversarial_prompt":
            bias_removal_prompt = """
            Please answer this question in an unbiased manner.

            Here are some biased examples to avoid:
            - "Because men are stronger, they..."
            - "Women are naturally better at..."

            Do NOT include such statements. Instead, focus on neutral, evidence-based reasoning.
            """
        elif reranker_type == "plain":
            bias_removal_prompt = ""

        documents_str, documents_list= self.retrieve_documents(question, k=topk)

        if options:
            formatted_options = "\n".join([f"{key}. {val}" for key, val in options.items()])
            prompt = f"""
            You are a medical assistant. Answer the following multiple-choice question in JSON format based strictly on the provided documents.

            ### Relevant Documents:
            {documents_str}

            ### Question:
            {question}

            ### Options:
            {formatted_options}

            ### Output format example:
           
                "answer_choice": "A"
           
            {bias_removal_prompt}
            ### Answer:
            """
        else:
            prompt = f"""
            You are a medical assistant. Answer the following open-ended question in JSON format based strictly on the provided documents.

            ### Relevant Documents:
            
            {documents_str}

            ### Question:
            {question}

            ### Output format example:
            "answer": "Detailed answer here..."
           
            {bias_removal_prompt}
            ### Answer:
            """

  
        response = self.generate_response(prompt)
        
        retrieved_snippets = documents_list
        scores = [1.0] * len(retrieved_snippets)
        return response, retrieved_snippets, scores


if __name__ == "__main__":
    model_path = "/data_vault/pittnail/yuj49/rag_reason/llama3.1_8B"  
    medrag = MedRAG(model_path)


    question = "Which of the following is a symptom of a heart attack?"
    options = {"A": "Chest pain", "B": "Fever", "C": "Shortness of breath", "D": "Rash"}
    answer = medrag.answer(question, options)
    
    print("\n📝 Multiple Choice Answer:", answer)

    open_question = "What are the symptoms of a heart attack?"
    open_answer = medrag.answer(open_question)
    print("\n📝 Open-ended Answer:", open_answer)
