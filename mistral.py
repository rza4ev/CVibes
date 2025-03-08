import streamlit as st
from mistralai import Mistral

API_KEY = "ngG4tVdtsCNoLmSgXhNXq3VCjj5wlfIG"
MODEL = "mistral-small-latest"


client = Mistral(api_key=API_KEY)


st.title("🔍 CV and Job Description")


cv_text = st.text_area("📌CV Section ", height=200)


job_text = st.text_area("📌 Job Description Section:", height=200)

# The specific prompt that sending to the AI
matching_prompt = f"""
You are an AI assistant specialized in evaluating CVs against job descriptions.
Your task is to analyze the provided CV and job description and determine how well they match.

### CV:
{cv_text}

### Job Description:
{job_text}

Your response must include:
- **MatchScore**: A percentage (0-100) indicating how well the CV matches the job description.
- **Strengths**: A list of key strengths where the candidate meets or exceeds the job requirements.
- **Weaknesses**: A list of missing skills, experiences, or qualifications that the candidate lacks compared to the job description.
- **OverallEvaluation**: A brief summary of the candidate's fit for the role.

Ensure the output is structured and provides clear insights into the match between the CV and the job description.
"""

if st.button("🔎 Control the mathcing"):
    with st.spinner("AI is analyzing ..."):
        # 
        response = client.chat.complete(
            model=MODEL,
            messages=[{"role": "system", "content": matching_prompt}]
        )

       
        ai_response = response.choices[0].message.content

    
        st.success("✅ Results")
        st.text(ai_response)

        
        st.download_button("📥 Download the result ", data=ai_response, file_name="matching_result.txt", mime="text/plain")