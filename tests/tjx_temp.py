import pytest
import asyncio
import pytest_asyncio

@pytest.mark.Temp
class TJXTemp:
    @pytest.mark.Temp02
    @pytest.mark.asyncio
    async def test_02(self):
        await asyncio.sleep(3)
        assert 1 + 1 == 2

    @pytest.mark.Temp03
    def test_03(self):
        assert 1 + 1 == 2

    @pytest.mark.Temp04
    @pytest.mark.asyncio
    async def test_04(self):
        await asyncio.sleep(5)
        assert 1 + 1 == 3