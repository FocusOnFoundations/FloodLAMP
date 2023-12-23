from contextlib import nullcontext
import datetime
import json
import random
import sys
import os
import pinecone
import streamlit as st

from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings import OpenAIEmbeddings
from langchain import OpenAI

from langchain.chat_models.openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.callbacks import wandb_tracing_enabled
from langchain.agents import initialize_agent, load_tools
from langchain.agents import AgentType
from langchain.chains import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.conversational_retrieval.prompts import (
    CONDENSE_QUESTION_PROMPT,
    QA_PROMPT,
)
from langchain.chains.question_answering import load_qa_chain

import prompts
# Configurations
os.environ[
    "OPENAI_API_KEY"
] = st.secrets["OPENAI_API_KEY"]  # Setting OpenAI API key
os.environ["LANGCHAIN_WANDB_TRACING"] = "false"

# wandb documentation to configure wandb using env variables
# https://docs.wandb.ai/guides/track/advanced/environment-variables
# here we are configuring the wandb project name
os.environ["WANDB_PROJECT"] = "langchain-tracing"


PINECONE_API_KEY = st.secrets['PINECONE_API_KEY']  # Pinecone API key
PINECONE_ENV = "gcp-starter"  # Pinecone environment
pinecone_index_name = "floodlamp"  # Index name for Pinecone database
model = "gpt-4-1106-preview"  # Options: gpt-4, gpt-3.5-turbo (double check turbo)

# ANSI escape sequences for color formatting
ANSI_RED = "\033[91m"
ANSI_GREEN = "\033[92m"
ANSI_BLUE = "\033[94m"
ANSI_RESET = "\033[0m"


pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
index = pinecone.Index(pinecone_index_name)
embeddings = OpenAIEmbeddings()
vectorstore = Pinecone(index, embeddings.embed_query, text_key="text")


# Setting up chat model and retrieval QA chain. Use max marginal relevance search to increase diversity of results.


llm = ChatOpenAI(model_name=model, temperature=0)
retriever = vectorstore.as_retriever(search_type="mmr")


CONDENSE_QUESTION_PROMPT = prompts.CONDENSE_QUESTION_PROMPT

if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = prompts.prompt_template

QA_PROMPT = PromptTemplate(
    template=st.session_state.current_prompt, input_variables=["context", "question"]
)

question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
doc_chain = load_qa_chain(chain_type="stuff", prompt=QA_PROMPT, llm=llm, verbose=True)

qa_chain = ConversationalRetrievalChain(
    retriever=retriever,
    combine_docs_chain=doc_chain,
    question_generator=question_generator,
    return_source_documents=True,
)


print("QA chain has been successfully built.")


# Function for performing retrieval QA
def perform_retrieval_qa(question, chat_history):
    result = qa_chain({"question": question, "chat_history": chat_history})
    # print("-" * 50)
    # print(f"{ANSI_GREEN}ANSWER: {result['answer']}{ANSI_RESET}")
    # print("-" * 50)
    # for i, source in enumerate(result["source_documents"]):
    #     print(f"{ANSI_BLUE}Source ({i}): {source.metadata['source']}{ANSI_RESET}")
    #     print(f"{ANSI_BLUE}Content ({i}): {source.page_content}\n{ANSI_RESET}")
    # print("-" * 50)
    return result


def generate_new_content_id(data):
    current_num = 0
    for content in data["sessions"][0]["session_content"]:
        content_id_num = int(content["exchange_id"].split("_")[-1])
        if content_id_num > current_num:
            current_num = content_id_num
    new_id = f"exchange_{str(current_num + 1).zfill(3)}"
    return new_id


if "dl_filename" not in st.session_state:
    st.session_state.dl_filename = (
        f"training_thread_{datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')}.json"
    )
    st.session_state.user_name = False

# Check if the file exists
if not os.path.exists(st.session_state.dl_filename):
    # If the file does not exist, create it with initial JSON data
    data = {
        "thread_id": "0000",  # this should be generated dynamically in the future
        "thread_start_date": str(datetime.datetime.now().date()),
        "thread_start_time": str(datetime.datetime.now().time()),
        "sessions": [],
    }
    with open(st.session_state.dl_filename, "w") as file:
        json.dump(data, file, indent=4)

