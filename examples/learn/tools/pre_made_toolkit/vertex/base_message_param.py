from pathlib import Path

from mirascope.core import BaseDynamicConfig, BaseMessageParam, vertex
from mirascope.tools import FileSystemToolKit


@vertex.call("gemini-1.5-flash")
def write_blog_post(topic: str, output_file: Path) -> BaseDynamicConfig:
    toolkit = FileSystemToolKit(base_directory=output_file.parent)
    return {
        "messages": [
            BaseMessageParam(
                role="user",
                content=f"Write a blog post about '{topic}' as a '{output_file.name}'.",
            )
        ],
        "tools": toolkit.create_tools(),
    }


response = write_blog_post("machine learning", Path("introduction.html"))
if tool := response.tool:
    result = tool.call()
    print(result)
