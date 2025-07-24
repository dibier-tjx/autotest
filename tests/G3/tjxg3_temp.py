import math
import pytest
import allure
import asyncio
from api import G3API  

@allure.feature("Temp")
@pytest.mark.Temp
class TJXG3Temp:

    _g3api: G3API = G3API()    
    _lock: asyncio.Lock = asyncio.Lock()

    async def pv_close_to_sp(self, sp: float, timeout: float = 20.):
        start_time = asyncio.get_running_loop().time()
        tolerance = self._g3api.get_temp_tolerance()
        timeout = max(20., timeout)
        while True:
            elapsed_time = asyncio.get_running_loop().time() - start_time
            pv = await self._g3api.get_temp_pv()
            if elapsed_time > timeout:
                return None, timeout, pv
            if math.fabs(sp - pv) < tolerance:
                return elapsed_time, timeout, pv
            await asyncio.sleep(3)

    @pytest.mark.asyncio
    @pytest.mark.run(order=2)
    @allure.title('test_02')
    async def test_02(self):
        async with self._lock:
            assert await self._g3api.start_agit_to_temp()
            assert await self._g3api.set_temp_sp_source('Fixed')
            for it in self._g3api.get_temp_sps():
                pv1 = await self._g3api.get_temp_pv()
                assert await self._g3api.set_temp_sp(it)
                elapsed_time, timeout, pv2 = await self.pv_close_to_sp(it)
                if elapsed_time is not None:
                    allure.attach(body=f'{pv1}->{it} speed {elapsed_time} s, curr pv is {pv2}', name='Comment', attachment_type=allure.attachment_type.TEXT)
                else:
                    allure.attach(body=f'{pv1}->{it} speed {timeout} s, curr pv is {pv2}', name='Error', attachment_type=allure.attachment_type.TEXT)
                    assert False

    @pytest.mark.asyncio
    @pytest.mark.run(order=3)
    @allure.title('test_03')
    async def test_03(self):
        profile = await self._g3api.set_temp_profile()
        if profile is not None:
            async with self._lock:
                assert await self._g3api.restart_runtime()
                assert await self._g3api.start_agit_to_temp()
                assert await self._g3api.set_temp_sp_source('Profile')
                for it in profile:
                    pv1 = await self._g3api.get_temp_pv()
                    elapsed_time, timeout, pv2 = await self.pv_close_to_sp(it[1], (it[0] + 0.01) * 3600)
                    if elapsed_time is not None:
                        allure.attach(body=f'{pv1}->{it[1]} speed {elapsed_time} s, curr pv is {pv2}', name='Comment', attachment_type=allure.attachment_type.TEXT)
                    else:
                        allure.attach(body=f'{pv1}->{it[1]} speed {timeout} s, curr pv is {pv2}', name='Error', attachment_type=allure.attachment_type.TEXT)
                        await self._g3api.set_temp_sp_source('Fixed')
                        assert False
                await self._g3api.set_temp_sp_source('Fixed')