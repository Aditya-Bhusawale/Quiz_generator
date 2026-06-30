from typing import List

from pydantic import BaseModel, Field


class Question(BaseModel):
    question: str = Field(description="MCQ question")

    option_a: str
    option_b: str
    option_c: str
    option_d: str

    answer: str = Field(
        description="Correct option. Must be A, B, C or D"
    )


class Quiz(BaseModel):
    questions: List[Question]