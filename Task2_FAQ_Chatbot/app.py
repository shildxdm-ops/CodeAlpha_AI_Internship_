import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="FAQ Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 FAQ Chatbot")
st.write("Ask a question and I will find the most relevant answer.")

# FAQ dataset
faqs = [
    {
        "question": "What is Python?",
        "answer": "Python is a high-level, easy-to-learn programming language."
    },
    {
        "question": "How can I learn Python?",
        "answer": "You can learn Python through tutorials, documentation, practice problems, and projects."
    },
    {
        "question": "What is artificial intelligence?",
        "answer": "Artificial Intelligence is the field of creating systems that can perform tasks requiring human-like intelligence."
    },
    {
        "question": "What is machine learning?",
        "answer": "Machine Learning is a branch of AI where computers learn patterns from data."
    },
    {
        "question": "What is an internship?",
        "answer": "An internship provides practical experience and helps students understand real-world work."
    },
    {
        "question": "How can I reset my password?",
        "answer": "Go to the login page, click 'Forgot Password', and follow the instructions."
    },
    {
        "question": "How can I contact support?",
        "answer": "You can contact support through the official support email or contact page."
    },
    {
        "question": "What are the working hours?",
        "answer": "Working hours depend on the organization and internship schedule."
    }
]

questions = [item["question"] for item in faqs]
answers = [item["answer"] for item in faqs]

# Convert FAQ questions into numerical vectors
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

faq_vectors = vectorizer.fit_transform(questions)

# User input
user_question = st.text_input(
    "💬 Enter your question:",
    placeholder="Example: What is machine learning?"
)

if st.button("🔍 Find Answer", use_container_width=True):

    if not user_question.strip():
        st.warning("Please enter a question.")

    else:
        # Convert user question into a vector
        user_vector = vectorizer.transform([user_question])

        # Calculate similarity
        similarity_scores = cosine_similarity(
            user_vector,
            faq_vectors
        )[0]

        best_match_index = similarity_scores.argmax()
        best_score = similarity_scores[best_match_index]

        # Minimum similarity threshold
        if best_score < 0.15:
            st.warning(
                "Sorry, I could not find a relevant answer in the FAQ dataset."
            )
        else:
            st.success("Best matching answer found!")

            st.subheader("🤖 Chatbot Response")
            st.info(answers[best_match_index])

            st.caption(
                f"Similarity Score: {best_score:.2f}"
            )

# Show available FAQs
with st.expander("📚 View Available FAQs"):
    for i, question in enumerate(questions, start=1):
        st.write(f"{i}. {question}")