import streamlit as st
import ell
from pydantic import BaseModel, Field
import openai
import random

# Pydantic models remain the same
class CareerSuggestion(BaseModel):
    career: str = Field(description="Suggested career path")
    reasons: str = Field(description="Reasons for this suggestion")

class InterviewQuestions(BaseModel):
    role: str = Field(description="Role for the interview")
    questions: list[str] = Field(description="List of tailored questions")

# Initialize session state for API key
if 'openai_api_key' not in st.session_state:
    st.session_state.openai_api_key = None

# Function to check if API key is set
def is_api_key_set():
    return st.session_state.openai_api_key is not None

# Career Guidance Generator
def generate_career_guidance(interests: str, skills: str, goals: str):
    if not is_api_key_set():
        st.error("Please enter your OpenAI API key in the sidebar first!")
        return None
    
    client = openai.Client(api_key=st.session_state.openai_api_key)
    
    @ell.complex(model="gpt-4o", client=client, response_format=CareerSuggestion)
    def _generate(interests: str, skills: str, goals: str):
        return f"Based on interests: {interests}, skills: {skills}, and goals: {goals}, suggest a suitable career."
    
    try:
        return _generate(interests, skills, goals)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Interview Questions Generator
def generate_interview_questions(role: str):
    if not is_api_key_set():
        st.error("Please enter your OpenAI API key in the sidebar first!")
        return None
    
    client = openai.Client(api_key=st.session_state.openai_api_key)
    
    @ell.complex(model="gpt-4o", client=client, response_format=InterviewQuestions)
    def _generate(role: str):
        return f"Generate 5 interview questions for the role of {role}."
    
    try:
        return _generate(role)
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def get_random_inspiration():
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Choose a job you love, and you'll never work a day in your life. - Confucius",
        "Your work is going to fill a large part of your life, and the only way to be truly satisfied is to do what you believe is great work. - Steve Jobs",
        "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill"
    ]
    return random.choice(quotes)

def main():
    # Custom CSS remains the same
    st.markdown("""
        <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            border: none;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            background-color: #45a049;
            transform: translateY(-2px);
        }
        .quote-box {
            padding: 1rem;
            background-color: rgb(38 39 48);
            border-radius: 10px;
            margin: 1rem 0;
        }
        .feature-card {
            padding: 1.5rem;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🚀 AI Career Mentor")
    
    # Sidebar API Key Input
    st.sidebar.title("✨ Configuration")
    api_key = st.sidebar.text_input(
        "Enter your OpenAI API key",
        type="password",
        help="Get your API key from https://platform.openai.com/api-keys",
        value=st.session_state.openai_api_key if st.session_state.openai_api_key else ""
    )
    
    if api_key:
        st.session_state.openai_api_key = api_key
        st.sidebar.success("✅ API key set successfully!")
    else:
        st.sidebar.warning("⚠️ Please enter your OpenAI API key to use the app features")

    st.sidebar.markdown("---")
    st.sidebar.title("🔍 Navigation")
    
    # Inspirational quote
    st.markdown(f'<div class="quote-box">{get_random_inspiration()}</div>', unsafe_allow_html=True)

    feature = st.sidebar.radio("Select a Feature", [
        "Career Guidance",
        "Interview Question Generator",
        "About the App",
        "How It Works"
    ])

    if feature == "Career Guidance":
        # st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.header("🎯 Career Guidance Generator")
        
        col1, col2 = st.columns(2)
        with col1:
            interests = st.text_area("💭 Your Interests", placeholder="e.g., technology, teaching, problem-solving")
        with col2:
            skills = st.text_area("🛠️ Your Skills", placeholder="e.g., programming, communication, critical thinking")
        
        goals = st.text_area("🎯 Your Goals", placeholder="e.g., starting a company, working with AI, teaching students")
        
        if st.button("✨ Generate Career Advice"):
            if not is_api_key_set():
                st.error("Please enter your OpenAI API key in the sidebar first!")
            elif interests and skills and goals:
                with st.spinner('Analyzing your profile...'):
                    response = generate_career_guidance(interests, skills, goals)
                    if response:
                        st.success("Analysis Complete!")
                        st.subheader("🌟 Suggested Career Path")
                        st.info(response.parsed.career)
                        st.subheader("💡 Why This Path?")
                        st.write(response.parsed.reasons)
            else:
                st.error("Please fill in all fields to get personalized advice!")
        st.markdown('</div>', unsafe_allow_html=True)

    elif feature == "Interview Question Generator":
        # st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.header("🎯 Interview Question Creator")
        role = st.text_input("💼 Job Role", placeholder="e.g., Data Scientist, Product Manager")
        
        if st.button("🎲 Generate Questions"):
            if not is_api_key_set():
                st.error("Please enter your OpenAI API key in the sidebar first!")
            elif role:
                with st.spinner('Creating tailored questions...'):
                    response = generate_interview_questions(role)
                    if response:
                        st.success("Questions Generated!")
                        for idx, question in enumerate(response.parsed.questions, 1):
                            st.markdown(f"**Q{idx}.** {question}")
            else:
                st.error("Please enter a job role!")
        st.markdown('</div>', unsafe_allow_html=True)

    elif feature == "About the App":
        # st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.header("ℹ️ About AI Career Mentor")
        st.write(
            "Welcome to AI Career Mentor, your intelligent companion in career development! "
            "This app combines the power of advanced AI with intuitive design to help you "
            "make informed career decisions and prepare for your dream job."
        )
        st.markdown("""
        To get started:
        1. Enter your OpenAI API key in the sidebar
        2. Choose a feature you'd like to explore
        3. Follow the prompts to get personalized career guidance or interview questions
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    elif feature == "How It Works":
        # st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.header("⚙️ How It Works")
        st.write("Let's see how simple it is to use ell with this example:")
        
        st.code("""
import ell

@ell.simple(model="gpt-4o")
def write_a_poem(name: str):
    \"\"\"You are a helpful assistant that writes in lower case.\"\"\"
    return f"Write a poem for the developer named {name}"

write_a_poem("John")
        """, language="python")
        
        if st.button("🚀 Run Example"):
            if not is_api_key_set():
                st.error("Please enter your OpenAI API key in the sidebar first!")
            else:
                st.markdown("---")
                st.markdown("""
                *here's a poem for john, the coding star*
                
                in lines of code, john finds his way,
                debugging issues day by day,
                with coffee close and screen aglow,
                he makes the functions smoothly flow.
                
                a developer's life, he chose to lead,
                turning concepts into reality with speed,
                in john's world of ones and zeros bright,
                every bug fixed brings pure delight.
                """)
                st.success("Yay! See how easy it is to create magic with ell? 🎉")
        
        st.markdown("""
        The app uses several key components:
        1. 🎯 **Structured Output:** Uses Pydantic models for consistent responses
        2. 🤖 **AI Integration:** Leverages GPT-4 through the ell package
        3. 🎨 **Interactive UI:** Built with Streamlit for a seamless experience
        4. 🔄 **Real-time Processing:** Instant feedback and generation
        """)

        st.markdown("---")
        st.markdown("""
        🌟 **Want to dive deeper into ell?**  
        Explore the comprehensive [ell documentation](https://docs.ell.so/) to unlock its full potential and build amazing AI-powered applications!
        """)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()