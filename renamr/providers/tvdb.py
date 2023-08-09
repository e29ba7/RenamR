from .provider import Provider


class TVDb(Provider):
    def movie(query: str) -> dict:
        ...

    def tv(query: str) -> dict:
        ...
