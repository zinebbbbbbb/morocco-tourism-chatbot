from langchain_community.llms import LlamaCpp
from .retriever import load_retriever
from .memory import get_memory
from .prompts import get_prompt

# Setup
retriever = load_retriever("data/finalll_dataset (1).csv")
memory = get_memory()
prompt = get_prompt()

llm = LlamaCpp(
    model_path="models/llama-2-7b-chat.Q4_K_M.gguf",
    n_gpu_layers=40,
    n_ctx=4096,
    n_batch=256,
    verbose=False,
)

llm_chain = prompt | llm

def get_context(user_input, history):
    """Enhanced retrieval that handles follow-up questions."""
    follow_up_keywords = ['more', 'else', 'other', 'another', 'also', 'what about', 'how about']
    is_follow_up = any(k in user_input.lower() for k in follow_up_keywords)

    if is_follow_up and history:
        last_user_messages = [msg.content for msg in history if msg.type == 'human'][-2:]
        main_topic = " ".join(last_user_messages)
        query = f"{main_topic} {user_input}"
    else:
        query = user_input

    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])

def chat(user_input: str):
    history = memory.load_memory_variables({})["chat_history"]
    history_str = "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in history])

    context_text = get_context(user_input, history)
    input_dict = {"context": context_text, "history": history_str, "question": user_input}

    answer = llm_chain.invoke(input_dict).strip()
    memory.save_context({"input": user_input}, {"output": answer})
    return answer
