from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from src.prompt import system_prompt
from src.schema import Quiz

load_dotenv()


class QuizGenerator:

    def __init__(self):
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0
        )
        self.llm = llm.with_structured_output(Quiz)

    def generate_quiz(self,retriever,topic,difficulty,num_questions):
        # Retrieve relevant documents
        docs = retriever.invoke(topic)

        # Convert documents to a single string
        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human","""
                            Context:{context}
                            Topic: {topic}
                            Difficulty: {difficulty}
                            Generate {num_questions} questions.
                        """
                )
            ]
        )

        chain = prompt | self.llm

        quiz = chain.invoke(
            {
                "context": context,
                "topic": topic,
                "difficulty": difficulty,
                "num_questions": num_questions
            }
        )

        return quiz