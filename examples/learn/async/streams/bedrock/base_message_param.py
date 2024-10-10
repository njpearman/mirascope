import asyncio

from mirascope.core import BaseMessageParam, bedrock


@bedrock.call(model="anthropic.claude-3-haiku-20240307-v1:0", stream=True)
async def recommend_book(genre: str) -> list[BaseMessageParam]:
    return [BaseMessageParam(role="user", content=f"Recommend a {genre} book")]


async def main():
    stream = await recommend_book("fantasy")
    async for chunk, _ in stream:
        print(chunk.content, end="", flush=True)


asyncio.run(main())
