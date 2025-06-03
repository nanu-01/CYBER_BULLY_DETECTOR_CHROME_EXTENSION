from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline
import torch

app = FastAPI()

# Enable CORS for Chrome Extension access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the pipeline (getting raw logits for multi-label processing)
model_id = "anu111222/cyberbully-detector"
text_classifier = pipeline("text-classification", model=model_id, return_tensors=True)

@app.get("/")
def read_root():
    return {"message": "Cyberbullying detector is running."}

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    text = data.get("text", "")

    if not text.strip():
        return {"error": "No text provided"}

    # Get model output (raw logits)
    output = text_classifier(text)
    logits = output[0]["logits"]

    # Apply sigmoid activation for multi-label classification
    probs = torch.sigmoid(torch.tensor(logits)).tolist()

    # Get label mapping if available
    id2label = text_classifier.model.config.id2label  # Example: {0: "toxic", 1: "insult", ...}

    # Apply threshold to determine toxic categories
    threshold = 0.5
    predicted_labels = [id2label[i] for i, p in enumerate(probs) if p >= threshold]

    return {"predicted_labels": predicted_labels}
