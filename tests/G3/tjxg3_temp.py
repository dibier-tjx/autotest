import pytest
import allure
import asyncio
from g3_config import *

@allure.feature("温度")
@pytest.mark.Temp
class TJXG3Temp:
    async def pv_close_to_sp(self, sp: float, timeout: float = 2):
        start_time = asyncio.get_running_loop().time()
        tolerance = get_temp_tolerance()
        while True:
            elapsed_time = asyncio.get_running_loop().time() - start_time
            if elapsed_time > timeout:
                return None
            pv = await get_temp_pv()
            if abs(sp - pv) < tolerance:
                return elapsed_time
            await asyncio.sleep(1)

    @allure.story('具体文本信息')
    @pytest.mark.asyncio
    @pytest.mark.run(order=1)
    async def test_01(self):
        await start_agit_to_temp()
        await set_temp_sp_source('Fixed')
        for it in get_temp_sps():
            pv1 = await get_temp_pv()
            await set_temp_sp(it)
            elapsed_time = await self.pv_close_to_sp(it)
            if elapsed_time is not None:
                pv2 = await get_temp_pv()
                # 
            else:
                # timeout
                pass
        await set_temp_sp_source('Disable')

    @pytest.mark.asyncio
    @pytest.mark.run(order=2)
    async def test_02(self):
        await start_agit_to_temp()
        await set_temp_sp_source('Profile')
        profile = await set_temp_profile()
        assert await restart_runtime()
        for it in profile:
            await self.pv_close_to_sp(it[1], it[0])
        await set_temp_sp_source('Disable')