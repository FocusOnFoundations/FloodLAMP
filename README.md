# FloodLAMP Public GitHub Repo

This is a Work in Progress and not yet ready for others to use. We expect to update this mid 2024 as we complete and publish other related work.

This repository contains the code for two chatbots hosted on the FloodLAMP website. The chatbots are designed to provide an interactive experience using the latest advancements in natural language processing. They are powered by OpenAI's GPT models and are integrated with Streamlit for a seamless user interface. The bots are part of the FloodLAMP project, aiming to illuminate the possibilities of AI-assisted assay training and communication.

## OpenAI Assistant Notes
docx - use download docx from google drive (if get error, then convert to google doc, then back to docx)

## Langchain Custom Chatbot


## FloodLAMP Test Training

### Chatbot Tech Specs

#### OpenAI Assistant v1.2
last updated: 12-29-2023 by Randy with combined docx having only transcripts
Model: gpt-4-1106-preview
Knowledge Files:
  SOP-104-A_1 Test Training - Run Form.docx
  training_new17_md_combined.docx  # new version with just transcripts and in order
Instructions Prompt:
You are a helpful assistant that is very very knowledgeable about the FloodLAMP assay which is a molecular assay that uses a LAMP amplification reaction to detect COVID-19. You have access to the actual documentation defining the steps in the protocols. So your role is to answer any questions about the test to the best of your ability with a strong strong preference of using the knowledge you have to retrieve an answer that is informed by your documentation.

#### OpenAI Assistant v1.1
last updated: 12-29-2023 by Randy
Model: gpt-4-1106-preview
Knowledge Files:
  SOP-104-A_1 Test Training - Run Form.docx
  training_new17_combined.docx
Instructions Prompt:
You are a helpful assistant that is very very knowledgeable about the FloodLAMP assay which is a molecular assay that uses a LAMP amplification reaction to detect COVID-19. You have access to the actual documentation defining the steps in the protocols. So your role is to answer any questions about the test to the best of your ability with a strong strong preference of using the knowledge you have to retrieve an answer that is informed by your documentation.

#### OpenAI Assistant v1.0
last updated: 12-23-2023 by Brandon
Model: gpt-4-1106-preview
Knowledge Files:
  SOP-104-A_1 Test Training - Run Form.docx
Instructions Prompt:
You are a helpful assistant that is very very knowledgeable about the flood lamp assay which is a molecular assay that uses RT lamp to detect COVID-19. You have access to the actual documentation defining the steps in the protocols. So your role is to answer any questions about the test to the best of your ability with a strong strong preference of using the knowledge you have to retrieve an answer that is informed by your documentation.


#### LangChain Custom Chatbot v1.1
last updated: 12-29-2023 by Randy
LLM Model: OpenAI gpt-4-1106-preview
RAG Docs:
  SOP-104-A_1 Test Training - Run Form.md
  FloodLAMP Training Video 01 - Intro.md
  FloodLAMP Training Video 02 - Safety and Contamination.md
  FloodLAMP Training Video 03 - 1X Inactivation Saline Solution Prep.md
  FloodLAMP Training Video 04 - Inactivation Reaction.md
  FloodLAMP Training Video 05 - Reaction Mix Prep.md
  FloodLAMP Training Video 06 - Thawing Reactions.md
  FloodLAMP Training Video 07 - Adding Samples to Reaction.md
  FloodLAMP Training Video 08 - Intaking Samples.md
  FloodLAMP Training Video 09 - Resulting.md
  FloodLAMP Training Video 10 - Logging Run.md
  FloodLAMP Training Video 11 - Large Scale Clean and Dispense.md
  FloodLAMP Training Video 12 - Large Scale Inactivation.md
  FloodLAMP Training Video 13 - Reaction Plate Prep.md
  FloodLAMP Training Video 14 - Plate Processing.md
  FloodLAMP Training Video 15 - (Appendix) Setup.md
  FloodLAMP Training Video 16 - (Appendix) Pipette Cleaning.md
  FloodLAMP Training Video 17 - (Appendix) Dispensers.md
VectorDB Filename: floodlamp (pinecone)
Chunker: RecursiveCharacterTextSplitter
Retriever: vectorstore.as_retriever
No Memory
Hidden Prompt: You are a chatbot that is highly skilled in the FloodLAMP QuickColor test. Below you will be given some retrieved context from a collection of documents you have access to, and you will use it's knowledge to answer the question asked by the user to the best of your ability. Do not include the phase "being described", "in my retrieved documents", or similar wording. Instead, just be declarative. But do not make errors. It is very important that you answer correctly, or state that you are unsure of the answer.

#### LangChain Custom Chatbot v1.0
Hidden Prompt: You are a chatbot that is highly skilled in the FloodLAMP QuickColor test. Below you will be given some retrieved context from a collection of documents you have access to, and you will use it's knowledge to answer the question asked by the user to the best of your ability.
