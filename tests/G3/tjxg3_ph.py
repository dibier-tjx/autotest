import pytest
import allure
import asyncio
from g3_config import *

@allure.feature("pH")
@pytest.mark.pH
class TJXG3PH:
    async def pv_close_to_sp(self, sp: float, timeout: float = 2):
        start_time = asyncio.get_running_loop().time()
        tolerance = get_ph_tolerance()
        while True:
            elapsed_time = asyncio.get_running_loop().time() - start_time
            if elapsed_time > timeout:
                return None, timeout
            pv = await get_ph_pv()
            if abs(sp - pv) < tolerance:
                return elapsed_time, timeout
            await asyncio.sleep(1)

    @pytest.mark.asyncio
    @pytest.mark.run(order=1)
    @allure.title('test_01')
    async def test_01(self):
        await set_ph_sp(10)
        await set_ph_sp_source('Fixed')
        await asyncio.sleep(2)
        pv1 = await get_ph_pv()
        if pv1 > 0:
            await set_ph_sp_source('Disable')
            await asyncio.sleep(2)
            pv2 = await get_ph_pv()
            if math.fabs(pv2) > 1e-10:
                allure.attach(body=f'curr pv is {pv2}, expect is zero', name='Error', attachment_type=allure.attachment_type.TEXT)
                assert False
        else:
            allure.attach(body=f'curr pv is {pv1}, expect is greater than zero', name='Error', attachment_type=allure.attachment_type.TEXT)
            assert False

    @pytest.mark.asyncio
    @pytest.mark.run(order=2)
    @allure.title('test_02')
    async def test_02(self):
        await set_ph_sp_source('Fixed')
        for it in get_ph_sps():
            pv1 = await get_ph_pv()
            await set_ph_sp(it)
            elapsed_time, timeout = await self.pv_close_to_sp(it)
            pv2 = await get_ph_pv()
            if elapsed_time is not None:
                allure.attach(body=f'{pv1}->{it} speed {elapsed_time} s, curr pv is {pv2}', name='Comment', attachment_type=allure.attachment_type.TEXT)
            else:
                allure.attach(body=f'{pv1}->{it} speed {timeout} s, curr pv is {pv2}', name='Error', attachment_type=allure.attachment_type.TEXT)
                await set_ph_sp_source('Disable')
                assert False
        await set_ph_sp_source('Disable')

    @pytest.mark.asyncio
    @pytest.mark.run(order=3)
    @allure.title('test_03')
    async def test_03(self):
        profile = await set_ph_profile()
        if profile is not None:
            assert await restart_runtime()
            await set_ph_sp_source('Profile')
            for it in profile:
                pv1 = await get_ph_pv()
                elapsed_time, timeout = await self.pv_close_to_sp(it[1], it[0])
                pv2 = await get_ph_pv()
                if elapsed_time is not None:
                    allure.attach(body=f'{pv1}->{it[1]} speed {elapsed_time} s, curr pv is {pv2}', name='Comment', attachment_type=allure.attachment_type.TEXT)
                else:
                    allure.attach(body=f'{pv1}->{it[1]} speed {timeout} s, curr pv is {pv2}', name='Error', attachment_type=allure.attachment_type.TEXT)
                    await set_ph_sp_source('Disable')
                    assert False
            await set_ph_sp_source('Disable')