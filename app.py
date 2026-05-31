import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="Aura Translator",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
<style>
.stApp { background-color: #0b1120; color: white; }
.main-title { text-align: center; font-size: 50px; font-weight: bold; color: #00ffff; }
.subtitle { text-align: center; color: #bbbbbb; margin-bottom: 20px; }
div[data-testid="stSidebar"] { background-color: #0d1b2e; }
.stTextArea textarea { background-color: #1a2a4a !important; color: white !important; border: 1px solid #00ffff33 !important; }
.stSelectbox > div { background-color: #1a2a4a !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🌍 Aura Translator</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-Powered Translation in 50+ Languages</div>", unsafe_allow_html=True)

# ── LANGUAGES ──
LANGUAGES = [
    "English", "Hindi", "French", "German", "Spanish", "Italian",
    "Portuguese", "Russian", "Chinese", "Japanese", "Korean",
    "Arabic", "Turkish", "Dutch", "Polish", "Swedish", "Danish",
    "Norwegian", "Finnish", "Greek", "Hebrew", "Thai", "Vietnamese",
    "Indonesian", "Malay", "Bengali", "Urdu", "Punjabi", "Marathi",
    "Tamil", "Telugu", "Kannada", "Gujarati", "Malayalam",
    "Nepali", "Sinhala", "Burmese", "Khmer", "Lao",
    "Ukrainian", "Czech", "Slovak", "Hungarian", "Romanian",
    "Bulgarian", "Croatian", "Serbian", "Slovenian", "Estonian",
    "Latvian", "Lithuanian", "Swahili", "Afrikaans",
]

TONES = {
    "Normal": "Translate naturally.",
    "Formal": "Use formal, professional language.",
    "Casual": "Use casual, friendly language.",
    "Business": "Use business/corporate language.",
    "Simple": "Use very simple, easy-to-understand words.",
}

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("## ⚙ Settings")
    st.markdown("---")

    mode = st.selectbox("🧩 Mode", [
        "🔤 Text Translator",
        "📄 Document Translator",
        "💬 Conversation Mode",
        "📚 Batch Translator",
        "🔍 Word Explorer",
    ])

    st.markdown("**🎭 Translation Tone:**")
    tone = st.selectbox("Tone", list(TONES.keys()))

    st.markdown("**🤖 AI Model:**")
    model_choice = st.selectbox("Model", [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
    ])

    st.markdown("---")
    st.caption("Built by Rupal Darode 🚀")


# ── GROQ HELPER ──
def groq_translate(prompt):
    try:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    except Exception:
        return "❌ GROQ_API_KEY not found in Streamlit secrets."
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_choice,
            "messages": [
                {"role": "system", "content": "You are an expert translator. Always return only the translated text, nothing else. No explanations, no notes."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 2000,
        }
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers, json=payload, timeout=30
        )
        data = res.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"].strip()
        elif "error" in data:
            return f"❌ {data['error']['message']}"
        return "❌ Unexpected error."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def groq_ask(system, user_msg):
    try:
        GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    except Exception:
        return "❌ GROQ_API_KEY not found."
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_choice,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_msg}
            ],
            "temperature": 0.5,
            "max_tokens": 1000,
        }
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers, json=payload, timeout=30
        )
        data = res.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"].strip()
        return "❌ Error."
    except Exception as e:
        return f"❌ {str(e)}"


# ══════════════════════════════════════════
# MODE 1: TEXT TRANSLATOR
# ══════════════════════════════════════════
if "Text" in mode:
    col1, col2 = st.columns(2)
    with col1:
        source_lang = st.selectbox("🗣 From", ["Auto Detect"] + LANGUAGES)
    with col2:
        target_lang = st.selectbox("🎯 To", LANGUAGES, index=1)

    input_text = st.text_area("✍ Enter text to translate", height=180,
                               placeholder="Type or paste your text here...")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        translate_btn = st.button("🔁 Translate", use_container_width=True)
    with col_b:
        explain_btn = st.button("📖 Explain Translation", use_container_width=True)
    with col_c:
        alt_btn = st.button("🔀 Show Alternatives", use_container_width=True)

    if translate_btn and input_text.strip():
        with st.spinner("Translating..."):
            src = f"from {source_lang}" if source_lang != "Auto Detect" else "detecting the language automatically"
            prompt = f"Translate the following text {src} to {target_lang}. {TONES[tone]}\n\nText: {input_text}"
            result = groq_translate(prompt)
            st.session_state.last_translation = result
            st.session_state.last_input = input_text
            st.session_state.last_target = target_lang

        st.success("✅ Translation complete!")
        st.text_area("📋 Translated Text", result, height=180)
        st.download_button("⬇ Download", result,
                           file_name=f"translation_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                           mime="text/plain")

    if explain_btn and input_text.strip():
        with st.spinner("Analyzing..."):
            prompt = f"Translate '{input_text}' to {target_lang}, then explain key translation choices, grammar differences, and cultural notes."
            result = groq_ask("You are an expert linguist and translator.", prompt)
            st.info(result)

    if alt_btn and input_text.strip():
        with st.spinner("Finding alternatives..."):
            prompt = f"Give 3 different ways to translate this to {target_lang}, each with slightly different tone or style:\n\n{input_text}"
            result = groq_ask("You are an expert translator.", prompt)
            st.info(result)

    if not input_text.strip() and (translate_btn or explain_btn or alt_btn):
        st.warning("Please enter some text first!")


# ══════════════════════════════════════════
# MODE 2: DOCUMENT TRANSLATOR
# ══════════════════════════════════════════
elif "Document" in mode:
    st.subheader("📄 Document Translator")
    st.caption("Upload a .txt file and translate the entire document")

    target_lang = st.selectbox("🎯 Translate To", LANGUAGES, index=1)
    uploaded = st.file_uploader("Upload .txt file", type=["txt"])

    if uploaded:
        content = uploaded.read().decode("utf-8")
        st.text_area("📄 Original Content", content, height=150)

        if st.button("🔁 Translate Document", use_container_width=True):
            # Split into chunks if long
            chunks = [content[i:i+1500] for i in range(0, len(content), 1500)]
            translated_chunks = []

            progress = st.progress(0)
            for i, chunk in enumerate(chunks):
                with st.spinner(f"Translating part {i+1}/{len(chunks)}..."):
                    prompt = f"Translate to {target_lang}. {TONES[tone]}\n\n{chunk}"
                    translated_chunks.append(groq_translate(prompt))
                progress.progress((i + 1) / len(chunks))

            full_translation = "\n".join(translated_chunks)
            st.text_area("📋 Translated Document", full_translation, height=200)
            st.download_button("⬇ Download Translation", full_translation,
                               file_name=f"translated_{uploaded.name}",
                               mime="text/plain",
                               use_container_width=True)


# ══════════════════════════════════════════
# MODE 3: CONVERSATION MODE
# ══════════════════════════════════════════
elif "Conversation" in mode:
    st.subheader("💬 Conversation Translator")
    st.caption("Real-time bilingual conversation — perfect for talking to someone in another language")

    col1, col2 = st.columns(2)
    with col1:
        lang_a = st.selectbox("👤 Person A speaks", LANGUAGES, index=0)
    with col2:
        lang_b = st.selectbox("👥 Person B speaks", LANGUAGES, index=1)

    if "conv_history" not in st.session_state:
        st.session_state.conv_history = []

    person = st.radio("Who is speaking?", [f"👤 {lang_a}", f"👥 {lang_b}"], horizontal=True)
    msg = st.text_input("Type your message...")

    if st.button("Send & Translate", use_container_width=True):
        if msg.strip():
            speaking_lang = lang_a if lang_a in person else lang_b
            target = lang_b if lang_a in person else lang_a

            with st.spinner("Translating..."):
                translated = groq_translate(f"Translate from {speaking_lang} to {target}: {msg}")

            st.session_state.conv_history.append({
                "person": person,
                "original": msg,
                "translated": translated,
                "from_lang": speaking_lang,
                "to_lang": target,
            })

    # Show conversation
    for entry in st.session_state.conv_history:
        with st.chat_message("user" if lang_a in entry["person"] else "assistant"):
            st.markdown(f"**{entry['person']}:** {entry['original']}")
            st.caption(f"🔁 {entry['to_lang']}: {entry['translated']}")

    if st.button("🗑 Clear Conversation"):
        st.session_state.conv_history = []
        st.rerun()


# ══════════════════════════════════════════
# MODE 4: BATCH TRANSLATOR
# ══════════════════════════════════════════
elif "Batch" in mode:
    st.subheader("📚 Batch Translator")
    st.caption("Translate multiple sentences at once")

    target_lang = st.selectbox("🎯 Translate All To", LANGUAGES, index=1)
    batch_input = st.text_area("Enter multiple sentences (one per line)",
                                height=200,
                                placeholder="Hello, how are you?\nGood morning!\nThank you very much.")

    if st.button("🔁 Translate All", use_container_width=True):
        if batch_input.strip():
            lines = [l.strip() for l in batch_input.strip().split("\n") if l.strip()]
            results = []
            progress = st.progress(0)

            for i, line in enumerate(lines):
                with st.spinner(f"Translating {i+1}/{len(lines)}..."):
                    translated = groq_translate(f"Translate to {target_lang}: {line}")
                    results.append(f"Original: {line}\nTranslated: {translated}")
                progress.progress((i + 1) / len(lines))

            output = "\n\n".join(results)
            st.text_area("📋 All Translations", output, height=250)
            st.download_button("⬇ Download All", output,
                               file_name="batch_translations.txt",
                               mime="text/plain",
                               use_container_width=True)
        else:
            st.warning("Please enter some text!")


# ══════════════════════════════════════════
# MODE 5: WORD EXPLORER
# ══════════════════════════════════════════
elif "Word" in mode:
    st.subheader("🔍 Word Explorer")
    st.caption("Deep dive into any word — meanings, synonyms, usage examples")

    target_lang = st.selectbox("🎯 Explore in Language", LANGUAGES, index=1)
    word = st.text_input("Enter a word or phrase", placeholder="e.g. Serendipity, Jugaad, Schadenfreude...")

    col1, col2, col3 = st.columns(3)
    with col1:
        meaning_btn = st.button("📖 Meaning & Translation", use_container_width=True)
    with col2:
        synonym_btn = st.button("🔗 Synonyms", use_container_width=True)
    with col3:
        usage_btn = st.button("✍ Usage Examples", use_container_width=True)

    if word.strip():
        if meaning_btn:
            with st.spinner("Exploring..."):
                result = groq_ask(
                    "You are a linguistics expert.",
                    f"For the word/phrase '{word}': 1) Give its meaning 2) Translate to {target_lang} 3) Give etymology if interesting"
                )
                st.info(result)

        if synonym_btn:
            with st.spinner("Finding synonyms..."):
                result = groq_ask(
                    "You are a linguistics expert.",
                    f"Give 5 synonyms for '{word}' in its original language AND their {target_lang} equivalents."
                )
                st.info(result)

        if usage_btn:
            with st.spinner("Creating examples..."):
                result = groq_ask(
                    "You are a language teacher.",
                    f"Give 3 example sentences using '{word}', then translate each to {target_lang}."
                )
                st.info(result)


# ── FOOTER ──
st.markdown("---")
st.markdown(
    "<center style='color: #555; font-size: 12px;'>Built with ❤️ by Rupal Darode | Aura Translator 🌍 | Powered by Groq AI</center>",
    unsafe_allow_html=True
)
