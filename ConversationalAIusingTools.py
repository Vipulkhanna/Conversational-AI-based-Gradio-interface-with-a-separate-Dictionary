import os
import json
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import traceback

load_dotenv(override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")
groq_url = "https://api.groq.com/openai/v1"
groq_api_key=""
groq = OpenAI(api_key=groq_api_key, base_url=groq_url)


#ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
#ollama_api_key = os.getenv("OLLAMA_API_KEY", "ollama")
#ollama = OpenAI(base_url=ollama_base_url, api_key=ollama_api_key)

MODEL = "llama-3.3-70b-versatile"

system_message = """
You are a helpful assistant for an Airline called FlightAI.
Give short, courteous answers, no more than 1 sentence.
Always be accurate. If you don't know the answer, say so.
"""

ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}

def get_ticket_price(destination_city):
    print(f"Tool called for city {destination_city}")
    price = ticket_prices.get(destination_city.lower(), "Unknown ticket price")
    return f"The price of a ticket to {destination_city} is {price}"


# There's a particular dictionary structure that's required to describe our function:

price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}


# And this is included in a list of tools:

tools = [{"type": "function", "function": price_function}]

def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    if tool_call.function.name == "get_ticket_price":
        arguments = json.loads(tool_call.function.arguments)
        city = arguments.get('destination_city')
        price_details = get_ticket_price(city)
        response = {
            "role": "tool",
            "content": price_details,
            "tool_call_id": tool_call.id
        }
    return response


def chat(message, history):
    try:
        history = [{"role":h["role"], "content":h["content"]} for h in history]
        messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
        response = groq.chat.completions.create(model=MODEL, messages=messages, temperature=0, tools=tools)

        if response.choices[0].finish_reason=="tool_calls":
            message = response.choices[0].message
            try:
                tool_response = handle_tool_call(message)
            except Exception as e:
                print(f"Error handling tool call: {e}")
                traceback.print_exc()
                return f"An error occurred while handling the tool call: {e}"

            messages.append(message)
            messages.append(tool_response)
            
            try:
                response = groq.chat.completions.create(model=MODEL, messages=messages)
            except Exception as e:
                print(f"Error in second LLM call after tool execution: {e}")
                traceback.print_exc()
                return f"An error occurred in the LLM response after tool execution: {e}"

        return response.choices[0].message.content
    except Exception as e:
        print(f"An unexpected error occurred in the chat function: {e}")
        traceback.print_exc()
        return f"An unexpected error occurred: {e}"

gr.ChatInterface(fn=chat, type="messages").launch()
