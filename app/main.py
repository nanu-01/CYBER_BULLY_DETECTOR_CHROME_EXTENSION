from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load tokenizer & model manually
model_id = "anu111222/cyberbully-detector"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Get label mapping
id2label = model.config.id2label  # Example: {0: "toxic", 1: "insult", ...}

@app.get("/")
def read_root():
    return {"message": "Cyberbullying detector is running."}

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    text = data.get("text", "")

    if not text.strip():
        return {"error": "No text provided"}

    # Tokenize input
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True).to(device)

    # Get raw model output
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.sigmoid(logits).squeeze().cpu().tolist()  # Apply sigmoid

    # Apply threshold
    threshold = 0.5
    predicted_labels = [
        id2label[i] for i, p in enumerate(probs) if p >= threshold
    ]

    return {"predicted_labels": predicted_labels}
