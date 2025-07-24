from s7client import S7Client

g_mcu_ip = '106.14.19.189'
g_mcu_port = 10067

g_mfcs = ['Air']
g_pumps = ['Base', 'Acid', 'Feed', 'Feed']

g_agit_sps = [100.0, 200.0, 400.0]
g_pump_sps = [50.0, 100.0, 200.0]
g_temp_sps = [10.0, 20.0, 40.0]
g_do_sps = [10.0, 20.0, 30.0]
g_mfc_sps = [1.0, 2.0, 3.0]
g_ph_sps = [1.0, 4.0, 8.0]
g_temp_to_agit = 300.0

g_tolerance_do = 0.1
g_tolerance_ph = 0.01
g_tolerance_mfc = 0.1
g_tolerance_pump = 0.1
g_tolerance_agit = 0.1
g_tolerance_temp = 0.01

g_profile_do: list = [
    [0.00, 10.0],
    [0.01, 20.0],
    [0.02, 30.0],
    [0.03, 40.0],
    [0.04, 50.0],
    [0.05, 60.0],
    [0.06, 70.0],
    [0.07, 80.0],
    [0.08, 90.0],
    [0.09, 100.0]
]
g_profile_ph: list = [
    [0.00, 7.11],
    [0.01, 7.12],
    [0.02, 7.13],
    [0.03, 7.14],
    [0.04, 7.15],
    [0.05, 7.16],
    [0.06, 7.17],
    [0.07, 7.18],
    [0.08, 7.19],
    [0.09, 7.20]
]
g_profile_pump: list = [
    [0.01, 100.0, 1.0],
    [0.02, 200.0, 2.0],
    [0.03, 100.0, 1.0],
    [0.04, 200.0, 2.0],
    [0.05, 100.0, 1.0],
    [0.06, 200.0, 2.0],
    [0.07, 100.0, 1.0],
    [0.08, 200.0, 2.0],
    [0.09, 100.0, 1.0],
    [0.10, 200.0, 2.0]
]
g_profile_agit: list = [
    [0.00, 50],
    [0.01, 100],
    [0.02, 200],
    [0.03, 300],
    [0.04, 400],
    [0.05, 500],
    [0.06, 600],
    [0.07, 700],
    [0.08, 800],
    [0.09, 900]
]
g_profile_temp: list = [
    [0.00, 35.1],
    [0.01, 35.2],
    [0.02, 35.3],
    [0.03, 35.4],
    [0.04, 35.5],
    [0.05, 35.6],
    [0.06, 35.7],
    [0.07, 35.8],
    [0.08, 35.9],
    [0.09, 36.0]
]

g_map_mfc = {
    'Air': 1,
    'O₂' : 2,
    'N₂' : 3,
    'CO₂': 4
}
g_map_pump = {
    'Base': 1,
    'Acid': 2,
    'AF'  : 3,
    'Feed': 4
}

