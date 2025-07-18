import pytest
import allure
import asyncio
from g3_config import *

@allure.feature("MFC")
@pytest.mark.MFC
class TJXG3MFC:
    async def pv_close_to_sp(self, i: int, sp: float, timeout: float = 2):
        start_time = asyncio.get_running_loop().time()
        tolerance = get_mfc_tolerance(i)
        while True:
            elapsed_time = asyncio.get_running_loop().time() - start_time
            if elapsed_time > timeout:
                return None, timeout
            pv = await get_mfc_pv(i)
            if abs(sp - pv) < tolerance:
                return elapsed_time, timeout
            await asyncio.sleep(1)

    @pytest.mark.asyncio
    @pytest.mark.run(order=1)
    @allure.title('test_01')
    async def test_01(self):
        for i, mfc in enumerate(get_mfcs()):
            await set_mfc_sp(i, 3)
            await set_mfc_sp_source(i, 'Fixed')
            await asyncio.sleep(2)
            pv1 = await get_mfc_pv(i)
            if pv1 > 0:
                await set_mfc_sp_source(i, 'Disable')
                await asyncio.sleep(2)
                pv2 = await get_mfc_pv(i)
                if math.fabs(pv2) > 1e-10:
                    allure.attach(body=f'MFC{i+1}[{mfc}] curr pv is {pv2}, expect is zero', name='Error', attachment_type=allure.attachment_type.TEXT)
                    assert False
            else:
                allure.attach(body=f'MFC{i+1}[{mfc}] curr pv is {pv1}, expect is greater than zero', name='Error', attachment_type=allure.attachment_type.TEXT)
                assert False

    @pytest.mark.asyncio
    @pytest.mark.run(order=2)
    @allure.title('test_02')
    async def test_02(self):
        for i, mfc in enumerate(get_mfcs()):
            await set_mfc_sp_source(i, 'Fixed')
            for it in get_mfc_sps(i):
                pv1 = await get_mfc_pv(i)
                await set_mfc_sp(i, it)
                elapsed_time, timeout = await self.pv_close_to_sp(i, it)
                pv2 = await get_mfc_pv(i)
                if elapsed_time is not None:
                    allure.attach(body=f'MFC{i+1}[{mfc}] {pv1}->{it} speed {elapsed_time} s, curr pv is {pv2}', name='Comment', attachment_type=allure.attachment_type.TEXT)
                else:
                    allure.attach(body=f'MFC{i+1}[{mfc}] {pv1}->{it} speed {timeout} s, curr pv is {pv2}', name='Error', attachment_type=allure.attachment_type.TEXT)
                    await set_mfc_sp_source(i, 'Disable')
                    assert False
            await set_mfc_sp_source(i, 'Disable')