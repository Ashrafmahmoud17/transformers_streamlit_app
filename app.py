import streamlit as st
from models import (
    summarize_text, analyze_sentiment, extract_entities, answer_question,
    generate_text, translate_text, fill_mask_text,
)

st.set_page_config(
    page_title="NLP Studio | Transformers",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1250px;}
    .hero {padding: 1.6rem 1.8rem; border-radius: 18px; background: linear-gradient(120deg,#111827,#243b53); color: white; margin-bottom: 1.25rem;}
    .hero h1 {margin: 0; font-size: 2.1rem;}
    .hero p {margin: .45rem 0 0 0; color: #dbeafe;}
    .metric-card {border: 1px solid rgba(128,128,128,.25); padding: 1rem 1.1rem; border-radius: 14px; min-height: 100px;}
    .result-card {border: 1px solid rgba(128,128,128,.25); border-radius: 14px; padding: 1rem 1.2rem; margin: .5rem 0;}
    div.stButton > button {border-radius: 10px; font-weight: 600; min-height: 2.8rem;}
</style>
""", unsafe_allow_html=True)

TASKS = {
    "Text Summarization": "📝",
    "Sentiment Analysis": "💬",
    "Named Entity Recognition": "🔎",
    "Question Answering": "❓",
    "Text Generation": "✨",
    "Translation": "🌍",
    "Fill Mask": "🧩",
}

with st.sidebar:
    st.markdown("## 🧠 NLP Studio")
    st.caption("Transformer models · Hugging Face")
    task = st.radio(
        "Choose a task",
        list(TASKS.keys()),
        format_func=lambda x: f"{TASKS[x]}  {x}",
    )
    st.divider()
    st.markdown("### About")
    st.caption("A demo application for eight NLP tasks using pretrained Transformer models.")
    st.caption("Models load only when you run a task. First run may take a few minutes.")

st.markdown(f"""
<div class="hero">
  <h1>{TASKS[task]} {task}</h1>
  <p>Explore NLP with pretrained Transformer models.</p>
</div>
""", unsafe_allow_html=True)

def run_button(label="Run model"):
    return st.button(f"🚀 {label}", type="primary", use_container_width=True)

def show_error(error):
    st.error(f"Could not complete this task: {error}")
    st.info("If this is the first run, wait for the model to download. If deployment fails, check the app logs and available memory.")

if task == "Text Summarization":
    st.markdown("Enter an English article and generate a shorter summary.")
    article = st.text_area("Article", height=230, placeholder="Paste an article here...")
    c1, c2 = st.columns(2)
    with c1:
        max_length = st.slider("Maximum summary length (tokens)", 30, 180, 80, 10)
    with c2:
        min_length = st.slider("Minimum summary length (tokens)", 5, 60, 15, 5)
    if run_button("Summarize"):
        if not article.strip():
            st.warning("Please enter an article first.")
        elif min_length >= max_length:
            st.warning("Minimum length must be smaller than maximum length.")
        else:
            with st.spinner("Loading model and summarizing..."):
                try:
                    result = summarize_text(article.strip(), max_length=max_length, min_length=min_length)
                    st.subheader("Summary")
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.write(result)
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.download_button("Download summary", result, file_name="summary.txt", mime="text/plain")
                except Exception as e:
                    show_error(e)

elif task == "Sentiment Analysis":
    st.markdown("Classify the sentiment of an English review or message.")
    text = st.text_area("Text to analyze", height=160, placeholder="This product is absolutely amazing!")
    if run_button("Analyze sentiment"):
        if not text.strip():
            st.warning("Please enter some text.")
        else:
            with st.spinner("Analyzing sentiment..."):
                try:
                    result = analyze_sentiment(text.strip())
                    label = result["label"]
                    score = float(result["score"])
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Predicted sentiment", "Positive" if label.upper() == "POSITIVE" else "Negative")
                    with col2:
                        st.metric("Model confidence", f"{score:.1%}")
                    st.progress(max(0.0, min(score, 1.0)))
                    st.caption("This model returns positive or negative labels; it does not provide a neutral class.")
                except Exception as e:
                    show_error(e)

elif task == "Named Entity Recognition":
    st.markdown("Find people, organizations, locations, and other named entities in English text.")
    text = st.text_area("Text", height=170, placeholder="Elon Musk founded SpaceX in California.")
    if run_button("Extract entities"):
        if not text.strip():
            st.warning("Please enter some text.")
        else:
            with st.spinner("Extracting entities..."):
                try:
                    entities = extract_entities(text.strip())
                    if not entities:
                        st.info("No entities were detected.")
                    else:
                        st.subheader(f"Found {len(entities)} entities")
                        for ent in entities:
                            left, right = st.columns([3, 1])
                            with left:
                                st.markdown(f"**{ent.get('word', '').strip()}**")
                                st.caption(f"Type: {ent.get('entity_group', 'Unknown')}")
                            with right:
                                st.metric("Confidence", f"{float(ent.get('score', 0)):.1%}")
                            st.divider()
                        st.download_button(
                            "Download entities as JSON",
                            data=__import__("json").dumps(entities, ensure_ascii=False, indent=2),
                            file_name="entities.json",
                            mime="application/json",
                        )
                except Exception as e:
                    show_error(e)

elif task == "Question Answering":
    st.markdown("Ask a question and the model will try to find the answer in the context you provide.")
    context = st.text_area("Context", height=220, placeholder="Paste the passage the answer should come from...")
    question = st.text_input("Question", placeholder="Who introduced the Transformer architecture?")
    if run_button("Find answer"):
        if not context.strip() or not question.strip():
            st.warning("Enter both a context and a question.")
        else:
            with st.spinner("Searching the context..."):
                try:
                    result = answer_question(question.strip(), context.strip())
                    answer = result.get("answer", "").strip()
                    if not answer:
                        st.info("The model could not find a confident answer in the supplied context.")
                    else:
                        st.subheader("Answer")
                        st.markdown(f'<div class="result-card">{answer}</div>', unsafe_allow_html=True)
                        st.metric("Confidence score", f"{float(result.get('score', 0)):.1%}")
                        st.caption("The score is a model estimate, not a guarantee that the answer is correct.")
                except Exception as e:
                    show_error(e)

elif task == "Text Generation":
    st.markdown("Generate a continuation from an English prompt using GPT-2.")
    prompt = st.text_area("Prompt", height=130, placeholder="Artificial intelligence will transform the world by...")
    c1, c2 = st.columns(2)
    with c1:
        max_new_tokens = st.slider("New tokens", 20, 120, 60, 10)
        temperature = st.slider("Temperature", 0.2, 1.5, 0.85, 0.05)
    with c2:
        variations = st.selectbox("Number of variations", [1, 2, 3], index=1)
        top_p = st.slider("Top-p", 0.5, 1.0, 0.92, 0.02)
    if run_button("Generate text"):
        if not prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating text..."):
                try:
                    outputs = generate_text(prompt.strip(), max_new_tokens=max_new_tokens,
                                            num_return_sequences=variations, temperature=temperature, top_p=top_p)
                    for i, output in enumerate(outputs, start=1):
                        st.markdown(f"**Variation {i}**")
                        st.markdown('<div class="result-card">', unsafe_allow_html=True)
                        st.write(output.get("generated_text", ""))
                        st.markdown("</div>", unsafe_allow_html=True)
                    st.download_button("Download generated text", "\n\n".join(x.get("generated_text", "") for x in outputs),
                                       file_name="generated_text.txt", mime="text/plain")
                except Exception as e:
                    show_error(e)

elif task == "Translation":
    st.markdown("Translate from English into one of the languages supported in your notebook.")
    language_options = {
        "French": "Helsinki-NLP/opus-mt-en-fr",
        "German": "Helsinki-NLP/opus-mt-en-de",
        "Spanish": "Helsinki-NLP/opus-mt-en-es",
        "Arabic": "Helsinki-NLP/opus-mt-en-ar",
    }
    language = st.selectbox("Target language", list(language_options.keys()))
    text = st.text_area("English text", height=160, placeholder="Artificial intelligence is changing the world.")
    if run_button("Translate"):
        if not text.strip():
            st.warning("Please enter text to translate.")
        else:
            with st.spinner(f"Translating into {language}..."):
                try:
                    result = translate_text(text.strip(), language_options[language])
                    st.subheader(f"Translation · {language}")
                    st.markdown('<div class="result-card">', unsafe_allow_html=True)
                    st.write(result)
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.download_button("Download translation", result, file_name="translation.txt", mime="text/plain")
                except Exception as e:
                    show_error(e)

elif task == "Fill Mask":
    st.markdown("Replace exactly one `[MASK]` token in an English sentence to see BERT's predictions.")
    sentence = st.text_input("Sentence with [MASK]", value="The capital of France is [MASK].")
    top_k = st.selectbox("Number of predictions", [3, 5], index=0)
    if run_button("Predict missing word"):
        if sentence.count("[MASK]") != 1:
            st.warning("Your sentence must contain exactly one [MASK] token.")
        else:
            with st.spinner("Predicting the missing word..."):
                try:
                    predictions = fill_mask_text(sentence, top_k=top_k)
                    st.subheader("Predictions")
                    for item in predictions:
                        token = item.get("token_str", "").strip()
                        score = float(item.get("score", 0))
                        st.write(f"**{token}** — {score:.1%}")
                        st.progress(max(0.0, min(score, 1.0)))
                except Exception as e:
                    show_error(e)

st.divider()
st.caption("Educational demo · Model outputs can be inaccurate. Review results before relying on them.")
