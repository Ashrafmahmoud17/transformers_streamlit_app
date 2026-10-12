import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

# Public hosting is commonly CPU-only. Use CUDA automatically when available.
DEVICE = 0 if torch.cuda.is_available() else -1

@__import__("streamlit").cache_resource(show_spinner=False, max_entries=1)
def get_pipeline(task_name, model_name, aggregation_strategy=None):
    kwargs = {"task": task_name, "model": model_name, "device": DEVICE}
    if aggregation_strategy is not None:
        kwargs["aggregation_strategy"] = aggregation_strategy
    return pipeline(**kwargs)

def summarize_text(text, max_length=80, min_length=15):
    model = get_pipeline("summarization", "sshleifer/distilbart-cnn-6-6")
    result = model(text, max_length=max_length, min_length=min_length, num_beams=4, truncation=True)
    return result[0]["summary_text"]

def analyze_sentiment(text):
    model = get_pipeline("sentiment-analysis", "distilbert-base-uncased-finetuned-sst-2-english")
    return model(text, truncation=True)[0]

def extract_entities(text):
    model = get_pipeline("ner", "dslim/bert-base-NER",
                         aggregation_strategy="simple")
    return model(text)

def answer_question(question, context):
    model = get_pipeline("question-answering", "deepset/roberta-base-squad2")
    result = model(question=question, context=context)
    # Do not expose a low-confidence span as a definite answer.
    if float(result.get("score", 0.0)) < 0.05:
        result["answer"] = ""
    return result

def generate_text(prompt, max_new_tokens=60, num_return_sequences=2, temperature=0.85, top_p=0.92):
    model = get_pipeline("text-generation", "gpt2")
    return model(
        prompt,
        max_new_tokens=max_new_tokens,
        num_return_sequences=num_return_sequences,
        temperature=temperature,
        top_p=top_p,
        top_k=50,
        do_sample=True,
        repetition_penalty=1.2,
        pad_token_id=50256,
    )

def translate_text(text, model_name):
    # Cache each translation model separately so a selected language is reused.
    model, tokenizer = get_translation_model(model_name)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(device)
    with torch.inference_mode():
        output_ids = model.generate(**inputs, max_new_tokens=200, num_beams=4)
    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

@__import__("streamlit").cache_resource(show_spinner=False, max_entries=1)
def get_translation_model(model_name):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    model.eval()
    return model, tokenizer

def classify_zero_shot(text, labels, multi_label=False):
    model = get_pipeline("zero-shot-classification", "facebook/bart-large-mnli")
    return model(text, candidate_labels=labels, multi_label=multi_label)

def fill_mask_text(text, top_k=3):
    model = get_pipeline("fill-mask", "bert-base-uncased")
    return model(text, top_k=top_k)