class G3API:

    _client: S7Client
    
    _addr_run: int = 2905

    _addr_do_pv: int = 2576
    _addr_do_sp: int = 2514
    _addr_do_profile: int = 1451
    _addr_do_sp_source: int = 1450
    _addr_do_enable_profile: int = 2872

    _addr_ph_pv: int = 2574
    _addr_ph_sp: int = 2512
    _addr_ph_profile: int = 1851
    _addr_ph_sp_source: int = 1850
    _addr_ph_enable_profile: int = 2862

    _addr_mfc_pv: int = 2580
    _addr_mfc_sp: int = 2518
    _addr_mfc_sp_source: int = 1301

    _addr_pump_pv: int = 2550
    _addr_pump_sp: int = 2500
    _addr_pump_profile: int = 134
    _addr_pump_sp_source: int = 101
    _addr_pump_enable_profile: int = 2759

    _addr_agit_pv: int = 2588
    _addr_agit_sp: int = 2526
    _addr_agit_profile: int = 1351
    _addr_agit_sp_source: int = 1350
    _addr_agit_enable_profile: int = 2900

    _addr_temp_pv: int = 2578
    _addr_temp_sp: int = 2516
    _addr_temp_profile: int = 2251
    _addr_temp_sp_source: int = 2250
    _addr_temp_enable_profile: int = 2882

    def __init__(self, ip: str = g_mcu_ip, port: int = g_mcu_port, rack: int = 0, slot: int = 0):
        self._client = S7Client(ip, port, rack, slot)

    def get_sensor_index_by_source(self, source: str) -> int:
        if source == 'Profile':
            return 1
        return 0

    def get_index_by_source(self, source: str) -> int:
        if source == 'Fixed':
            return 1
        elif source == 'Profile':
            return 10
        return 0

    async def restart_runtime(self) -> bool:
        self._client.write_u16(self._addr_run, [0])
        self._client.write_u16(self._addr_run, [1])
        res = self._client.read_u16(self._addr_run)
        return False if res is None else res[0] == 1

    async def start_agit_to_temp(self, sp: float = g_temp_to_agit) -> bool:
        return True # TODO
        return await self.set_agit_sp_source('Fixed') and await self.set_agit_sp(sp)

    '''
        DO
    '''
    def get_do_sps(self) -> float:
        return g_do_sps
    
    def get_do_tolerance(self) -> float:
        return g_tolerance_do
    
    async def get_do_pv(self) -> float:
        res = self._client.read_f32(self._addr_do_pv)
        return float('nan') if res is None else res[0] 

    async def set_do_profile(self) -> list:
        if g_profile_do is None:
            return None
        self._client.write_f32(self._addr_do_profile, [item for sublist in g_profile_do for item in sublist])
        return g_profile_do
    
    async def set_do_sp(self, sp: float) -> bool:
        return self._client.write_f32(self._addr_do_sp, [sp])

    async def set_do_sp_source(self, source: str) -> bool:
        index = self.get_sensor_index_by_source(source)
        return self._client.write_u16(self._addr_do_sp_source, [index]) and self._client.write_u16(self._addr_do_enable_profile, [1 if index == 1 else 0])
    
    '''
        pH
    '''
    def get_ph_sps(self) -> float:
        return g_ph_sps
    
    def get_ph_tolerance(self) -> float:
        return g_tolerance_ph
    
    async def get_ph_pv(self) -> float:
        res = self._client.read_f32(self._addr_ph_pv)
        return float('nan') if res is None else res[0] 

    async def set_ph_profile(self) -> list:
        if g_profile_ph is None:
            return None
        self._client.write_f32(self._addr_ph_profile, [item for sublist in g_profile_ph for item in sublist])
        return g_profile_ph

    async def set_ph_sp(self, sp: float) -> bool:
        return self._client.write_f32(self._addr_ph_sp, [sp])

    async def set_ph_sp_source(self, source: str) -> bool:
        index = self.get_sensor_index_by_source(source)
        return self._client.write_u16(self._addr_ph_sp_source, [index]) and self._client.write_u16(self._addr_ph_enable_profile, [1 if index == 1 else 0])

    '''
        MFC
    '''
    def get_mfcs(self) -> list:
        return g_mfcs

    def get_mfc_sps(self, i: int) -> float:
        return g_mfc_sps
    
    def get_mfc_tolerance(self, i: int) -> float:
        return g_tolerance_mfc
    
    async def get_mfc_pv(self, i: int) -> float:
        addr = self._addr_mfc_pv + i * 2
        res = self._client.read_f32(addr)
        return float('nan') if res is None else res[0] 

    async def set_mfc_sp(self, i: int, sp: float) -> bool:
        addr = self._addr_mfc_sp + i * 2
        success = self._client.write_f32(addr, [sp])
        addr = self._addr_mfc_sp_source - 1 + i * 10
        return success and self._client.write_u16(addr, [g_map_mfc[g_mfcs[i]]])

    async def set_mfc_sp_source(self, i: int, source: str) -> bool:
        addr = self._addr_mfc_sp_source + i * 10
        index = self.get_index_by_source(source)
        return self._client.write_u16(addr, [index])

    '''
        Pump
    '''
    def get_pumps(self) -> list:
        return g_pumps

    def get_pump_sps(self, i: int) -> float:
        return g_pump_sps
    
    def get_pump_tolerance(self, i: int) -> float:
        return g_tolerance_pump
    
    async def get_pump_pv(self, i: int) -> float:
        addr = self._addr_pump_pv + i * 4
        res = self._client.read_f32(addr)
        return float('nan') if res is None else res[0] 

    async def set_pump_sp(self, i: int, sp: float) -> bool:
        addr = self._addr_pump_sp + i * 2
        success = self._client.write_f32(addr, [sp])
        addr = self._addr_pump_sp_source - 1 + i * 200
        return success and self._client.write_u16(addr, [g_map_pump[g_pumps[i]]])

    async def set_pump_profile(self, i: int) -> list:
        if g_profile_pump is None:
            return None
        self._client.write_f32(self._addr_pump_profile + i * 200, [item for sublist in g_profile_pump for item in sublist])
        return g_profile_pump

    async def set_pump_sp_source(self, i: int, source: str) -> bool:
        index = self.get_index_by_source(source)
        addr = self._addr_pump_sp_source + i * 200
        success = self._client.write_u16(addr, [index])
        addr = self._addr_pump_enable_profile + i * 15
        return success and self._client.write_u16(addr, [1 if index == 10 else 0])

    '''
        Agit
    '''
    def get_agit_sps(self) -> float:
        return g_agit_sps
    
    def get_agit_tolerance(self) -> float:
        return g_tolerance_agit
    
    async def get_agit_pv(self) -> float:
        res = self._client.read_f32(self._addr_agit_pv)
        return float('nan') if res is None else res[0]

    async def set_agit_profile(self) -> list:
        if g_profile_agit is None:
            return None
        self._client.write_f32(self._addr_agit_profile, [item for sublist in g_profile_agit for item in sublist])
        return g_profile_agit
    
    async def set_agit_sp(self, sp: float) -> bool:
        return self._client.write_f32(self._addr_agit_sp, [sp])

    async def set_agit_sp_source(self, source: str) -> bool:
        index = self.get_index_by_source(source)
        return self._client.write_u16(self._addr_agit_sp_source, [index]) and self._client.write_u16(self._addr_agit_enable_profile, [1 if index == 10 else 0])

    '''
        Temp
    '''
    def get_temp_sps(self) -> float:
        return g_temp_sps
    
    def get_temp_tolerance(self) -> float:
        return g_tolerance_temp
    
    async def get_temp_pv(self) -> float:
        res = self._client.read_f32(self._addr_temp_pv)
        return float('nan') if res is None else res[0]

    async def set_temp_profile(self) -> list:
        if g_profile_temp is None:
            return None
        self._client.write_f32(self._addr_temp_profile, [item for sublist in g_profile_temp for item in sublist])
        return g_profile_temp

    async def set_temp_sp(self, sp: float) -> bool:
        return self._client.write_f32(self._addr_temp_sp, [sp])

    async def set_temp_sp_source(self, source: str) -> bool:
        index = self.get_sensor_index_by_source(source)
        return self._client.write_u16(self._addr_temp_sp_source, [index]) and self._client.write_u16(self._addr_temp_enable_profile, [1 if index == 1 else 0])