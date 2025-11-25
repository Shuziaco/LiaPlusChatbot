# LiaPlusChatbot
This is a basic sentimental analysis chatbot that perform sentimental analysis for every user as well as provide full sentimental summary for the whole conversation.

-Status of Tier 2: Implemented

**How to Run the Project**
1. Install dependencies
 pip install fastapi uvicorn transformers torch pydantic fastapi[all]

2. Start the FastAPI server
   uvicorn main:app --reload

3. Visit
   http://127.0.0.1:8000/

**Chosen Technologies**

**Backend**
FastAPI — high-performance Python web framework
Transformers (HuggingFace) — for sentiment classification
distilbert-base-uncased-finetuned-sst-2-english — lightweight, fast sentiment model
Uvicorn — ASGI server

**Frontend**
HTML + CSS + JavaScript
Uses fetch() API to interact with FastAPI
Custom popup sentiment tags positioned above each user bubble

**API Endpoints**
➤ POST /chat
Sends a user message and receives:
bot reply
sentiment label (POSITIVE/NEGATIVE/NEUTRAL)

➤ GET /sentiment_summary
Returns sentiment statistics only from user messages, including:
total messages
positive count
negative count
neutral count
overall sentiment label

**How Sentiment Logic Works**

1. The user message goes through DistilBERT
  result = sentiment_model(user_msg)[0]
  label = result["label"]
  score = float(result["score"])

2. The model outputs one of:
  POSITIVE
  NEGATIVE
  (rarely) NEUTRAL — handled manually

3. The backend attaches the sentiment result to conversation history:

  conversation_history.append({
      "user": user_msg,
      "sentiment": label,
      "score": score
  })

4. The chatbot responds with predefined emotional replies:
POSITIVE : "That's good to hear!"
NEGATIVE : "I'm here for you. Tell me what happened."
neutral : "I understand. Go on."

