from mirascope.core import vertex


@vertex.call("gemini-1.5-flash")
def recommend_book(genre: str) -> str:
    return f"Recommend a {genre} book"


print(recommend_book("fantasy"))