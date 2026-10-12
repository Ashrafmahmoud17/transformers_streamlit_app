# NLP Studio — Lightweight Transformers + Streamlit

A Streamlit web app for seven NLP tasks, using pretrained Hugging Face models downloaded automatically on the server when needed.

## Tasks and models
- Text Summarization — `sshleifer/distilbart-cnn-6-6` (smaller than the original 12-6 checkpoint)
- Sentiment Analysis — `distilbert-base-uncased-finetuned-sst-2-english`
- Named Entity Recognition — `dslim/bert-base-NER` (base-size replacement for BERT-large NER)
- Question Answering — `deepset/roberta-base-squad2`
- Text Generation — `gpt2`
- Translation — one selected Helsinki-NLP English-to-French, German, Spanish, or Arabic model
- Fill Mask — `bert-base-uncased`

The original `facebook/bart-large-mnli` Zero-Shot Classification task has been removed to reduce memory pressure.

## Deploy online
1. Upload `app.py`, `models.py`, `requirements.txt`, `.streamlit/config.toml`, and `README.md` to the root of a GitHub repository.
2. Open https://share.streamlit.io/ and create an app from that repository.
3. Set the main file path to `app.py` and deploy.
4. Models download to the server cache when a user runs a task. You do not need to upload model weights to GitHub.

## Resource notes
Streamlit Community Cloud's published approximate maximum is 2.7 GB RAM, but actual available resources and limits can vary. The app itself, Python, PyTorch, and model inference all consume memory beyond the raw model weight files.
- Model loading is lazy; only a selected task is loaded when run.
- The model cache is restricted to one general pipeline and one translation model at a time, to reduce the chance of keeping many large models resident.
- This is a lighter configuration, not a guarantee that every model will fit or run quickly on free hosting. Test each task after deployment and inspect Streamlit Cloud logs if a task fails.
- Translation models are loaded separately by language; avoid switching rapidly among languages on a memory-constrained instance.
- CPU inference may be slow. Models are downloaded automatically from Hugging Face on the server during first use.

Model outputs can be inaccurate. Do not use them as the sole basis for important decisions.
