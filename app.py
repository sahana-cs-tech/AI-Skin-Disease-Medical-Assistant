import streamlit as st

from src.chatbot_backend import analyze_patient

st.set_page_config(
    page_title="Skin Disease Medical Chatbot",
    page_icon="🩺"
)

st.title("🩺 AI Skin Disease Medical Assistant")

uploaded_file, camera_image = st.columns(2)

with uploaded_file:
    uploaded_file = st.file_uploader(
        "📎 Attach Image",
        type=["jpg", "jpeg", "png"]
    )

with camera_image:
    camera_image = st.camera_input(
        "📷 Camera"
    )

question = st.text_area(
    "Describe your symptoms or ask a question"
)

if st.button(
    "🔍 Analyze",
    use_container_width=True
):
    image = uploaded_file if uploaded_file else camera_image

    with st.spinner("Analyzing..."):

        disease, confidence, answer, sources = analyze_patient(
            image,
            question
        )

    st.success("Analysis Complete")

    if disease is not None:
        st.subheader("Possible Condition")
        st.write(disease)

    if confidence is not None:
        st.subheader("Confidence")
        st.write(f"{confidence*100:.2f}%")

    st.subheader("Medical Explanation")
    st.write(answer)

    if sources:
        st.subheader("Sources")

        for source in sources:
            st.write("📄", source)
    st.divider()

    st.caption(
        "⚠️ Disclaimer: This AI assistant is intended for educational and informational purposes only. "
        "It does not provide medical advice, diagnosis, or treatment. Always consult a qualified healthcare "
        "professional for an accurate diagnosis and appropriate medical care."
    )