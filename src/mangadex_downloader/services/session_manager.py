import aiohttp


class SessionManager:
    _session: aiohttp.ClientSession = None

    @staticmethod
    def create_session() -> aiohttp.ClientSession:
        """
        Creates a new aiohttp.ClientSession if one does not already exist
        """

        if SessionManager._session is None:
            SessionManager._session = aiohttp.ClientSession()

        return SessionManager._session

    @staticmethod
    async def close_session() -> None:
        """
        Closes the aiohttp.ClientSession if one exists
        """

        if SessionManager._session is not None:
            await SessionManager._session.close()
            SessionManager._session = None
