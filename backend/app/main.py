from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

app = FastAPI()

# Load model and tokenizer
model_path = "./app/model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model.eval()

# Labels
LABELS = ['toxic', 'obscene', 'insult', 'severe_toxic', 'identity_hate', 'threat']

# Input schema
class TextInput(BaseModel):
    text: str

@app.post("/predict")
async def predict(input: TextInput):
    inputs = tokenizer(input.text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.sigmoid(outputs.logits)
        predictions = (probs >= 0.5).int().squeeze().tolist()
    predicted_labels = [label for label, pred in zip(LABELS, predictions) if pred == 1]
    return {"labels": predicted_labels if predicted_labels else ["Safe 🌼"]}
