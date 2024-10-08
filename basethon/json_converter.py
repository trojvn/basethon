import asyncio
from pathlib import Path
from typing import Generator

from jsoner import json_write_sync
from telethon import TelegramClient
from telethon.sessions import StringSession
from tooler import ProxyParser

from .base_session import BaseSession


class JsonConverter(BaseSession):
    def __init__(
        self,
        base_dir: Path,
        errors_dir: Path,
        banned_dir: Path,
        proxy: str,
        json_write: bool = True,
    ):
        super().__init__(base_dir, errors_dir, banned_dir)
        self.__api_id, self.__api_hash = 2040, "b18441a1ff607e10a989891a5462e627"
        self.__proxy = ProxyParser(proxy).asdict_thon
        self.__json_write = json_write

    def _main(self, item: Path, json_file: Path, json_data: dict) -> dict:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient(str(item), self.__api_id, self.__api_hash)
        ss = StringSession()
        ss._server_address = client.session.server_address  # type: ignore
        ss._takeout_id = client.session.takeout_id  # type: ignore
        ss._auth_key = client.session.auth_key  # type: ignore
        ss._dc_id = client.session.dc_id  # type: ignore
        ss._port = client.session.port  # type: ignore
        string_session = ss.save()
        del ss, client
        json_data["proxy"] = self.__proxy
        json_data["string_session"] = string_session
        if self.__json_write:
            json_write_sync(json_file, json_data)
        return json_data

    def iter(self) -> Generator:
        for item, json_file, json_data in self.iter_sessions():
            _json_data = self._main(item, json_file, json_data)
            yield item, json_file, _json_data

    def main(self) -> int:
        count = 0
        self.__json_write = True
        for item, json_file, json_data in self.iter_sessions():
            self._main(item, json_file, json_data)
            count += 1
        return count
