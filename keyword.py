
import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# OpenAI API Key
load_dotenv()

# Function to get Groq completions
def get_groq_completions(user_content):
    client = Groq(
        api_key=os.getenv("GROQ_API_KEY"),
    )
    # prompt = f"Summarize the following text:\n{user_content}\nTranslate the summary into French language:"
    # prompt = f"Extract the most important keywords from the following text in French language:\n{user_content}\nKeywords:"
    prompt = f"""
                    Please identify and list the top 20 most important keywords and keyphrases from this text {user_content}.
                    Keywords and keyphrases should capture the core subjects, concepts, and entities discussed in the text. 
                    Focus on selecting terms that offer a concise overview of the text's content and its primary themes. 
                    Ensure that your selection precisely reflects the text's main points and overall significance.
                    Present your list by separating each keyword and keyphrase with a semicolon and Translate the summary into French language.
                    """
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful ai assistant"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5,
        max_tokens=5640,
        top_p=1,
        stream=True,
        stop=None,
    )

    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""

    return result

# Streamlit interface
def main():
    st.title("French Summary")
    user_content = st.text_input("Enter the text:")

    if st.button("Generate Summarry"):
        if not user_content:
                st.warning("Please enter a text before generating Summary.")
                return
        st.info("Generating Summary... Please wait.")
        generated_titles = get_groq_completions(user_content)
        st.success("Summary generated successfully!")

        # Display the generated titles
        st.markdown("### Generated Summay:")
        st.text_area("", value=generated_titles, height=200)

if __name__ == "__main__":
    main()

