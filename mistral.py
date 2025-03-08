import streamlit as st
from mistralai import Mistral

# API Anahtarınızı Buraya Ekleyin
API_KEY = "ngG4tVdtsCNoLmSgXhNXq3VCjj5wlfIG"
MODEL = "mistral-small-latest"

# Mistral AI istemcisini başlat
client = Mistral(api_key=API_KEY)

# Streamlit başlığı
st.title("🔍 CV & İş İlanı Eşleştirme")

# Kullanıcıdan CV metni alma
cv_text = st.text_area("📌 Lütfen adayın CV'sini girin:", height=200)

# Kullanıcıdan iş ilanı metni alma
job_text = st.text_area("📌 Lütfen iş ilanını girin:", height=200)

# AI'ya gönderilecek özel prompt
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

# Eğer hem CV hem iş ilanı girildiyse AI'ya gönder
if st.button("🔎 Eşleşmeyi Kontrol Et"):
    with st.spinner("AI analiz ediyor..."):
        # AI'ya CV ve iş ilanı metinlerini gönder
        response = client.chat.complete(
            model=MODEL,
            messages=[{"role": "system", "content": matching_prompt}]
        )

        # AI'dan gelen yanıtı al
        ai_response = response.choices[0].message.content

        # Sonucu ekrana yazdır
        st.success("✅ AI tarafından yapılan eşleşme analizi:")
        st.text(ai_response)

        # JSON'u indirme butonu
        st.download_button("📥 Sonucu İndir", data=ai_response, file_name="matching_result.txt", mime="text/plain")