# Load the JSON data from the file
with open(st.session_state.dl_filename, "r") as file:
    data = json.load(file)
    # for key, value in data.get("response_feedbacks", {}).items():
    #     st.session_state[key] = value

    # for key, value in data.get("retrieval_feedbacks", {}).items():
    #     st.session_state[key] = value
    file_data = file.read()


if "messages" not in st.session_state:
    st.session_state.messages = []


# If a session doesn't exist, create one
if not data["sessions"]:
    data["sessions"].append(
        {
            "session_metadata": {
                "session_id": "session_001",  # this should be generated dynamically
                "code_version": "1.1",  # you should define this
                "code_description": "QA Retrieval",  # you should define this
                "code_details": {
                    "splitter": "",
                    "retriever": "mmr vectorstore",
                    "prompts": {
                        "QA_PROMPT": st.session_state.current_prompt,
                        "CONDENSE_QUESTION_PROMPT": prompts._template,
                    },
                    "chains": "Conversational Retrieval Chain",
                },
            },
            "session_content": [],
        }
    )


if __name__ == "__main__":
    st.title("FloodLAMP Test Training Bot")
    st.subheader(
        "A chatbot to answer questions about the FloodLAMP QuickColor test"
    )
    # To explore these ideas through a linked set of notes we're building out, please visit the
    st.markdown(
        ""
    )
    st.markdown(
        "A project by FloodLAMP Biotechnologies, PBC."
    )
    # st.markdown(
    #     "Heavily inspired by the work of [Andy M](https://andymatuschak.org/) and [thebeginningofinfinity.xyz](https://thebeginningofinfinity.xyz/)"
    # )


col1, col2 = st.columns(2)

with col1:
    review_fields = st.toggle("Review Fields")
if not st.session_state.user_name:
    with col2:
        user_name = st.text_input("Enter your name (optional)")
        if user_name is not "":

            def insert_string(original_string, insert_string, position):
                return (
                    original_string[:position]
                    + insert_string
                    + original_string[position:]
                )

            # Usage
            original_string = st.session_state.dl_filename
            insertion_string = user_name + "_"
            position = 12
            new_string = insert_string(original_string, insertion_string, position)
            st.session_state.dl_filename = new_string
            st.session_state.user_name = True

last_i = None  # Initialize last_i

if review_fields:
    response_feedback_areas = {}
    retrieval_feedback_areas = {}
    for i, message in enumerate(st.session_state.messages):
        # Create two columns

        # Add the chat message to the first column

        avatar = message["avatar"] if "avatar" in message else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            if "sources" in message and message["role"] == "training_bot":
                with st.expander("Sources"):
                    for j, source in enumerate(message["sources"], start=1):
                        st.markdown(f"**Source ({j}):** {source['source']}")
                        st.markdown(f"**Content ({j}):** {source['content']}\n")

        if message["role"] == "training_bot":
            # For response feedback
            response_key = f"response_feedback_{i}"
            # if response_key not in st.session_state:
            #     st.session_state[response_key] = "Default text"
            response_feedback_areas[response_key] = st.text_area(
                "Response Feedback",
                value=st.session_state.messages[i]["response_feedback"],
                key=response_key,
            )

            # For retrieval feedback
            retrieval_key = f"retrieval_feedback_{i}"
            # if retrieval_key not in st.session_state:
            #     st.session_state[retrieval_key] = "Default text"

            retrieval_feedback_areas[retrieval_key] = st.text_area(
                "Retrieval Feedback",
                value=st.session_state.messages[i]["retrieval_feedback"],
                key=retrieval_key,
            )
        last_i = i  # Update last_i

else:
    # Display chat messages from history on app rerun
    for i, message in enumerate(st.session_state.messages):
        avatar = message["avatar"] if "avatar" in message else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
            if "sources" in message and message["role"] == "training_bot":
                with st.expander("Sources"):
                    for j, source in enumerate(message["sources"], start=1):
                        st.markdown(f"**Source ({j}):** {source['source']}")
                        st.markdown(f"**Content ({j}):** {source['content']}\n")


# Generate the timestamped filename
chat_history = []
question = st.chat_input("Please enter a question or statement")

