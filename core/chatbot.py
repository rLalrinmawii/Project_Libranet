import openai
from .utils import search_similar_books  # Custom function to query your database
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)



# Load environment variables from .env
load_dotenv()

class BookRecommendationChatbot:
    def __init__(self, user_input):
        self.user_input = user_input
        openai.api_key = os.getenv('OPENAI_API_KEY')  # Retrieve API key

    def get_recommendations(self):
        """
        Retrieve similar books from the database based on the user query.
        """
        recommended_books = search_similar_books(self.user_input)
        
        # Format the database results into a readable string
        if recommended_books:
            recommendations = "\n".join(
                [f"{book.title} by {book.author}" for book in recommended_books]
            )
        else:
            recommendations = None
        return recommendations

    def generate_response(self):
        """
        Generate a response using GPT based on database results.
        """
        # Get recommendations from the database
        recommendations = self.get_recommendations()

        # If no recommendations are found, provide a fallback response
        if not recommendations:
            return (
                f"Sorry, I couldn't find any books matching your query: '{self.user_input}'. "
                "Could you try a different search or refine your query?"
            )

        # Initialize the GPT model
        llm = ChatOpenAI(model="gpt-3.5-turbo")

        # Define a strict prompt template
        prompt_template = PromptTemplate(
            input_variables=["text", "books"],
            template=(
                "You are a helpful book recommendation chatbot. The user asked: {text}.\n\n"
                "Below are books found in the database that match their query:\n\n"
                "{books}\n\n"
                "Summarize these recommendations in a friendly and engaging way. If some of the books may not match the exact request, "
                "explain why they are included and provide a brief summary of the key themes."
            )
        )

        # Create a chain using the prompt template and OpenAI model
        book_chain = LLMChain(llm=llm, prompt=prompt_template)

        # Run the model to generate the response
        response = book_chain.run({"text": self.user_input, "books": recommendations})

        return response
