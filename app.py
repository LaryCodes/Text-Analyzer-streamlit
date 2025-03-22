import streamlit as st
from typing import Tuple

st.set_page_config(
    page_title="Advanced Text Analyzer",
    page_icon="📝",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main-header {
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def count_text_statistics(text: str) -> Tuple[int, int, int]:
    """
    Calculate basic text statistics.
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        Tuple[int, int, int]: Word count, character count, and vowel count
    """
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    vowel_count = sum(1 for char in text.lower() if char in 'aeiou')
    return word_count, char_count, vowel_count

def calculate_avg_word_length(text: str) -> float:
    words = text.split()
    if not words:
        return 0.0
    return sum(len(word) for word in words) / len(words)

def main():
    if 'text_input' not in st.session_state:
        st.session_state.text_input = ""
    if 'search_word' not in st.session_state:
        st.session_state.search_word = ""
    if 'replace_word' not in st.session_state:
        st.session_state.replace_word = ""
    if 'modified_text' not in st.session_state:
        st.session_state.modified_text = ""

    st.markdown("<h1 class='main-header'>✨ Advanced Text Analyzer ✨</h1>", unsafe_allow_html=True)
    
    st.markdown("### 📝 Enter Your Text")
    text_input = st.text_area(
        "",
        value=st.session_state.text_input,
        height=200,
        placeholder="Type or paste your text here...",
        help="Enter the text you want to analyze",
        key="text_area"
    )
    
    st.session_state.text_input = text_input

    analyze_clicked = st.button("🔍 Analyze Text", use_container_width=True)
    
    if analyze_clicked or st.session_state.text_input:
        if not st.session_state.text_input.strip():
            st.error("⚠️ Please enter some text to analyze!")
            return

        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
            st.subheader("📊 Basic Statistics")
            word_count, char_count, vowel_count = count_text_statistics(text_input)
            
            metrics = {
                "Words": word_count,
                "Characters": char_count,
                "Vowels": vowel_count,
                "Avg Word Length": f"{calculate_avg_word_length(text_input):.2f}"
            }
            
            for label, value in metrics.items():
                st.metric(label, value)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
            st.subheader("🔄 Text Transformations")
            
            with st.expander("UPPERCASE", expanded=True):
                st.code(text_input.upper())
            
            with st.expander("lowercase", expanded=True):
                st.code(text_input.lower())

            python_exists = "python" in text_input.lower()
            st.info("🐍 Python Reference Check", icon="ℹ️")
            if python_exists:
                st.success("Found 'Python' in the text!")
            else:
                st.warning("No 'Python' reference found.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col3:
            st.markdown("<div class='stat-card'>", unsafe_allow_html=True)
            st.subheader("🔎 Search and Replace")

            with st.form(key='search_replace_form'):
                search_word = st.text_input(
                    "Search for:",
                    value=st.session_state.search_word,
                    placeholder="Enter word to find..."
                )
                replace_word = st.text_input(
                    "Replace with:",
                    value=st.session_state.replace_word,
                    placeholder="Enter replacement word..."
                )
                submit_button = st.form_submit_button(label="Replace Text")
                
                if submit_button:
                    st.session_state.search_word = search_word
                    st.session_state.replace_word = replace_word
                    if search_word and replace_word:
                        st.session_state.modified_text = st.session_state.text_input.replace(search_word, replace_word)
                        st.success("Text modified successfully!")
                    else:
                        st.warning("Please enter both search and replace words.")

            if st.session_state.modified_text:
                with st.expander("View Modified Text", expanded=True):
                    st.code(st.session_state.modified_text)

                if st.button("📋 Copy Modified Text"):
                    st.session_state.text_input = st.session_state.modified_text
                    st.success("Modified text copied to input!")
                    st.rerun()
                    
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