if question:
    user = st.chat_message("User")
    user.write(question)
    st.session_state.messages.append({"role": "user", "content": question})
    with st.spinner("Thinking..."):
        result = perform_retrieval_qa(question, chat_history)
    training_bot = st.chat_message(
        name="Training Bot"
    )
    training_bot.markdown(result["answer"])
    response = result["answer"] + "\n"
if question:
    with st.expander("Sources"):
        sources = [
            {
                "chunk_num": i + 1,
                "source": source.metadata["source"],
                "content": source.page_content,
            }
            for i, source in enumerate(result["source_documents"])
        ]
        for i, source in enumerate(result["source_documents"], start=1):
            st.markdown(f"**Source ({i}):** {source.metadata['source']}")
            st.markdown(f"**Content ({i}):** {source.page_content}\n")
            response += f"\n**Source ({i}):** {source.metadata['source']}"
            response += f"\n**Content ({i}):** {source.page_content}\n"

    st.session_state.messages.append(
        {
            "role": "training_bot",
            "content": result["answer"],
            "sources": sources,
            "response_feedback": "",
            "retrieval_feedback": "",
        }
    )
    if review_fields:
        response_key = f"response_feedback_{last_i+2}"
        # if response_key not in st.session_state:
        #     st.session_state[response_key] = "Default text"
        print(last_i + 1)
        print(len(st.session_state.messages))
        print(st.session_state.messages[last_i + 2]["response_feedback"])
        response_feedback_areas[response_key] = st.text_area(
            "Response Feedback",
            value=st.session_state.messages[last_i + 2]["response_feedback"],
            key=response_key,
        )

        # For retrieval feedback
        retrieval_key = f"retrieval_feedback_{last_i+2}"
        # if retrieval_key not in st.session_state:
        #     st.session_state[retrieval_key] = "Default text"

        response_feedback_areas[retrieval_key] = st.text_area(
            "Retrieval Feedback",
            value=st.session_state.messages[last_i + 2]["retrieval_feedback"],
            key=retrieval_key,
        )

    session_content_entry = {
        "exchange_id": generate_new_content_id(data),
        "object": "DOES THIS DO ANYTHING????",
        "created": str(datetime.datetime.now()),
        "model": "gpt-4",  # you should define this
        "choices": [
            {
                "index": 0,
                "message": {"role": "User", "content": question},
                "finish_reason": "completed",
            },
            {
                "index": 1,
                "message": {"role": "Bot", "content": result["answer"]},
                "finish_reason": "completed",
            },
        ],
        "usage": {
            # this is a simplistic calculation
            "prompt_tokens": "",
            "completion_tokens": "",
            "total_tokens": "",
        },
        "under_the_hood": {
            "retrieved_chunks": [
                {
                    "chunk_num": i + 1,
                    "source": doc.metadata["source"],
                    "content": doc.page_content,
                    "chunk_score": "",
                    "chunk_note": "",
                }
                for i, doc in enumerate(result["source_documents"])
            ]
        },
        "review": {
            "reviewer_name": "",
            "response_score": "",
            "retrieval_score": "",
            "review_note": "",
            "response_feedback": "",
            "retrieval_feedback": "",
        },
    }

    # Append to session content
    data["sessions"][0]["session_content"].append(session_content_entry)
    chat_history.extend([(question, result["answer"])])

    # Save to JSON
    with open(st.session_state.dl_filename, "w") as file:
        json.dump(data, file, indent=4)
    # Provide the download button for the JSON
    with open(st.session_state.dl_filename, "r") as file:
        file_data = file.read()
    # Before uploading the file



# Check if the file exists
if not os.path.exists(st.session_state.dl_filename):
    # If the file does not exist, create it
    with open(st.session_state.dl_filename, "w") as file:
        json.dump(data, file, indent=4)

if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

import pprint


def save_feedback_in_state():
    # pprint.PrettyPrinter(response_feedback_areas)
    for i, message in enumerate(st.session_state.messages):
        if st.session_state.messages[i]["role"] == "training_bot":
            st.session_state.messages[i]["response_feedback"] = response_feedback_areas[
                f"response_feedback_{i}"
            ]
            st.session_state.messages[i][
                "retrieval_feedback"
            ] = retrieval_feedback_areas[f"retrieval_feedback_{i}"]


