from transformers import TFAutoModelForSequenceClassification, AutoTokenizer


def download_model():
    model_name = "KoalaAI/Text-Moderation"

    # I'm assuming it's okay to store the models locally. Alternatively, I could upload them to cloud storage (e.g., S3 or GCS).
    # Another option would be to fetch the predictions from Hugging Face without downloading the models,
    # but 1) it was a requirement in the exercise, and 2) downloading the models ensures the model remains unchanged, maintaining consistency.
    cache_dir = "../models/koala_ai_text_moderation"
    model = TFAutoModelForSequenceClassification.from_pretrained(model_name, cache_dir=cache_dir)
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)

    model.save_pretrained(cache_dir)
    tokenizer.save_pretrained(cache_dir)

    print(f"Model and tokenizer downloaded and saved to {cache_dir}")

    return model, tokenizer


if __name__ == "__main__":
    download_model()
