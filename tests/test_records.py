import pytest
import httpx 
from fastapi import FastAPI
from starlette.status import HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY




class TestScrappingRoute:
    @pytest.mark.asyncio
    async def test_scrapping_exist(self) -> None:
        async with httpx.AsyncClient() as client:
            res = await client.post("http://localhost:5000/scrape", json={})
            assert res.status_code != HTTP_404_NOT_FOUND
    @pytest.mark.asyncio
    async def test_invalid_input_raises_error(self) -> None:
        # timeout = httpx.TimeoutConfig(connect_timeout=5, read_timeout=None, write_timeout=5 )
        async with httpx.AsyncClient() as client:
            res = await client.post("http://localhost:5000/scrape", json={"page_name":""},timeout=None)
            assert res.status_code != HTTP_422_UNPROCESSABLE_ENTITY