import streamlit as st
import time
import base64
from datetime import datetime, timedelta

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    md = f"""
    <audio autoplay="true">
    <source src="data:audio/wav;base64,{b64}" type="audio/wav">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)

def format_time(seconds):
    minutes, secs = divmod(seconds, 60)
    return f"{minutes:02d}:{secs:02d}"

def posture_reminder():
    st.title("Posture Reminder by Jason")

    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
        st.session_state.timer_complete = False
        st.session_state.start_time = None
        st.session_state.duration = 0

    position = st.radio("Choose your position:", ("Sit", "Stand"))
    default_time = 30 if position == "Sit" else 15
    duration = st.number_input(f"Enter the duration in minutes (default is {default_time} mins):", 
                               min_value=1, value=default_time, step=1)

    start_button = st.button("Start Timer")
    
    if start_button:
        st.session_state.timer_running = True
        st.session_state.timer_complete = False
        st.session_state.start_time = datetime.now()
        st.session_state.duration = duration * 60
        st.session_state.position = position

    if st.session_state.timer_running and not st.session_state.timer_complete:
        placeholder = st.empty()
        while True:
            now = datetime.now()
            elapsed = (now - st.session_state.start_time).total_seconds()
            remaining = max(st.session_state.duration - elapsed, 0)
            
            if remaining <= 0:
                break
            
            with placeholder.container():
                st.progress(1 - remaining / st.session_state.duration)
                st.markdown(f"""
                <div style="display: flex; justify-content: center; align-items: center; height: 150px; 
                            background-color: #f0f2f6; border-radius: 10px; margin: 20px 0;">
                    <span style="font-size: 80px; font-weight: bold; color: #0066cc;">
                        {format_time(int(remaining))}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            
            time.sleep(0.1)
        
        placeholder.empty()
        autoplay_audio("alert.wav")
        st.audio("alert.wav", format="audio/wav")
        st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 150px; 
                    background-color: #ff0000; border-radius: 10px; margin: 20px 0;">
            <span style="font-size: 60px; font-weight: bold; color: #ffffff;">
                TIME'S UP!
            </span>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.timer_complete = True
        st.session_state.timer_running = False

    if st.session_state.timer_complete:
        st.success(f"Finished! Please change your posture from {st.session_state.position.lower()}ing!")
        if st.button("Reset"):
            st.session_state.timer_running = False
            st.session_state.timer_complete = False
            st.session_state.start_time = None
            st.session_state.duration = 0
            st.rerun()

if __name__ == "__main__":
    posture_reminder()