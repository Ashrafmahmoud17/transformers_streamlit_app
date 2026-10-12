
import html
import json
import streamlit as st

from models import (
    summarize_text,
    analyze_sentiment,
    extract_entities,
    answer_question,
    generate_text,
    translate_text,
    fill_mask_text,
)

st.set_page_config(
    page_title="NLP Studio | Transformers",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================
# Custom CSS
# =========================

st.markdown("""
<style>
    :root {
        --page-bg: #f7f8fa;
        --surface: #ffffff;
        --text-main: #202938;
        --text-muted: #667085;
        --border: #e1e5eb;
        --accent: #344054;
    }

    /* Main page */
    .stApp {
        background: var(--page-bg);
        color: var(--text-main);
    }

    .block-container {
        max-width: 1120px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* General text */
    .stApp p,
    .stApp label,
    .stApp [data-testid="stMarkdownContainer"],
    .stApp [data-testid="stCaptionContainer"],
    .stApp [data-testid="stWidgetLabel"],
    .stApp h1,
    .stApp h2,
    .stApp h3 {
        color: var(--text-main);
    }

    .stApp [data-testid="stCaptionContainer"] {
        color: var(--text-muted) !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] h2 {
        color: var(--text-main) !important;
        font-size: 1.35rem;
        font-weight: 650;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span {
        color: #252b36 !important;
    }

    /* Hero section */
    .hero {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1.5rem 1.6rem;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        color: var(--text-main) !important;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.035em;
        line-height: 1.2;
        margin: 0 0 0.55rem 0;
    }

    .hero p {
        color: var(--text-muted) !important;
        font-size: 1rem;
        line-height: 1.6;
        margin: 0;
    }

    /* Inputs */
    .stApp input,
    .stApp textarea {
        color: #202938 !important;
        -webkit-text-fill-color: #202938 !important;
        background-color: #ffffff !important;
        border-color: #d0d5dd !important;
    }

    .stApp input::placeholder,
    .stApp textarea::placeholder {
        color: #667085 !important;
        -webkit-text-fill-color: #667085 !important;
        opacity: 1 !important;
    }

    .stApp [data-baseweb="select"] {
        background-color: #ffffff !important;
    }

    .stApp [data-baseweb="select"] * {
        color: #202938 !important;
        -webkit-text-fill-color: #202938 !important;
    }

    /* Buttons */
    .stApp div.stButton > button,
    .stApp div.stFormSubmitButton > button {
        background-color: #344054 !important;
        color: #ffffff !important;
        border: 1px solid #344054 !important;
        border-radius: 6px;
        min-height: 2.65rem;
        font-weight: 600;
        box-shadow: none;
        transition: background-color 0.15s ease;
    }

    .stApp div.stButton > button *,
    .stApp div.stFormSubmitButton > button * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    .stApp div.stButton > button:hover,
    .stApp div.stFormSubmitButton > button:hover {
        background-color: #263246 !important;
        border-color: #263246 !important;
    }

    /* Download buttons */
    .stApp div.stDownloadButton > button {
        background-color: #ffffff !important;
        color: #344054 !important;
        border: 1px solid #d0d5dd !important;
        border-radius: 6px;
        min-height: 2.65rem;
        font-weight: 550;
    }

    .stApp div.stDownloadButton > button * {
        color: #344054 !important;
        -webkit-text-fill-color: #344054 !important;
    }

    /* Metrics */
    .stApp [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1rem;
    }

    .stApp [data-testid="stMetricLabel"],
    .stApp [data-testid="stMetricValue"] {
        color: #202938 !important;
    }

    .stApp [data-testid="stMetricDelta"] {
        opacity: 1 !important;
    }

    /* Result cards */
    .result-card {
        background: #ffffff !important;
        border: 1px solid #dce2ea;
        border-radius: 8px;
        padding: 1.1rem 1.2rem;
        margin: 0.5rem 0 1.1rem 0;
        color: #202938 !important;
        font-size: 1rem;
        line-height: 1.8;
        overflow-wrap: anywhere;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
    }

    .result-card * {
        color: #202938 !important;
    }

    /* FIX: Variation titles */
    .stApp .variation-title {
        display: block !important;
        width: 100% !important;
        box-sizing: border-box !important;
        background: #eaf2ff !important;
        color: #174ea6 !important;
        -webkit-text-fill-color: #174ea6 !important;
        border: 1px solid #b6d0ff !important;
        border-left: 5px solid #2563eb !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        margin: 22px 0 10px 0 !important;
        font-size: 1.15rem !important;
        font-weight: 750 !important;
        line-height: 1.5 !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    .stApp [data-testid="stMarkdownContainer"] .variation-title,
    .stApp [data-testid="stMarkdownContainer"] p.variation-title {
        background: #eaf2ff !important;
        color: #174ea6 !important;
        -webkit-text-fill-color: #174ea6 !important;
    }

    /* Divider and progress */
    .stApp hr {
        border-color: var(--border);
    }

    .stApp [data-testid="stProgress"] > div {
        border-radius: 4px;
    }

    /* Responsive layout */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 2rem;
        }

        .hero {
            padding: 1.15rem;
        }

        .hero h1 {
            font-size: 1.65rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# =========================
# Sidebar
# =========================

TASKS = [
    "Text Summarization",
    "Sentiment Analysis",
    "Named Entity Recognition",
    "Question Answering",
    "Text Generation",
    "Translation",
    "Fill Mask",
]

with st.sidebar:
    st.markdown("## NLP Studio")
    st.caption("Natural language processing tools")

    task = st.radio(
        "Choose a task",
        TASKS,
    )

    st.divider()

    st.markdown("### About")
    st.caption(
        "A demonstration of seven natural language processing tasks "
        "using pretrained models."
    )
    st.caption(
        "Models load only when you run a task. "
        "First run may take a few minutes."
    )


# =========================
# Page header
# =========================

st.markdown(
    f"""
    <div class="hero">
        <h1>{html.escape(task)}</h1>
        <p>Explore NLP with pretrained Transformer models.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================
# Helper functions
# =========================

def run_button(label="Run model"):
    return st.button(
        label,
        type="primary",
        use_container_width=True,
    )


def show_error(error):
    st.error(f"Could not complete this task: {error}")
    st.info(
        "If this is the first run, wait for the model to download. "
        "If deployment fails, check the app logs and available memory."
    )


def show_result(result):
    """Display model output safely inside a result card."""
    safe_result = html.escape(str(result)).replace("\n", "<br>")

    st.markdown(
        f'<div class="result-card">{safe_result}</div>',
        unsafe_allow_html=True,
    )


def show_variation_title(number):
    """Display a clearly visible title for each generated variation."""
    st.markdown(
        f'<p class="variation-title">Variation {number}</p>',
        unsafe_allow_html=True,
    )


# =========================
# Text Summarization
# =========================

if task == "Text Summarization":

    st.markdown(
        "Enter an English article and generate a shorter summary."
    )

    article = st.text_area(
        "Article",
        height=230,
        placeholder="Paste an article here...",
    )

    c1, c2 = st.columns(2)

    with c1:
        max_length = st.slider(
            "Maximum summary length (tokens)",
            30, 180, 80, 10,
        )

    with c2:
        min_length = st.slider(
            "Minimum summary length (tokens)",
            5, 60, 15, 5,
        )

    if run_button("Summarize"):

        if not article.strip():
            st.warning("Please enter an article first.")

        elif min_length >= max_length:
            st.warning(
                "Minimum length must be smaller than maximum length."
            )

        else:
            with st.spinner("Loading model and summarizing..."):
                try:
                    result = summarize_text(
                        article.strip(),
                        max_length=max_length,
                        min_length=min_length,
                    )

                    st.subheader("Summary")
                    show_result(result)

                    st.download_button(
                        "Download summary",
                        str(result),
                        file_name="summary.txt",
                        mime="text/plain",
                    )

                except Exception as e:
                    show_error(e)


# =========================
# Sentiment Analysis
# =========================

elif task == "Sentiment Analysis":

    st.markdown(
        "Classify the sentiment of an English review or message."
    )

    text = st.text_area(
        "Text to analyze",
        height=160,
        placeholder="This product is absolutely amazing!",
    )

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
                        sentiment = (
                            "Positive"
                            if label.upper() == "POSITIVE"
                            else "Negative"
                        )

                        st.metric(
                            "Predicted sentiment",
                            sentiment,
                        )

                    with col2:
                        st.metric(
                            "Model confidence",
                            f"{score:.1%}",
                        )

                    st.progress(max(0.0, min(score, 1.0)))

                    st.caption(
                        "This model returns positive or negative labels; "
                        "it does not provide a neutral class."
                    )

                except Exception as e:
                    show_error(e)


# =========================
# Named Entity Recognition
# =========================

elif task == "Named Entity Recognition":

    st.markdown(
        "Find people, organizations, locations, and other named "
        "entities in English text."
    )

    text = st.text_area(
        "Text",
        height=170,
        placeholder="Elon Musk founded SpaceX in California.",
    )

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
                        st.subheader(
                            f"Found {len(entities)} entities"
                        )

                        for ent in entities:
                            left, right = st.columns([3, 1])

                            with left:
                                st.markdown(
                                    f"**{html.escape(str(ent.get('word', '')).strip())}**"
                                )

                                st.caption(
                                    f"Type: {ent.get('entity_group', 'Unknown')}"
                                )

                            with right:
                                st.metric(
                                    "Confidence",
                                    f"{float(ent.get('score', 0)):.1%}",
                                )

                            st.divider()

                        st.download_button(
                            "Download entities as JSON",
                            data=json.dumps(
                                entities,
                                ensure_ascii=False,
                                indent=2,
                            ),
                            file_name="entities.json",
                            mime="application/json",
                        )

                except Exception as e:
                    show_error(e)


# =========================
# Question Answering
# =========================

elif task == "Question Answering":

    st.markdown(
        "Ask a question and the model will try to find the answer "
        "in the context you provide."
    )

    context = st.text_area(
        "Context",
        height=220,
        placeholder="Paste the passage the answer should come from...",
    )

    question = st.text_input(
        "Question",
        placeholder="Who introduced the Transformer architecture?",
    )

    if run_button("Find answer"):

        if not context.strip() or not question.strip():
            st.warning("Enter both a context and a question.")

        else:
            with st.spinner("Searching the context..."):
                try:
                    result = answer_question(
                        question.strip(),
                        context.strip(),
                    )

                    answer = result.get("answer", "").strip()

                    if not answer:
                        st.info(
                            "The model could not find a confident answer "
                            "in the supplied context."
                        )

                    else:
                        st.subheader("Answer")
                        show_result(answer)

                        st.metric(
                            "Confidence score",
                            f"{float(result.get('score', 0)):.1%}",
                        )

                        st.caption(
                            "The score is a model estimate, not a guarantee "
                            "that the answer is correct."
                        )

                except Exception as e:
                    show_error(e)


# =========================
# Text Generation
# =========================

elif task == "Text Generation":

    st.markdown(
        "Generate a continuation from an English prompt using GPT-2."
    )

    prompt = st.text_area(
        "Prompt",
        height=130,
        placeholder="Artificial intelligence will transform the world by...",
    )

    c1, c2 = st.columns(2)

    with c1:
        max_new_tokens = st.slider(
            "New tokens",
            20, 120, 60, 10,
        )

        temperature = st.slider(
            "Temperature",
            0.2, 1.5, 0.85, 0.05,
        )

    with c2:
        variations = st.selectbox(
            "Number of variations",
            [1, 2, 3],
            index=1,
        )

        top_p = st.slider(
            "Top-p",
            0.5, 1.0, 0.92, 0.02,
        )

    if run_button("Generate text"):

        if not prompt.strip():
            st.warning("Please enter a prompt.")

        else:
            with st.spinner("Generating text..."):
                try:
                    outputs = generate_text(
                        prompt.strip(),
                        max_new_tokens=max_new_tokens,
                        num_return_sequences=variations,
                        temperature=temperature,
                        top_p=top_p,
                    )

                    for i, output in enumerate(outputs, start=1):

                        # Explicit CSS class fixes the Variation title color.
                        show_variation_title(i)

                        generated_text = output.get(
                            "generated_text", ""
                        )

                        show_result(generated_text)

                    st.download_button(
                        "Download generated text",
                        "\n\n".join(
                            x.get("generated_text", "")
                            for x in outputs
                        ),
                        file_name="generated_text.txt",
                        mime="text/plain",
                    )

                except Exception as e:
                    show_error(e)


# =========================
# Translation
# =========================

elif task == "Translation":

    st.markdown(
        "Translate from English into one of the languages "
        "supported in your notebook."
    )

    language_options = {
        "French": "Helsinki-NLP/opus-mt-en-fr",
        "German": "Helsinki-NLP/opus-mt-en-de",
        "Spanish": "Helsinki-NLP/opus-mt-en-es",
        "Arabic": "Helsinki-NLP/opus-mt-en-ar",
    }

    language = st.selectbox(
        "Target language",
        list(language_options.keys()),
    )

    text = st.text_area(
        "English text",
        height=160,
        placeholder="Artificial intelligence is changing the world.",
    )

    if run_button("Translate"):

        if not text.strip():
            st.warning("Please enter text to translate.")

        else:
            with st.spinner(f"Translating into {language}..."):
                try:
                    result = translate_text(
                        text.strip(),
                        language_options[language],
                    )

                    st.subheader(f"Translation: {language}")
                    show_result(result)

                    st.download_button(
                        "Download translation",
                        str(result),
                        file_name="translation.txt",
                        mime="text/plain",
                    )

                except Exception as e:
                    show_error(e)


# =========================
# Fill Mask
# =========================

elif task == "Fill Mask":

    st.markdown(
        "Replace exactly one [MASK] token in an English sentence "
        "to see BERT's predictions."
    )

    sentence = st.text_input(
        "Sentence with [MASK]",
        value="The capital of France is [MASK].",
    )

    top_k = st.selectbox(
        "Number of predictions",
        [3, 5],
        index=0,
    )

    if run_button("Predict missing word"):

        if sentence.count("[MASK]") != 1:
            st.warning(
                "Your sentence must contain exactly one [MASK] token."
            )

        else:
            with st.spinner("Predicting the missing word..."):
                try:
                    predictions = fill_mask_text(
                        sentence,
                        top_k=top_k,
                    )

                    st.subheader("Predictions")

                    for item in predictions:
                        token = item.get("token_str", "").strip()
                        score = float(item.get("score", 0))

                        st.write(
                            f"**{html.escape(token)}** — {score:.1%}"
                        )

                        st.progress(
                            max(0.0, min(score, 1.0))
                        )

                except Exception as e:
                    show_error(e)


# =========================
# Footer
# =========================

st.divider()

st.caption(
    "Educational demonstration. Model outputs may be inaccurate; "
    "review results before relying on them."
)
