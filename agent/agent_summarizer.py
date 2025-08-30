# import libraries
import streamlit as st
from agno.models.google import Gemini
from agno.agent import Agent
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini model with the API key from environment variables
gemini_model = Gemini(api_key=os.getenv("AI_API_KEY"))

# Function to evaluate user input using an AI agent
def AI_agent_evaluation(user_input, data_insights):
    # Check if user input is provided
    if not user_input.strip():
        st.error("No user input provided for evaluation.")
        return "No user input to evaluate."

    # Initialize the evaluation agent with specific instructions
    evaluation_agent = Agent(
        name="Data Analysis Evaluation Expert",
        role="Correct and evaluate the user input",
        model=gemini_model,
        instructions=[
             "You are a senior data analysis expert.",
            "Evaluate the user input based on the following criteria:",
            "1. **Summarize**: Condense the key information, claims, and evidence in the user input.",
            "2. **Identify Rhetorical Situation**: Clarify the purpose, audience, and context of the original text.",
            "3. **Analyze Evidence and Arguments**: Assess the use of evidence, logic, and rhetorical appeals.",
            "4. **Evaluate Effectiveness**: Determine the effectiveness of the author's choices in persuading the audience.",
            "5. **Formulate Your Argument**: Develop an argument highlighting strengths and weaknesses of the original text.",
            "6. **Support Your Argument**: Provide specific examples and evidence from the user input to back your evaluation.",
            "7. **Score**: Assign a score (0-50) based on the quality of the input; 50 is full marks.",
            "8. **Feedback**: Offer constructive feedback for improvement, including a corrected version of the text that incorporates all data insights.",
            "9. **Check Guidelines**: Ensure the user input adheres to the data insights. Provide specific feedback on any discrepancies.",
            "10. **Leniency for Line Graphs**: Be lenient when interpreting line graphs, focusing on overall trends rather than specifics.",
            "11. **Vagueness**: If the output lacks clarity or does not meet guidelines, assign a score of 0.",
            "Output the evaluation in a clear, cohesive paragraph.",
        ]
    )
    
    try:
        combined_input = f"{user_input}\n\n{data_insights}" # Combine user input with data insights for evaluation
        summary = evaluation_agent.run(combined_input)  # Run the agent to get the evaluation
        return summary # Return the evaluation summary
    except Exception as e:
        st.error(f"An error occurred while generating the evaluation: {str(e)}") # Log the error message
        return None