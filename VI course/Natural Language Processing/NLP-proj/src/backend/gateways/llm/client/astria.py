from .base import BaseClient


class AtriaClient(BaseClient):
    """Адаптер API Atria-Dawn"""


    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str,
        timeout: float = 120.0
    ) -> None:

        super().__init__(
            base_url=base_url,
            api_key=api_key,
            model=model,
            timeout=timeout
        )
