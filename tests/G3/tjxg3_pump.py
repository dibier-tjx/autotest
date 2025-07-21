import math
import pytest
import allure
import asyncio
from api import G3API

@allure.feature("Pump")
@pytest.mark.Pump
class TJXG3Pump:

    _g3api: G3API = G3API()    

    async def pv_close_to_sp(self, i: int, sp: float, timeout: float = 2):
        start_time = asyncio.get_running_loop().time()
        tolerance = self._g3api.get_pump_tolerance(i)
        while True:
            elapsed_time = asyncio.get_running_loop().time() - start_time
            if elapsed_time > timeout:
                return None, timeout
            pv = await self._g3api.get_pump_pv(i)
            if math.fabs(sp - pv) < tolerance:
                return elapsed_time, timeout
            await asyncio.sleep(1)

    @pytest.mark.asyncio
    @pytest.mark.run(order=1)
    @allure.title('test_01')
    async def test_01(self):
        for i, pump in enumerate(self._g3api.get_pumps()):
            await self._g3api.set_pump_sp(i, 3)
            await self._g3api.set_pump_sp_source(i, 'Fixed')
            await asyncio.sleep(2)
            pv1 = await self._g3api.get_pump_pv(i)
            if pv1 > 0:
                await self._g3api.set_pump_sp_source(i, 'Disable')
                await asyncio.sleep(2)
                pv2 = await self._g3api.get_pump_pv(i)
                if math.fabs(pv2) > 1e-10:
                    allure.attach(body=f'Pump{i+1}[{pump}] curr pv is {pv2}, expect is zero', name='Error', attachment_type=allure.attachment_type.TEXT)
                    assert False
            else:
                allure.attach(body=f'Pump{i+1}[{pump}] curr pv is {pv1}, expect is greater than zero', name='Error', attachment_type=allure.attachment_type.TEXT)
                assert False

    @pytest.mark.asyncio
    @pytest.mark.run(order=2)
    @allure.title('test_02')
    async def test_02(self):
        for i, pump in enumerate(self._g3api.get_pumps()):
            await self._g3api.set_pump_sp_source(i, 'Fixed')
            for it in self._g3api.get_pump_sps(i):
                pv1 = await self._g3api.get_pump_pv(i)
                await self._g3api.set_pump_sp(i, it)
                elapsed_time, timeout = await self.pv_close_to_sp(i, it)
                pv2 = await self._g3api.get_pump_pv(i)
                if elapsed_time is not None:
                    allure.attach(body=f'Pump{i+1}[{pump}] {pv1}->{it} speed {elapsed_time} s, curr pv is {pv2}', name='Comment', attachment_type=allure.attachment_type.TEXT)
                else:
                    allure.attach(body=f'Pump{i+1}[{pump}] {pv1}->{it} speed {timeout} s, curr pv is {pv2}', name='Error', attachment_type=allure.attachment_type.TEXT)
                    await self._g3api.set_pump_sp_source(i, 'Disable')
                    assert False
            await self._g3api.set_pump_sp_source(i, 'Disable')

    @pytest.mark.asyncio
    @pytest.mark.run(order=3)
    @allure.title('test_03')
    async def test_03(self):
        for i, pump in enumerate(self._g3api.get_pumps()):
            if pump != 'Feed':
                continue
            profile = await self._g3api.set_pump_profile()
            if profile is not None:
                assert await self._g3api.restart_runtime()
                await self._g3api.set_pump_sp_source(i, 'Profile')
                for it in profile:
                    pv1 = await self._g3api.get_pump_pv(i)
                    elapsed_time, timeout = await self.pv_close_to_sp(it[1], it[0])
                    pv2 = await self._g3api.get_pump_pv(i)
                    if elapsed_time is not None:
                        allure.attach(body=f'{pv1}->{it[1]} speed {elapsed_time} s, curr pv is {pv2}', name='Comment', attachment_type=allure.attachment_type.TEXT)
                    else:
                        allure.attach(body=f'{pv1}->{it[1]} speed {timeout} s, curr pv is {pv2}', name='Error', attachment_type=allure.attachment_type.TEXT)
                        await self._g3api.set_pump_sp_source(i, 'Disable')
                        assert False
                await self._g3api.set_pump_sp_source(i, 'Disable')