from langchain.memory import ConversationBufferWindowMemory

def get_memory(k: int = 5):
    """
    Create a memory object that stores the last `k` turns
    of conversation. Default = 5.
    """
    return ConversationBufferWindowMemory(
        memory_key="chat_history",
        k=k,
        return_messages=True
    )
