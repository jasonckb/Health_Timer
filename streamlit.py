import streamlit as st
import time

def posture_reminder():
    st.title("Posture Reminder App")

    # JavaScript for playing beep sound
    st.markdown("""
    <script>
    function beep() {
        var audio = new Audio('https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3');
        audio.play();
    }
    </script>
    """, unsafe_allow_html=True)

    # Add a button to test the sound
    if st.button("Test Sound"):
        st.markdown("<script>beep();</script>", unsafe_allow_html=True)
        st.write("If you didn't hear a sound, please check your audio settings and ensure autoplay is allowed for this site.")

    # Step 1: Ask user if they want to sit or stand
    position = st.radio("Choose your position:", ("Sit", "Stand"))

    # Step 2: Ask user to input the time
    default_time = 30 if position == "Sit" else 15
    duration = st.number_input(f"Enter the duration in minutes (default is {default_time} mins):", 
                               min_value=1, value=default_time, step=1)

    # Step 3: Start button
    if st.button("Start Timer"):
        # Step 4: Countdown timer
        progress_bar = st.progress(0)
        
        # Fancy timer display
        timer_placeholder = st.empty()
        
        for remaining in range(duration * 60, 0, -1):
            minutes, seconds = divmod(remaining, 60)
            
            # Update progress bar
            progress_bar.progress(1 - (remaining / (duration * 60)))
            
            # Update fancy timer display
            timer_placeholder.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; height: 150px; 
                        background-color: #f0f2f6; border-radius: 10px; margin: 20px 0;">
                <span style="font-size: 80px; font-weight: bold; color: #0066cc;">
                    {minutes:02d}:{seconds:02d}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(1)

        # Step 5: Finish notification with flashing visual alert and sound
        st.markdown("<script>beep();</script>", unsafe_allow_html=True)
        for _ in range(5):  # Flash 5 times
            timer_placeholder.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; height: 150px; 
                        background-color: #ff0000; border-radius: 10px; margin: 20px 0;">
                <span style="font-size: 80px; font-weight: bold; color: #ffffff;">
                    TIME'S UP!
                </span>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.5)
            timer_placeholder.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; height: 150px; 
                        background-color: #ffffff; border-radius: 10px; margin: 20px 0;">
                <span style="font-size: 80px; font-weight: bold; color: #ff0000;">
                    TIME'S UP!
                </span>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.5)

        st.success(f"Finished! Please change your posture from {position.lower()}ing!")

        # Reset button
        if st.button("Reset"):
            st.experimental_rerun()

if __name__ == "__main__":
    posture_reminder()