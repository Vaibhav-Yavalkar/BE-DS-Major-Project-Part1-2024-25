import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi


genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

prompt = ''' as an expert in transcripting youtube videos , give a accurate summary of urls which is provided . the summary hsould be in 200 to 300 words . '''

#Getting the url and extracting transcript from videos
def extract_transcribe_text(youtube_video_url):
    try:    
        video_id = youtube_video_url.split("=")[1]
        transcrpit_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = '' # Append from list to paragraph
        for i in transcrpit_text:
            transcript += " " + i['text']
        return transcript
    
    except Exception as e:
        raise e



# Getting summary based on prompt using gemini pro
def generate_gemini_transcribe(transcrpit_text , prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt+transcrpit_text)
    return response.text

#Streamlit Part
st.title("YT Transcriber")
video_url = st.text_input("Enter Youtube Video Link")

if video_url:
    video_id = video_url.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcribe_text(video_url)

    if transcript_text:
        summary=generate_gemini_transcribe(transcript_text,prompt)
        st.markdown("Detailed Notes:")
        st.write(summary)
        
#https://www.youtube.com/watch?v=Qj7jPTQa2f4&t=2s