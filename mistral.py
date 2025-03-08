import streamlit as st
from mistralai.client import MistralClient
import json

# 🔒 API açarı (TƏHLÜKƏSİZ SAXLA!)
API_KEY = "ngG4tVdtsCNoLmSgXhNXq3VCjj5wlfIG"
MODEL = "mistral-small-latest"

# Mistral müştərisini yaradın
client = MistralClient(api_key=API_KEY)

st.title("🔍 CV and Job Description Matching!")

cv_text = st.text_area("📌 CV Section:", height=200)
job_text = st.text_area("📌 Job Description Section:", height=200)

# ✅ AI Request Göndərmək üçün Funksiya
def process_request(cv, job):
    matching_prompt = f"""
    You are an AI assistant specialized in evaluating CVs against job descriptions.
    Your task is to analyze the provided CV and job description and determine how well they match.

    ### CV:
    {cv}

    ### Job Description:
    {job}

    Your response must include:
    - **MatchScore**: A percentage (0-100) indicating how well the CV matches the job description.
    - **Strengths**: A list of key strengths where the candidate meets or exceeds the job requirements.
    - **Weaknesses**: A list of missing skills, experiences, or qualifications that the candidate lacks compared to the job description.
    - **OverallEvaluation**: A brief summary of the candidate's fit for the role.

    Ensure the output is structured and provides clear insights into the match between the CV and the job description.
    """

    # 🔹 Yeni versiyada `ChatMessage` yoxdur, dict istifadə edirik
    messages = [
        {"role": "system", "content": "You are a job matching AI."},
        {"role": "user", "content": matching_prompt}
    ]

    response = client.chat(model=MODEL, messages=messages)
    return response.choices[0].message.content

# 🔹 API ilə GET request üçün URL dəstəyi əlavə edirik
params = st.experimental_get_query_params()
cv_param = params.get("cv", [""])[0]
job_param = params.get("job", [""])[0]

if cv_param and job_param:
    ai_response = process_request(cv_param, job_param)
    st.json({"response": ai_response})

# 🔘 UI düyməsi (Əl ilə işlətmək üçün)
if st.button("🔎 Check Matching"):
    with st.spinner("AI is analyzing ..."):
        ai_response = process_request(cv_text, job_text)
        st.success("✅ Results")
        st.text_area("🔹 AI Evaluation:", ai_response, height=300)
        st.download_button("📥 Download the result", data=ai_response, file_name="matching_result.txt", mime="text/plain")
