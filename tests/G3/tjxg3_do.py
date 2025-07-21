import math
import pytest
import allure
import asyncio
from api import G3API

@allure.feature("DO")
@pytest.mark.DO
class TJXG3DO:

    _g3api: G3API = G3API()    

    async def pv_close_to_sp(self, sp: float, timeout: float = 2):
        start_time = asyncio.get_running_loop().time()
        tolerance = self._g3api.get_do_tolerance()
        while True:
            elapsed_time = asyncio.get_running_loop().time() - start_time
            if elapsed_time > timeout:
                return None, timeout
            pv = await self._g3api.get_do_pv()
            if math.fabs(sp - pv) < tolerance:
                return elapsed_time, timeout
            await asyncio.sleep(1)

    @pytest.mark.asyncio
    @pytest.mark.run(order=1)
    @allure.title('test_01')
    async def test_01(self):
        await self._g3api.set_do_sp_source('Fixed')
        for it in self._g3api.get_do_sps():
            pv1 = await self._g3api.get_do_pv()
            await self._g3api.set_do_sp(it)
            elapsed_time, timeout = await self.pv_close_to_sp(it)
            pv2 = await self._g3api.get_do_pv()
            if elapsed_time is not None:
                allure.attach(body=f'{pv1}->{it} speed {elapsed_time} s, curr pv is {pv2}', name='Comment', attachment_type=allure.attachment_type.TEXT)
            else:
                allure.attach(body=f'{pv1}->{it} speed {timeout} s, curr pv is {pv2}', name='Error', attachment_type=allure.attachment_type.TEXT)
                assert False

    @pytest.mark.asyncio
    @pytest.mark.run(order=2)
    @allure.title('test_02')
    async def test_02(self):
        profile = await self._g3api.set_do_profile()
        if profile is not None:
            assert await self._g3api.restart_runtime()
            await self._g3api.set_do_sp_source('Profile')
            for it in profile:
                pv1 = await self._g3api.get_do_pv()
                elapsed_time, timeout = await self.pv_close_to_sp(it[1], it[0])
                pv2 = await self._g3api.get_do_pv()
                if elapsed_time is not None:
                    allure.attach(body=f'{pv1}->{it[1]} speed {elapsed_time} s, curr pv is {pv2}', name='Comment', attachment_type=allure.attachment_type.TEXT)
                else:
                    allure.attach(body=f'{pv1}->{it[1]} speed {timeout} s, curr pv is {pv2}', name='Error', attachment_type=allure.attachment_type.TEXT)
                    await self._g3api.set_do_sp_source('Fixed')
                    assert False
            await self._g3api.set_do_sp_source('Fixed')