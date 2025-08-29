
from pydantic import BaseModel
from openai import OpenAI
client = OpenAI()

class Poster(BaseModel):
    title: str
    authors: str
    institutions: str

    summary: str
    contributions: str
    methodology: str
    results: str
    discussions: str


def suggest_visuals(summary_text: str) -> Poster:
    instruction = "You are a research poster designer. You will be provided with a markdown summarization of an academic paper to design a HTML poster. Extract the key points in the text provided, and convert them into HTML documents and fill into the structure."

    resp = client.responses.parse(
        input=summary_text,
        model="gpt-4.1",
        instructions=instruction,
        text_format=Poster,
    )

    if resp.output_parsed is not None:
        return resp.output_parsed
    else:
        raise Exception("visualizer model does not follow text_format")
