import pandas as pd
from transformers import AutoTokenizer, AutoModelForTokenClassification
def load_model(model_path):

    # Load the tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForTokenClassification.from_pretrained(model_path)
    return model, tokenizer
def tokenize_data(tokenizer, sentences):
    """
    Tokenizes the input sentences for evaluation.

    Args:
        tokenizer: The tokenizer to use.
        sentences (list of str): List of sentences to tokenize.

    Returns:
        dict: Tokenized inputs as tensors.
    """
    return tokenizer(
        sentences,
        truncation=True,
        padding=True,
        return_tensors="pt"
    )
import torch

def predict_labels(sentences, model, tokenizer):
    all_predictions = []
    for sentence in sentences:
        # Tokenize input
        tokens = tokenizer(sentence, return_tensors="pt", truncation=True, is_split_into_words=True)
        
        # Get model predictions
        with torch.no_grad():
            outputs = model(**tokens)
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=-1).squeeze().tolist()
        
        # Convert token IDs back to labels
        labels = [model.config.id2label[id] for id in predictions]
        all_predictions.append(labels)
    
    return all_predictions
def align_labels(predictions, true_labels, tokenizer, sentence):
    word_ids = tokenizer(sentence, return_tensors="pt", truncation=True, is_split_into_words=True).word_ids()
    aligned_preds, aligned_trues = [], []
    
    for word_id, pred, true in zip(word_ids, predictions, true_labels):
        if word_id is not None:  # Skip special tokens
            aligned_preds.append(pred)
            aligned_trues.append(true)
    
    return aligned_preds, aligned_trues
from sklearn.metrics import classification_report

def evaluate_model(sentences, true_labels, model, tokenizer):
    """
    Evaluate the model's predictions using F1-score, precision, and recall.
    """
    predictions = []
    for sentence in sentences:
        encoding = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**encoding)
        logits = outputs.logits
        predicted_labels = torch.argmax(logits, dim=-1).squeeze().tolist()

        tokens = tokenizer.convert_ids_to_tokens(encoding["input_ids"].squeeze())
        predictions.append(predicted_labels[:len(tokens)])  # Truncate to match token length

    # Flatten true and predicted labels
    true_labels_flat = [label for sublist in true_labels for label in sublist]
    predicted_labels_flat = [label for sublist in predictions for label in sublist]

    return classification_report(true_labels_flat, predicted_labels_flat, output_dict=True)
