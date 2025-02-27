import os
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer, pipeline


class ModelSingleton:
    """ A singleton class that ensures only one instance of the model is loaded."""
    _model_instance = None

    @classmethod
    def get_model(cls):
        """Retrieves the tex moderation model"""
        if cls._model_instance is None:
            model_dir = os.path.abspath(
                "app/models/koala_ai_text_moderation")  # Hardcoded model path; could be made configurable via an env variable
            model = TFAutoModelForSequenceClassification.from_pretrained(
                model_dir)  # Using TensorFlow (no specific reason, I could also use PyTorch)
            tokenizer = AutoTokenizer.from_pretrained(model_dir)
            cls._model_instance = pipeline("text-classification", model=model, tokenizer=tokenizer)
        return cls._model_instance
