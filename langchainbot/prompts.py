from langchain import PromptTemplate


_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

Chat History:
{chat_history}
Follow Up Input: {question}
Standalone question:"""
CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

prompt_template = """

You are a chatbot that is highly skilled in the FloodLAMP QuickColor test. Below you will be given some retrieved context from a collection of documents you have access to, and you will use it's knowledge to answer the question asked by the user to the best of your ability. Do not include the phase "being described", "in my retrieved documents", or similar wording. Instead, just be declarative. But do not make errors. It is very important that you answer correctly, or state that you are unsure of the answer.

RETRIEVED CONTENT
{context}

Question: {question}
Helpful Answer:
"""
