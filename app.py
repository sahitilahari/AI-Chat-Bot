import streamlit as st
import google.generativeai as genai

# Configure Generative AI API
genai.configure(api_key="AIzaSyDyMkMloUmcxgb4BNJXf3_SI41fsIl14-0")

# Initialize Generative Model  
llm = genai.GenerativeModel("models/gemini-1.5-flash")
chatbot = llm.start_chat(history=[])

# Streamlit App
st.title("💬 An AI Code Reviewer")

# Input Section for Python Code
code_input = st.text_area(
    "Enter your Python code here:",
    height=300,
    placeholder="Paste your Python code..."
)

# Button to Submit Code for Review
if st.button("Generate"):
    if code_input.strip() == "":
        st.warning("Please enter some Python code to review.")
    else:
        st.info("Reviewing your code... Please wait.")
        
        # Construct the prompt for the Generative AI model
        review_prompt = (
            f"Review the following Python code for bugs, errors, and improvements. "
            f"Provide the results in two parts:\n"
            f"1. Bug Report: List any identified issues, errors, or inefficiencies in the code.\n"
            f"2. Fixed Code: Provide the corrected or improved version of the code.\n\n"
            f"{code_input}"
        )
        
        try:
            # Send the code review request
            response = chatbot.send_message(review_prompt)
            ai_feedback = response.text

            # Split the AI's response into Bug Report and Fixed Code
            bug_report, fixed_code = "", ""
            if "Bug Report:" in ai_feedback and "Fixed Code:" in ai_feedback:
                # Parse Bug Report and Fixed Code from the response
                split_feedback = ai_feedback.split("Bug Report:")[1].split("Fixed Code:")
                bug_report = split_feedback[0].strip()
                fixed_code = split_feedback[1].strip()
            else:
                # If the response is not formatted correctly
                bug_report = "Could not identify a specific bug report section in the response."
                fixed_code = ai_feedback  # Display the whole response as a fallback

            # Display Code Review Heading
            st.subheader("Code Review")
            
            # Display Bug Report without asterisks or formatting
            st.markdown(" Bug Report")
            if bug_report:
                st.text_area("Identified Issues", bug_report, height=200, disabled=True)  # Display as plain text

            # Display Fixed Code without asterisks or formatting
            st.markdown(" Fixed Code")
            if fixed_code:
                st.text_area("Corrected Code", fixed_code, height=300, disabled=True)  # Display as plain text

        except Exception as e:
            st.error(f"An error occurred while reviewing the code: {e}")

# Footer
#st.markdown("---")
#st.markdown("Developed with 💻 using Streamlit and Generative AI.")
