from .provider import Provider

class TVMaze(Provider):
    def tv(query: str) -> dict:
        ...