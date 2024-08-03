import streamlit as st
import time
import base64

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

def run_timer():
    placeholder = st.empty()
    start_time = time.time()
    
    while True:
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(st.session_state.duration * 60 - elapsed_time, 0)
        
        if remaining_time == 0:
            break
        
        mins, secs = divmod(remaining_time, 60)
        time_str = f'{mins:02d}:{secs:02d}'
        
        with placeholder.container():
            st.progress(1 - remaining_time / (st.session_state.duration * 60))
            st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; height: 150px; 
                        background-color: #f0f2f6; border-radius: 10px; margin: 20px 0;">
                <span style="font-size: 60px; font-weight: bold; color: #0066cc;">
                    {time_str}
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        time.sleep(1)
    
    # Clear the timer display
    placeholder.empty()
    
    # Play sound once with autoplay
    autoplay_audio("alert.wav")
    
    # Also add Streamlit's audio component for manual playback if needed
    st.audio("alert.wav", format="audio/wav")
    
    # Display "TIME'S UP!" message
    st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; height: 150px; 
                background-color: #ff0000; border-radius: 10px; margin: 20px 0;">
        <span style="font-size: 80px; font-weight: bold; color: #ffffff;">
            TIME'S UP!
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.timer_complete = True

def posture_reminder():
    st.title("Posture Reminder App")

    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
        st.session_state.timer_complete = False

    position = st.radio("Choose your position:", ("Sit", "Stand"))
    default_time = 30 if position == "Sit" else 15
    duration = st.number_input(f"Enter the duration in minutes (default is {default_time} mins):", 
                               min_value=1, value=default_time, step=1)

    start_button = st.button("Start Timer")
    
    if start_button:
        st.session_state.timer_running = True
        st.session_state.duration = duration
        st.session_state.position = position
        st.session_state.timer_complete = False

    if st.session_state.timer_running and not st.session_state.timer_complete:
        run_timer()

    if st.session_state.timer_complete:
        st.success(f"Finished! Please change your posture from {st.session_state.position.lower()}ing!")
        if st.button("Reset"):
            st.session_state.timer_running = False
            st.session_state.timer_complete = False
            st.rerun()

if __name__ == "__main__":
    posture_reminder()