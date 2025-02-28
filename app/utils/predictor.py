import logging
import os
from transformers import (
    AutoTokenizer,
    pipeline,
    AutoModelForSequenceClassification,
)

SCORES_MAPPING = {
    "S": "sexual",
    "H": "hate",
    "V": "violence",
    "HR": "harassment",
    "SH": "self-harm",
    "S3": "sexual/minors",
    "H2": "hate/threatening",
    "V2": "violence/graphic",
    "OK": "OK",
}

logger = logging.getLogger(__name__)

MODEL_NAME = "KoalaAI/Text-Moderation"
# I'm assuming it's okay to store the models locally. Alternatively, I could upload them to cloud storage (e.g., S3 or GCS).
# Another option would be to fetch the predictions from Hugging Face without downloading the models,
# but 1) it was a requirement in the exercise, and 2) downloading the models ensures the model remains unchanged, maintaining consistency.
MODEL_DIR = "./app/models/koala_ai_text_moderation"


class Predictor:
    model = None
    tokenizer = None
    classifier = None

    @classmethod
    def load_model(cls):
        """Load the model and tokenizer only once."""
        if cls.model is None or cls.tokenizer is None:
            if not os.path.exists(MODEL_DIR) or not os.listdir(MODEL_DIR):
                logger.info("Downloading the model...")
                cls.model = AutoModelForSequenceClassification.from_pretrained(
                    MODEL_NAME, cache_dir=MODEL_DIR
                )
                cls.tokenizer = AutoTokenizer.from_pretrained(
                    MODEL_NAME, cache_dir=MODEL_DIR
                )
                cls.model.save_pretrained(MODEL_DIR)
                cls.tokenizer.save_pretrained(MODEL_DIR)
            else:
                logger.info(f"Model already exists at {MODEL_DIR}")
                cls.model = AutoModelForSequenceClassification.from_pretrained(
                    MODEL_DIR
                )
                cls.tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)

            cls.classifier = pipeline(
                "text-classification", model=cls.model, tokenizer=cls.tokenizer
            )

    @classmethod
    def predict_moderation(cls, text: str) -> dict:
        """Predict moderation score for the input text."""
        if cls.classifier is None:
            logger.error("Model not initialized. Please initialize the model first.")
            return {"error": "Model not initialized."}

        result = cls.classifier(text)
        prediction = result[0]

        score = round(prediction.get("score", 0), 4)
        category = SCORES_MAPPING.get(prediction["label"], "unknown")

        return {"text": text, "category": category, "confidence": score}