def update_json_with_feedback():
    for i, message in enumerate(st.session_state.messages):
        if st.session_state.messages[i]["role"] == "training_bot":
            j = int((i - 1) / 2)
            pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(data["sessions"][0]["session_content"])
            print(j)
            print(
                f"session content is this long: ",
                {len(data["sessions"][0]["session_content"])},
            )
            data["sessions"][0]["session_content"][j]["review"][
                "response_feedback"
            ] = st.session_state.messages[i]["response_feedback"]
            data["sessions"][0]["session_content"][j]["review"][
                "retrieval_feedback"
            ] = st.session_state.messages[i]["retrieval_feedback"]
    with open(st.session_state.dl_filename, "w") as file:
        json.dump(data, file, indent=4)
    with open(st.session_state.dl_filename, "r") as file:
        file_data = file.read()


with st.container():
    # Create two columns
    col1, col2, col3 = st.columns(3)

    # Add the download button to the first column
    with col1:
        with open(st.session_state.dl_filename, "r") as file:
            file_data = file.read()

        st.download_button(
            label="Download JSON File",
            data=file_data,
            file_name=st.session_state.dl_filename,
            mime="application/json",
        )

    # Add the "Change Prompt" button to the second column
    with col2:
        if st.download_button(
            "Change Prompt", file_data, st.session_state.dl_filename, "application/json"
        ):
            st.session_state.button_clicked = True

    with col3:
        if review_fields:
            if st.button("Save"):
                save_feedback_in_state()
                update_json_with_feedback()



if st.session_state.button_clicked:
    with st.container():
        # Create placeholders for the text area and the button
        text_area_placeholder = st.empty()
        button_placeholder = st.empty()

        new_prompt = text_area_placeholder.text_area(
            "Current Prompt: ", value=st.session_state.current_prompt, height=400
        )
        if button_placeholder.button("Accept new Prompt"):
            st.session_state.current_prompt = new_prompt
            del st.session_state["dl_filename"]
            del st.session_state["button_clicked"]

            # Clear the placeholders
            text_area_placeholder.empty()
            button_placeholder.empty()

            # Clear the chat messages
            st.session_state.messages.clear()
            if "dummy_counter" not in st.session_state:
                st.session_state.dummy_counter = 0
            st.session_state.dummy_counter += 1


if "FILE_UPLOADED" not in st.session_state:
    st.session_state.FILE_UPLOADED = False


if st.session_state.FILE_UPLOADED == False:
    with st.expander("Upload a JSON file"):
        with st.form("my-form", clear_on_submit=True):
            uploaded_file = st.file_uploader(
                "uploader", type="json", label_visibility="hidden"
            )
            submitted = st.form_submit_button("Submit")
    if uploaded_file is not None:
        st.session_state.dl_filename = uploaded_file.name

        data = json.load(uploaded_file)
        if "sessions" in data:
            st.session_state.current_prompt = data["sessions"][0]["session_metadata"][
                "code_details"
            ]["prompts"]["QA_PROMPT"]
            st.session_state.messages = []
            for content in data["sessions"][0]["session_content"]:
                # for under_the_hood in content["under_the_hood"]["retrieved_chunks"]:
                #     source = under_the_hood["source"]
                #     content = under_the_hood["content"]
                st.session_state.messages.append(
                    {
                        "role": "User",
                        "content": content["choices"][0]["message"]["content"],
                    }
                )

                st.session_state.messages.append(
                    {
                        "role": "training_bot",
                        "content": content["choices"][1]["message"]["content"],
                        "sources": content["under_the_hood"]["retrieved_chunks"],
                        "avatar": "https://pbs.twimg.com/profile_images/925701269041401857/ff6NE-H-_400x400.jpg",
                        "response_feedback": content["review"]["response_score"],
                        "retrieval_feedback": content["review"]["retrieval_score"],
                    }
                )
            st.session_state.FILE_UPLOADED = True
            st.experimental_rerun()

            # uploaded_file = None

        else:
            st.error("Invalid JSON file. The file does not contain 'sessions' key.")
st.write("Currently there is no memory, each entry is independent.")
