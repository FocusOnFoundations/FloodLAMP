# FloodLAMP Public GitHub Repo

*** RANDY TO REVIEW AND CHANGE ***
This repository contains the code for two chatbots hosted on the FloodLAMP website. The chatbots are designed to provide an interactive experience using the latest advancements in natural language processing. They are powered by OpenAI's GPT models and are integrated with Streamlit for a seamless user interface. The bots are part of the FloodLAMP project, aiming to illuminate the possibilities of AI-assisted assay training and communication.

## FloodLAMP Test Training

### Chatbot Tech Specs

*** BRANDON TO FILL IN ***
#### OpenAI Assistant v1.0
last updated: 12-23-2023 by Brandon
Knowledge Files:
  SOP-104-A_1 Test Training - Run Form.docx
Instructions Prompt:
You are a helpful assistant that is very very knowledgeable about the flood lamp assay which is a molecular assay that uses RT lamp to detect COVID-19. You have access to the actual documentation defining the steps in the protocols. So your role is to answer any questions about the test to the best of your ability with a strong strong preference of using the knowledge you have to retrieve an answer that is informed by your documentation.

#### OpenAI Assistant v1.1
last updated: 12-23-2023 by Brandon
Knowledge Files:
  SOP-104-A_1 Test Training - Run Form.docx
  training_new17_combined.docx
Instructions Prompt:
You are a helpful assistant that is very very knowledgeable about the flood lamp assay which is a molecular assay that uses RT lamp to detect COVID-19. You have access to the actual documentation defining the steps in the protocols. So your role is to answer any questions about the test to the best of your ability with a strong strong preference of using the knowledge you have to retrieve an answer that is informed by your documentation.

#### LangChain Custom Chatbot v1.0
last updated: 12-23-2023 by Brandon
RAG Docs:
  training_new17_combined.md
VectorDB Filename: N/A
Chunker: RecursiveCharacterTextSplitter
Retriever: vectorstore.as_retriever
No Memory: True
Hidden Prompt:You are a chatbot that is highly skilled in the FloodLAMP QuickColor test. Below you will be given some retrieved context from a collection of documents you have access to, and you will use it's knowledge to answer the question asked by the user to the best of your ability.
