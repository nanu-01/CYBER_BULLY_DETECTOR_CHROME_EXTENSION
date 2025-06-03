from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from transformers import pipeline

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize text classification pipeline
model_id = "anu111222/cyberbully-detector"  # Your model
text_classifier = pipeline("text-classification", model=model_id, device=0)  # Use GPU if available

@app.get("/")
def read_root():
    return {"message": "Cyberbullying detector is running."}

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    text = data.get("text", "")

    if not text.strip():
        return {"error": "No text provided"}

    # Use pipeline for prediction
    predictions = text_classifier(text, truncation=True)

    # Extract labels based on confidence threshold
    threshold = 0.5
    predicted_labels = [
        pred["label"]
        for pred in predictions
        if pred["score"] >= threshold
    ]

    return {"predicted_labels": predicted_labels}
