from renamr.providers.provider import Provider


class OMDb(Provider):
    def movie(query: str) -> dict:
        ...

    def tv(query: str) -> dict:
        ...
