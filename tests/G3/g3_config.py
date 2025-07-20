from api import G3API

_g3api = G3API()

async def start_agit_to_temp(): 
    await _g3api.start_agit_to_temp(get_temp_to_agit())

async def restart_runtime() -> bool:
    return await _g3api.restart_runtime()

'''
    DO
'''
def get_do_sps() -> float:
    return [
        10.0, 
        20.0, 
        30.0
    ]

async def set_do_sp(sp: float):
    await _g3api.set_do_sp(sp)

async def get_do_pv() -> float:
    return await _g3api.get_do_pv()

def get_do_tolerance() -> float:
    return 0.1

async def set_do_profile() -> list:
    return await _g3api.set_do_profile([
        [1, 10],
        [2, 20]
    ])

async def set_do_sp_source(source: str):
    await _g3api.set_do_sp_source(source)

'''
    pH
'''
def get_ph_sps() -> float:
    return [
        10.0, 
        20.0, 
        30.0
    ]

async def set_ph_sp(sp: float):
    await _g3api.set_ph_sp(sp)

async def get_ph_pv() -> float:
    return await _g3api.get_ph_pv()

def get_ph_tolerance() -> float:
    return 0.1

async def set_ph_profile() -> list:
    return await _g3api.set_ph_profile([
        [1, 10],
        [2, 20]
    ])

async def set_ph_sp_source(source: str):
    await _g3api.set_ph_sp_source(source)


'''
    EGA
'''

'''
    RGB
'''

'''
    MFC
'''
def get_mfcs() -> list:
    return [
        'Air',
        'N₂',
        'CO₂',
        'O₂'
    ]

def get_mfc_sps(i: int) -> float:
    return [
        10.0, 
        20.0, 
        30.0
    ]

async def get_mfc_pv(i: int) -> float:
    return await _g3api.get_mfc_pv(i)

def get_mfc_tolerance(i: int) -> float:
    return 0.1

async def set_mfc_sp(i: int, sp: float):
    await _g3api.set_mfc_sp(i, sp)

async def set_mfc_sp_source(i: int, source: str):
    await _g3api.set_mfc_sp_source(i, source)

'''
    Pump
'''
def get_pumps() -> list:
    return [
        'Base',
        'Acid',
        'Feed1',
        'Feed2',
        'Feed3',
        'Feed4'
    ]

def get_pump_sps(i: int) -> float:
    return [
        10.0, 
        20.0, 
        30.0
    ]

async def get_pump_pv(i: int) -> float:
    return await _g3api.get_pump_pv(i)

def get_pump_tolerance(i: int) -> float:
    return 0.1

async def set_pump_sp(i: int, sp: float):
    await _g3api.set_pump_sp(i, sp)

async def set_pump_sp_source(i: int, source: str):
    await _g3api.set_pump_sp_source(i, source)

'''
    Agit
'''
def get_agit_sps() -> float:
    return [
        10.0, 
        20.0, 
        30.0
    ]

async def set_agit_sp(sp: float):
    await _g3api.set_agit_sp(sp)

async def get_agit_pv() -> float:
    return await _g3api.get_agit_pv()

def get_agit_tolerance() -> float:
    return 0.1

async def set_agit_profile() -> list:
    return await _g3api.set_agit_profile([
        [1, 10],
        [2, 20]
    ])

async def set_agit_sp_source(source: str):
    await _g3api.set_agit_sp_source(source)

'''
    Temp
'''
def get_temp_sps() -> float:
    return [
        10.0, 
        20.0, 
        30.0
    ]

def get_temp_to_agit() -> float:
    return 300.

async def set_temp_sp(sp: float):
    await _g3api.set_temp_sp(sp)

async def get_temp_pv() -> float:
    return await _g3api.get_temp_pv()

def get_temp_tolerance() -> float:
    return 0.1

async def set_temp_profile() -> list:
    return await _g3api.set_temp_profile([
        [1, 10],
        [2, 20]
    ])

async def set_temp_sp_source(source: str):
    await _g3api.set_temp_sp_source(source)