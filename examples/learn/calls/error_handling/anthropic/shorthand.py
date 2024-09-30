from anthropic import AnthropicError
from mirascope.core import anthropic


@anthropic.call("claude-3-5-sonnet-20240620")
def recommend_book(genre: str) -> str:
    return f"Recommend a {genre} book"


try:
    response = recommend_book("fantasy")
    print(response.content)
except AnthropicError as e:
    print(f"Error: {str(e)}")