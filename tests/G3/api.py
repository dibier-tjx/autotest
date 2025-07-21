from s7client import S7Client

g_temp_to_agit = 300.0
g_mcu_ip = '127.0.0.1'
g_mcu_port = 102

class G3API:

    _client: S7Client
    
    _addr_run: int = 2905

    _addr_do_pv: int = 2576
    _addr_do_sp: int = 2514
    _addr_do_profile: int = 1451
    _addr_do_sp_source: int = 1450

    _addr_ph_pv: int = 2574
    _addr_ph_sp: int = 2512
    _addr_ph_profile: int = 1851
    _addr_ph_sp_source: int = 1850

    _addr_mfc_pv: int = 2580
    _addr_mfc_sp: int = 2518
    _addr_mfc_sp_source: int = 1301

    _addr_pump_pv: int = 2550
    _addr_pump_sp: int = 2500
    _addr_pump_profile: int = 134
    _addr_pump_sp_source: int = 101

    _addr_agit_pv: int = 2588
    _addr_agit_sp: int = 2526
    _addr_agit_profile: int = 1351
    _addr_agit_sp_source: int = 1350

    _addr_temp_pv: int = 2578
    _addr_temp_sp: int = 2516
    _addr_temp_profile: int = 2251
    _addr_temp_sp_source: int = 2250

    _profile_do: list = [
        [1, 10],
        [2, 20]
    ]
    _profile_ph: list = [
        [1, 10],
        [2, 20]
    ]
    _profile_temp: list = [
        [1, 10],
        [2, 20]
    ]
    _profile_agit: list = [
        [1, 10],
        [2, 20]
    ]
    _profile_temp: list = [
        [1, 10],
        [2, 20]
    ]

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

    async def start_agit_to_temp(self, sp: float = g_temp_to_agit):
        await self.set_agit_sp_source('Fixed')
        await self.set_agit_sp(sp)

    async def restart_runtime(self) -> bool:
        self._client.write_u16(self._addr_run, [0])
        self._client.write_u16(self._addr_run, [1])
        res = self._client.read_u16(self._addr_run)
        return False if res is None else res[0] == 1
        
    '''
        DO
    '''
    def get_do_sps(self) -> float:
        return [
            10.0, 
            20.0, 
            30.0
        ]
    
    def get_do_tolerance(self) -> float:
        return 0.1
    
    async def get_do_pv(self) -> float:
        res = self._client.read_f32(self._addr_do_pv)
        return float('nan') if res is None else res[0] 

    async def set_do_sp(self, sp: float):
        self._client.write_f32(self._addr_do_sp, [sp])

    async def set_do_profile(self) -> list:
        return self._profile_do

    async def set_do_sp_source(self, source: str):
        index = self.get_sensor_index_by_source(source)
        self._client.write_u16(self._addr_do_sp_source, [index])
    
    '''
        pH
    '''
    def get_ph_sps(self) -> float:
        return [
            1.0,
            4.0,
            8.0
        ]
    
    def get_ph_tolerance(self) -> float:
        return 0.1
    
    async def get_ph_pv(self) -> float:
        res = self._client.read_f32(self._addr_ph_pv)
        return float('nan') if res is None else res[0] 

    async def set_ph_sp(self, sp: float):
        self._client.write_f32(self._addr_ph_sp, [sp])

    async def set_ph_profile(self) -> list:
        return self._profile_ph
    
    async def set_ph_sp_source(self, source: str):
        index = self.get_sensor_index_by_source(source)
        self._client.write_u16(self._addr_ph_sp_source, [index])

    '''
        MFC
    '''
    def get_mfcs(self) -> list:
        return [
            'Air',
            'O₂',
            'N₂',
            'CO₂'
        ]

    def get_mfc_sps(self, i: int) -> float:
        return [
            1.0,
            2.0,
            3.0
        ]
    
    def get_mfc_tolerance(self, i: int) -> float:
        return 0.1
    
    async def get_mfc_pv(self, i: int) -> float:
        addr = self._addr_mfc_pv + i * 2
        res = self._client.read_f32(addr)
        return float('nan') if res is None else res[0] 

    async def set_mfc_sp(self, i: int, sp: float):
        addr = self._addr_mfc_sp + i * 2
        self._client.write_f32(addr, [sp])

    async def set_mfc_sp_source(self, i: int, source: str):
        addr = self._addr_mfc_sp_source + i * 10
        index = self.get_index_by_source(source)
        self._client.write_u16(addr, [index])

    '''
        Pump
    '''
    def get_pumps(self) -> list:
        return [
            'Base',
            'Acid',
            'AF',
            'Feed1',
            'Feed2',
            'Feed3'
        ]

    def get_pump_sps(self, i: int) -> float:
        return [
            50.0,
            100.0,
            200.0
        ]
    
    def get_pump_tolerance(self, i: int) -> float:
        return 0.1
    
    async def get_pump_pv(self, i: int) -> float:
        addr = self._addr_pump_pv + i * 4
        res = self._client.read_f32(addr)
        return float('nan') if res is None else res[0] 

    async def set_pump_sp(self, i: int, sp: float):
        addr = self._addr_pump_sp + i * 2
        self._client.write_f32(addr, [sp])

    async def set_pump_sp_source(self, i: int, source: str):
        addr = self._addr_pump_sp_source + i * 200
        index = self.get_index_by_source(source)
        self._client.write_u16(addr, [index])

    '''
        Agit
    '''
    def get_agit_sps(self) -> float:
        return [
            100.0,
            200.0,
            500.0
        ]
    
    def get_agit_tolerance(self) -> float:
        return 0.1
    
    async def get_agit_pv(self) -> float:
        res = self._client.read_f32(self._addr_agit_pv)
        return float('nan') if res is None else res[0]

    async def set_agit_sp(self, sp: float):
        self._client.write_f32(self._addr_agit_sp, [sp])

    async def set_agit_profile(self) -> list:
        return self._profile_agit

    async def set_agit_sp_source(self, source: str):
        index = self.get_index_by_source(source)
        self._client.write_u16(self._addr_agit_sp_source, [index])

    '''
        Temp
    '''
    def get_temp_sps(self) -> float:
        return [
            10.0, 
            20.0, 
            40.0
        ]
    
    def get_temp_tolerance(self) -> float:
        return 0.1
    
    async def get_temp_pv(self) -> float:
        res = self._client.read_f32(self._addr_temp_pv)
        return float('nan') if res is None else res[0]

    async def set_temp_sp(self, sp: float):
        self._client.write_f32(self._addr_temp_sp, [sp])

    async def set_temp_profile(self) -> list:
        return self._profile_temp

    async def set_temp_sp_source(self, source: str):
        index = self.get_sensor_index_by_source(source)
        self._client.write_u16(self._addr_temp_sp_source, [index])