from mirascope.core import Messages, bedrock


def get_book_author(title: str) -> str:
    """Returns the author of the book with the given title

    Example:
        {"title": "The Name of the Wind"}

    Args:
        title: The title of the book.
    """
    if title == "The Name of the Wind":
        return "Patrick Rothfuss"
    elif title == "Mistborn: The Final Empire":
        return "Brandon Sanderson"
    else:
        return "Unknown"


@bedrock.call("anthropic.claude-3-haiku-20240307-v1:0", tools=[get_book_author])
def identify_author(book: str) -> Messages.Type:
    return Messages.User(f"Who wrote {book}?")


response = identify_author("The Name of the Wind")
if tool := response.tool:
    print(tool.call())
else:
    print(response.content)
