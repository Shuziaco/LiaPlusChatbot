from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import pipeline
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import threading

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load sentimental model
sentiment_model = pipeline(
    task="sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    revision="714eb0f" 
    )
conversation_history = []
history_lock = threading.Lock()

class ChatMessage(BaseModel):
    text: str

# Serve UI
@app.get("/")
def serve_ui():
    return FileResponse("static/chatbot.html")

@app.post("/chat")
def chat(msg: ChatMessage):
    user_msg = msg.text.strip()
    if not user_msg:
        raise HTTPException(status_code=400, detail = "Empty message")

    # Analyze sentiment
    result = sentiment_model(user_msg)[0]
    label = result["label"]
    score = float(result["score"])

    entry = {
        "user": user_msg,
        "sentiment": label,
        "score": score,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    with history_lock:
        conversation_history.append(entry)
        
        
            

    if label == "NEGATIVE":
        bot_reply = "I'm here for you. Tell me what happened."
    elif label == "POSITIVE":
        bot_reply = "That's good to hear!"
    else:
        bot_reply = "I understand. Go on."
    
    with history_lock:
        conversation_history[-1]["bot"] = bot_reply


    return {
        "reply": bot_reply,
        "sentiment_label": label,
        }

@app.get("/sentiment_summary")
def conversation_sentiment():
    
    if not conversation_history:
        return {"error": "No conversation yet"}

    positive = sum(1 for msg in conversation_history if msg["sentiment"] == "POSITIVE")
    negative = sum(1 for msg in conversation_history if msg["sentiment"] == "NEGATIVE")
    neutral = sum(1 for msg in conversation_history if msg["sentiment"] not in ["POSITIVE", "NEGATIVE"])


    # Overall sentiment decision (counts only, NOT score)
    if positive > negative:
        overall = "POSITIVE"
    elif negative > positive:
        overall = "NEGATIVE"
    else:
        overall = "NEUTRAL"

    return {
        "total_messages": len(conversation_history),
        "positive_messages": positive,
        "negative_messages": negative,
        "neutral_messages": neutral,
        "overall_sentiment": overall
    }