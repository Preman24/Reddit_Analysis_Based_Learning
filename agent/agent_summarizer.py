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
            "Based on the user input, provide a corrected version of the text.",
            "Give a score based on the quality of the input.",
            "To approach the evaluation, follow these steps:",
            "1. Summarize the original work: Condense the key information, claims, and evidence from the text.",
            "2. Identify the rhetorical situation: Understand the original text's purpose, audience, and context.",
            "3. Analyze the evidence and arguments: Assess how the author uses evidence, logic, and rhetorical appeals to support their claims.",
            "4. Evaluate effectiveness: Determine whether the author's choices are effective in persuading the audience and achieving their purpose.",
            "5. Formulate your argument: Develop your own argument about the strengths and weaknesses of the original text.",
            "6. Support your argument: Back up your evaluation with specific examples and evidence from the text.",
            "Give a score based on the quality of the input where 50 is the full marks.",
            "Give feedback on how to improve the input with a sample of the corrected text.",
            "Check if the user input matches the data insights guidelines, if it doesn't, provide specific feedback on the discrepancies.",
            "Be more strict with the user input and its adherence to the guidelines.",
            "Output the evaluation in paragraph form.",
            "if the output does not meet any guidelines at all, give a 0 score."
        ]
    )
    
    try:
        combined_input = f"{user_input}\n\n{data_insights}" # Combine user input with data insights for evaluation
        summary = evaluation_agent.run(combined_input)  # Run the agent to get the evaluation
        return summary # Return the evaluation summary
    except Exception as e:
        st.error(f"An error occurred while generating the evaluation: {str(e)}") # Log the error message
        return None