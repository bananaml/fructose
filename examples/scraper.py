from fructose import Fructose
import requests
from dataclasses import dataclass

ai = Fructose()

def get(uri: str) -> str:
    """
    GET request to a URI
    """
    return requests.get(uri).text

@dataclass
class Comment:
    username: str
    comment: str

@ai(
    uses=[
        get
    ],
    debug=True
)
def get_comments(uri: str) -> list[Comment]:
    """
    Gets all base comments from a hacker news post
    """
    ...
    

result = get_comments("https://news.ycombinator.com/item?id=39619053")

for comment in result:
    print(f"🧑 {comment.username}: \n💬 {comment.comment}\n")

