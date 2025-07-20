from s7client import S7Client

class G3API:

    _client: None
    
    _addr_run: 200
    _addr_do_pv: 1
    _addr_do_sp: 1
    _addr_do_sp_source: 1

    _addr_ph_pv: 1
    _addr_ph_sp: 1
    _addr_ph_sp_source: 1

    _addr_mfc_pv: 1
    _addr_mfc_sp: 1
    _addr_mfc_sp_source: 1

    _addr_pump_pv: 1
    _addr_pump_sp: 1
    _addr_pump_sp_source: 1

    _addr_agit_pv: 1
    _addr_agit_sp: 1
    _addr_agit_sp_source: 1

    _addr_temp_pv: 1
    _addr_temp_sp: 1
    _addr_temp_sp_source: 1

    def __init__(self, ip: str = '127.0.0.1', rack: int = 0, slot: int = 0):
        self._client = S7Client(ip, rack, slot)

    def get_index_by_source(self, source: str) -> int:
        if source == 'Fixed':
            return 1
        elif source == 'Profile':
            return 2
        return 0

    async def start_agit_to_temp(self, sp: float):
        await self.set_agit_sp_source('Fixed')
        await self.set_agit_sp(sp)

    async def restart_runtime(self) -> bool:
        await self._client.write_u16(self._addr_run, [0])
        await self._client.write_u16(self._addr_run, [1])
        return await self._client.read_u16(self._addr_run)
        
    '''
        DO
    '''
    async def get_do_pv(self) -> float:
        return await self._client.read_f32(self._addr_do_pv)

    async def set_do_sp(self, sp: float):
        await self._client.write_f32(self._addr_do_sp, [sp])

    async def set_do_sp_source(self, source: str):
        index = self.get_index_by_source(source)
        await self._client.write_u16(self._addr_do_sp_source, [index])

    async def set_do_profile(self, list: list) -> list:
        return list
    
    '''
        pH
    '''
    async def get_ph_pv(self) -> float:
        return await self._client.read_f32(self._addr_ph_pv)

    async def set_ph_sp(self, sp: float):
        await self._client.write_f32(self._addr_ph_sp, [sp])

    async def set_ph_sp_source(self, source: str):
        index = self.get_index_by_source(source)
        await self._client.write_u16(self._addr_ph_sp_source, [index])

    async def set_ph_profile(self, list: list) -> list:
        return list
    
    '''
        MFC
    '''
    async def get_mfc_pv(self, i: int) -> float:
        addr = self._addr_mfc_pv
        return await self._client.read_f32(addr)

    async def set_mfc_sp(self, i: int, sp: float):
        addr = self._addr_mfc_sp
        await self._client.write_f32(addr, [sp])

    async def set_mfc_sp_source(self, i: int, source: str):
        addr = self._addr_mfc_sp_source
        index = self.get_index_by_source(source)
        await self._client.write_u16(addr, [index])

    '''
        Pump
    '''
    async def get_pump_pv(self, i: int) -> float:
        addr = self._addr_pump_pv
        return await self._client.read_f32(addr)

    async def set_pump_sp(self, i: int, sp: float):
        addr = self._addr_pump_sp
        await self._client.write_f32(addr, [sp])

    async def set_pump_sp_source(self, i: int, source: str):
        addr = self._addr_pump_sp_source
        index = self.get_index_by_source(source)
        await self._client.write_u16(addr, [index])

    '''
        Agit
    '''
    async def get_agit_pv(self) -> float:
        return await self._client.read_f32(self._addr_agit_pv)

    async def set_agit_sp(self, sp: float):
        await self._client.write_f32(self._addr_agit_sp, [sp])

    async def set_agit_sp_source(self, source: str):
        index = self.get_index_by_source(source)
        await self._client.write_u16(self._addr_agit_sp_source, [index])

    async def set_agit_profile(self, list: list) -> list:
        return list
    
    '''
        Temp
    '''
    async def get_temp_pv(self) -> float:
        return await self._client.read_f32(self._addr_temp_pv)

    async def set_temp_sp(self, sp: float):
        await self._client.write_f32(self._addr_temp_sp, [sp])

    async def set_temp_sp_source(self, source: str):
        index = self.get_index_by_source(source)
        await self._client.write_u16(self._addr_temp_sp_source, [index])

    async def set_temp_profile(self, list: list) -> list:
        return list