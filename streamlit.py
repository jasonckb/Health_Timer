import streamlit as st
import time

def posture_reminder():
    st.title("Posture Reminder App")

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
        status_text = st.empty()

        for remaining in range(duration * 60, 0, -1):
            minutes, seconds = divmod(remaining, 60)
            status_text.text(f"Time remaining: {minutes:02d}:{seconds:02d}")
            progress_bar.progress(1 - (remaining / (duration * 60)))
            time.sleep(1)

        # Step 5: Finish notification
        st.success(f"Finished! Please change your posture from {position.lower()}ing!")

        # Reset button
        if st.button("Reset"):
            st.experimental_rerun()

if __name__ == "__main__":
    posture_reminder()