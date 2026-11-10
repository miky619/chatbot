import streamlit as st
import utils_1

st.title("STREAMLIT CHATBOT")

model = "gemma3:1b"

if "messages" not in st.session_state:
    st.session_state["messages"] = [{'role': 'ai', "content": "How Can I Help You?"}]


if st.session_state["messages"][-1]["role"] == "user":
    st.session_state["messages"].append({"role": "ai", "content": "Stopped."})


if st.sidebar.button("Clear History"):
    st.session_state["messages"] = [{'role': 'ai', "content": "How Can I Help You?"}]


if st.sidebar.button("Summarize & Save Chat"):
    chat_text = ""
    for msg in st.session_state["messages"]:
        chat_text = chat_text + msg["role"] + ": " + msg["content"] + "\n"

   
    with open("chat.txt", "w", encoding="utf-8") as f:
        f.write(chat_text)

    summary_prompt = (
        "Summarize the following conversation between a user and an AI. "
        "Write the main topic, the user's main questions, and the key points of the answers. "
        "Keep it short (maximum 100 words) and do not add anything that is not in the conversation.\n\n"
        "Conversation:\n" + chat_text
    )
    with st.spinner("Summarizing ..."):
        summary = utils_1.call_ollama_model(summary_prompt, model)

    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    st.sidebar.success("Saved: chat.txt and summary.txt")


for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input("Enter Your Question")
if prompt:
    new_prompt = prompt #+ " Describe your answer with detail and shape"
    st.chat_message("user").write(prompt)
    st.session_state["messages"].append({"role": "user", "content": prompt})

    
    st.button("Stop")

    
    response = st.chat_message("ai").write_stream(
        utils_1.stream_ollama_model(new_prompt, model)
    )
    st.session_state["messages"].append({"role": "ai", "content": response})
