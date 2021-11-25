import torch
from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizerFast


def load_model_and_tokenizer():
    """
    Инициализация предобученной модели.
    """
    tokenizer = BertTokenizerFast.from_pretrained(
        'blanchefort/rubert-base-cased-sentiment')
    model = AutoModelForSequenceClassification.from_pretrained(
        'blanchefort/rubert-base-cased-sentiment', return_dict=True)
    return model, tokenizer


@torch.no_grad()
def predict(text, model, tokenizer):
    """
    Функция для предсказания типа данного на вход текста: нейтральный, позитивный, негативный.
    """
    inputs = tokenizer(
        text,
        max_length=512,
        padding=True,
        truncation=True,
        return_tensors='pt')
    outputs = model(**inputs)
    predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
    predicted_class = torch.argmax(predicted, dim=1).numpy()[0]
    return predicted_class