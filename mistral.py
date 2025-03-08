import streamlit as st
import threading
import time
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from mistralai import Mistral
import uvicorn

# Mistral AI üçün API açarı
API_KEY = "ngG4tVdtsCNoLmSgXhNXq3VCjj5wlfIG"
MODEL = "mistral-small-latest"

client = Mistral(api_key=API_KEY)

# FastAPI tətbiqi
app = FastAPI()

class CVRequest(BaseModel):
    cv_text: str
    job_text: str

@app.post("/match_cv")
async def match_cv(request: CVRequest):
    matching_prompt = f"""
    You are an AI assistant specialized in evaluating CVs against job descriptions.
    Your task is to analyze the provided CV and job description and determine how well they match.

    ### CV:
    {request.cv_text}

    ### Job Description:
    {request.job_text}

    Your response must include:
    - **MatchScore**: A percentage (0-100) indicating how well the CV matches the job description.
    - **Strengths**: A list of key strengths where the candidate meets or exceeds the job requirements.
    - **Weaknesses**: A list of missing skills, experiences, or qualifications that the candidate lacks compared to the job description.
    - **OverallEvaluation**: A brief summary of the candidate's fit for the role.

    Ensure the output is structured and provides clear insights into the match between the CV and the job description.
    """

    try:
        response = client.chat.complete(
            model=MODEL,
            messages=[{"role": "system", "content": matching_prompt}]
        )

        result = response.choices[0].message.content
        return {"match_result": result}

    except Exception as e:
        return {"error": str(e)}

# FastAPI serverini ayrıca bir thread-də işə salırıq
def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)

threading.Thread(target=run_fastapi, daemon=True).start()

time.sleep(2)  # FastAPI serverinin tam başladığından əmin olmaq üçün gözləmə


# 🌟 STREAMLIT UI 
st.title("🔍 CV and Job Description Matcher")

cv_text = st.text_area("📌 CV Section", height=200)
job_text = st.text_area("📌 Job Description Section", height=200)

if st.button("🔎 Control the matching"):
    with st.spinner("AI is analyzing ..."):
        API_URL = "http://127.0.0.1:8000/match_cv"  # Lokal API çağırışı
        response = requests.post(API_URL, json={"cv_text": cv_text, "job_text": job_text})

        if response.status_code == 200:
            result = response.json()["match_result"]
            st.success("✅ Results")
            st.text(result)

            st.download_button("📥 Download the result", data=result, file_name="matching_result.txt", mime="text/plain")
        else:
            st.error("🚨 Error: Could not process the request!")
