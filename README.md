FlightAI — Airline Assistant Chatbot

A conversational AI assistant for **FlightAI**, powered by [Groq](https://groq.com/) (LLaMA 3.3 70B) and built with [Gradio](https://www.gradio.app/). The bot answers airline-related queries and uses **tool calling** to fetch real-time ticket prices.

---

## Features

- 🤖 Powered by `llama-3.3-70b-versatile` via the Groq API
- 💬 Interactive chat UI using Gradio
- 🛠️ Tool calling support — the model can invoke a `get_ticket_price` function to look up fares
- 🌍 Supports destinations: London, Paris, Tokyo, Berlin
- ⚡ Low-latency inference via Groq's fast inference engine

---
## How It Works

1. The user sends a message through the Gradio chat interface.
2. The message (along with conversation history) is sent to the Groq LLM.
3. If the model determines a ticket price is needed, it triggers the `get_ticket_price` tool.
4. The tool result is sent back to the model, which formulates a final natural-language response.

**Supported cities and prices:**

| City | Price |
|---|---|
| London | $799 |
| Paris | $899 |
| Tokyo | $1,400 |
| Berlin | $499 |

---

## Example Interaction

```
User:  How much does a ticket to Tokyo cost?
Bot:   A return ticket to Tokyo is priced at $1,400.
```

## Requirements

```
openai
gradio
python-dotenv
```

> Install with: `pip install openai gradio python-dotenv`
---

## Extending the Bot

- **Add more destinations:** Update the `ticket_prices` dictionary in `app.py`.
- **Add more tools:** Define a new function + JSON schema and add it to the `tools` list.
- **Switch models:** Change the `MODEL` variable to any Groq-supported model.
- **Use Ollama locally:** Uncomment the Ollama section and update `MODEL` accordingly.

---







<img width="1372" height="712" alt="image" src="https://github.com/user-attachments/assets/534a6915-7fd5-4c72-9605-dc504489158f" />
