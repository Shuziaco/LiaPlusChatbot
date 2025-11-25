async function sendMessage() {
    const inputBox = document.getElementById("inputBox");
    const msgText = inputBox.value.trim();
    if (!msgText) return;

    addMessage(msgText, "user", null);
    inputBox.value = "";

    const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: msgText })
    });

    const data = await response.json();

    // remove the last added user message (no sentiment)
    const messagesDiv = document.getElementById("messages");
    messagesDiv.lastElementChild.remove()

    // readded user message with sentiments
    addMessage(msgText, "user", data.sentiment_label);

    const botMessage = `${data.reply}`;
    addMessage(botMessage, "bot", null);
}


function addMessage(text, sender, sentimentLabel) {
    const messagesDiv = document.getElementById("messages");
    const msgWrapper = document.createElement("div");
    msgWrapper.className = "msg-wrapper " + sender;
      

    if (sentimentLabel && sender === "user") {
        const sentimentTag = document.createElement('div');
        sentimentTag.className = "sentiment-tag " + sentimentLabel.toLowerCase();
        sentimentTag.innerText = sentimentLabel;
        msgWrapper.appendChild(sentimentTag);
    }

    const msg = document.createElement("div");
    msg.className = "msg " + sender;
    // msg.innerHTML = text.replace(/\n/g, "<br>");  
    msg.innerText = text;

    msgWrapper.appendChild(msg)
    messagesDiv.appendChild(msgWrapper);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;

}
document.getElementById("summaryBtn").addEventListener("click", getConversationSummary);
async function getConversationSummary() {
    const res = await fetch("http://127.0.0.1:8000/sentiment_summary");
    const data = await res.json();

    if(data.error) {
        addMessage("No conversation yet.", "bot");
        return 
    }
    const summaryText = `

    **Conversation Summary**
    Total Messages: ${data.total_messages}\n
    Positive Messages: ${data.positive_messages}\n
    Negative Messages: ${data.negative_messages}\n
    Neutral Messages: ${data.neutral_messages}\n
    Overall Sentiment: ${data.overall_sentiment}
    `;
    addMessage(summaryText, "bot", null);

}