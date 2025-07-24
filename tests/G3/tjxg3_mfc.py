import math
import pytest
import allure
import asyncio
from api import G3API

@allure.feature("MFC")
@pytest.mark.MFC
class TJXG3MFC:

    _g3api: G3API = G3API()  
    _lock: asyncio.Lock = asyncio.Lock()  

    async def pv_close_to_sp(self, i: int, sp: float, timeout: float = 20.):
        start_time = asyncio.get_running_loop().time()
        tolerance = self._g3api.get_mfc_tolerance(i)
        timeout = max(20., timeout)
        while True:
            elapsed_time = asyncio.get_running_loop().time() - start_time
            pv = await self._g3api.get_mfc_pv(i)
            if elapsed_time > timeout:
                return None, timeout, pv
            if math.fabs(sp - pv) < tolerance:
                return elapsed_time, timeout, pv
            await asyncio.sleep(3)

    @pytest.mark.asyncio
    @pytest.mark.run(order=1)
    @allure.title('test_01')
    async def test_01(self):
        async with self._lock:
            for i, mfc in enumerate(self._g3api.get_mfcs()):
                assert await self._g3api.set_mfc_sp_source(i, 'Fixed')
                assert await self._g3api.set_mfc_sp(i, 2.)
                assert await self._g3api.set_mfc_sp_source(i, 'Disable')
                elapsed_time, _, pv = await self.pv_close_to_sp(i, 0.)
                if elapsed_time is not None:
                    allure.attach(body=f'MFC{i+1}[{mfc}] curr pv is {pv}', name='Comment', attachment_type=allure.attachment_type.TEXT)
                    assert True
                else:
                    allure.attach(body=f'MFC{i+1}[{mfc}] curr pv is {pv}, expect is zero', name='Error', attachment_type=allure.attachment_type.TEXT)
                    assert False

    @pytest.mark.asyncio
    @pytest.mark.run(order=2)
    @allure.title('test_02')
    async def test_02(self):
        async with self._lock:
            for i, mfc in enumerate(self._g3api.get_mfcs()):
                assert await self._g3api.set_mfc_sp_source(i, 'Fixed')
                for it in self._g3api.get_mfc_sps(i):
                    pv1 = await self._g3api.get_mfc_pv(i)
                    assert await self._g3api.set_mfc_sp(i, it)
                    elapsed_time, timeout, pv2 = await self.pv_close_to_sp(i, it)
                    if elapsed_time is not None:
                        allure.attach(body=f'MFC{i+1}[{mfc}] {pv1}->{it} speed {elapsed_time} s, curr pv is {pv2}', name='Comment', attachment_type=allure.attachment_type.TEXT)
                    else:
                        allure.attach(body=f'MFC{i+1}[{mfc}] {pv1}->{it} speed {timeout} s, curr pv is {pv2}', name='Error', attachment_type=allure.attachment_type.TEXT)
                        await self._g3api.set_mfc_sp_source(i, 'Disable')
                        assert False
                await self._g3api.set_mfc_sp_source(i, 'Disable')