import gradio as gr
from app.chatbot import chat

def chatbot_interface(message, history):
    # Keep the response exactly as returned by the chatbot
    response = chat(message)
    history = history + [(message, response)]
    return history, history

with gr.Blocks(css="""
    body {background-color: #D8BFA5; font-family: 'Helvetica', sans-serif;}
    .gradio-container {background-color: #D8BFA5;}
    .chatbot-message.user {background-color: #F5F0E6; color: #3E2F1C; border-radius: 12px; padding: 8px;}
    .chatbot-message.bot {background-color: #F5F0E6; color: #3E2F1C; border-radius: 12px; padding: 8px;}
    .gr-button {background-color: #C7A17A; color: white; border-radius: 8px;}
    .gr-button:hover {background-color: #B08B61;}
    .gr-textbox {border: 1px solid #C7A17A; border-radius: 8px; background-color: #F5F0E6;}
    #header {color: #3E2F1C; text-align: center; margin-bottom: 20px;}
    #footer {color: #3E2F1C; text-align: center; margin-top: 20px;}
    #tips {background-color: #F5F0E6; padding: 15px; border-radius: 10px; margin-top: 20px; border: 1px solid #C7A17A;}
    .title-emoji {font-size: 2em; margin: 0 10px;}
""") as demo:

    # Header
    gr.Markdown(
        """
        <div style="text-align: center;">
            <h1>🌍 Your Personal Morocco Travel Assistant 🕌</h1>
            <h3 style="color: #8B4513; font-style: italic;">Discover the Magic of Morocco - From Imperial Cities to Sahara Dunes</h3>
            <p style="font-size: 1.1em; margin: 15px 0;">Get expert advice on destinations, cuisine, culture, and travel tips for an unforgettable Moroccan adventure!</p>
        </div>
        """,
        elem_id="header"
    )

    # Chat interface
    chatbot_ui = gr.Chatbot(
        label="Your Travel Assistant",
        height=400,
        placeholder="Hello! I'm your Morocco travel expert. Ask me anything about traveling in Morocco!"
    )

    msg = gr.Textbox(
        placeholder="Ask me about Morocco - cities, food, culture, transportation, or anything else!",
        label="Your Message",
        lines=2,
        max_lines=5
    )

    with gr.Row():
        submit_btn = gr.Button("Send Message", variant="primary", scale=2)
        clear_btn = gr.Button("Clear Chat", variant="secondary", scale=1)

    # Tips section
    gr.Markdown(
        """
        <div id="tips">
            <h3 style="color: #8B4513; margin-top: 0;">💡 Popular Questions to Get You Started:</h3>
            <ul style="color: #3E2F1C; line-height: 1.6;">
                <li><strong>Cities & Destinations:</strong> "What are the best cities to visit in Morocco?" or "Tell me about Marrakech vs Fez"</li>
                <li><strong>Food & Cuisine:</strong> "Recommend authentic Moroccan dishes to try" or "Where can I find the best tagine?"</li>
                <li><strong>Transportation:</strong> "How do I get around Morocco?" or "Is it safe to rent a car in Morocco?"</li>
                <li><strong>Culture & Customs:</strong> "What should I know about Moroccan culture?" or "What's appropriate to wear in Morocco?"</li>
                <li><strong>Activities:</strong> "Best things to do in the Sahara Desert" or "Recommended day trips from Casablanca"</li>
            </ul>
        </div>
        """
    )

    # Events
    msg.submit(chatbot_interface, [msg, chatbot_ui], [chatbot_ui, chatbot_ui])
    msg.submit(lambda: "", None, msg)  # Clear input after sending
    submit_btn.click(chatbot_interface, [msg, chatbot_ui], [chatbot_ui, chatbot_ui])
    submit_btn.click(lambda: "", None, msg)  # Clear input after sending
    clear_btn.click(lambda: [], None, chatbot_ui, queue=False)

    # Footer
    gr.Markdown(
        """
        <div style="text-align: center; margin-top: 30px;">
            <p style="font-size: 1.1em; color: #8B4513;">🌟 Ready to explore Morocco? Start your journey with a question above! 🌟</p>
        </div>
        """,
        elem_id="footer"
    )

demo.launch()
