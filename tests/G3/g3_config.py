import asyncio

async def start_agit_to_temp(): 
    await asyncio.sleep(2)
    pass

async def restart_runtime() -> bool:
    await asyncio.sleep(2)
    return True


'''
    DO
'''
def get_do_sps() -> float:
    return [
        10.0, 
        20.0, 
        30.0
    ]

async def get_do_pv() -> float:
    await asyncio.sleep(2)
    return 0.

def get_do_tolerance() -> float:
    return 0.1

async def set_do_profile() -> list:
    await asyncio.sleep(2)
    return [
        [1, 10],
        [2, 20]
    ]

async def set_do_sp(sp: float) -> float:
    await asyncio.sleep(2)

async def set_do_sp_source(source: str = 'Fixed'):
    await asyncio.sleep(2)

'''
    pH
'''
def get_ph_sps() -> float:
    return [
        10.0, 
        20.0, 
        30.0
    ]

async def get_ph_pv() -> float:
    await asyncio.sleep(2)
    return 0.

def get_ph_tolerance() -> float:
    return 0.1

async def set_ph_profile() -> list:
    await asyncio.sleep(2)
    return [
        [1, 10],
        [2, 20]
    ]

async def set_ph_sp(sp: float) -> float:
    await asyncio.sleep(2)

async def set_ph_sp_source(source: str = 'Fixed'):
    await asyncio.sleep(2)

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
        'N',
        'CO',
        'O'
    ]

def get_mfc_sps(i: int) -> float:
    return [
        10.0, 
        20.0, 
        30.0
    ]

async def get_mfc_pv(i: int) -> float:
    await asyncio.sleep(2)
    return 0.

def get_mfc_tolerance(i: int) -> float:
    return 0.1

async def set_mfc_sp(i: int, sp: float) -> float:
    await asyncio.sleep(2)

async def set_mfc_sp_source(i: int, source: str = 'Fixed'):
    await asyncio.sleep(2)

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
    await asyncio.sleep(2)
    return 0.

def get_pump_tolerance(i: int) -> float:
    return 0.1

async def set_pump_sp(i: int, sp: float) -> float:
    await asyncio.sleep(2)

async def set_pump_sp_source(i: int, source: str = 'Fixed'):
    await asyncio.sleep(2)

'''
    Agit
'''
def get_agit_sps() -> float:
    return [
        10.0, 
        20.0, 
        30.0
    ]

async def get_agit_pv() -> float:
    await asyncio.sleep(2)
    return 0.

def get_agit_tolerance() -> float:
    return 0.1

async def set_agit_profile() -> list:
    await asyncio.sleep(2)
    return [
        [1, 10],
        [2, 20]
    ]

async def set_agit_sp(sp: float) -> float:
    await asyncio.sleep(2)

async def set_agit_sp_source(source: str = 'Fixed'):
    await asyncio.sleep(2)

'''
    Temp
'''
def get_temp_sps() -> float:
    return [
        10.0, 
        20.0, 
        30.0
    ]

async def get_temp_pv() -> float:
    await asyncio.sleep(2)
    return 0.

def get_temp_to_agit() -> float:
    return 300.

def get_temp_tolerance() -> float:
    return 0.1

async def set_temp_profile() -> list:
    await asyncio.sleep(2)
    return [
        [1, 10],
        [2, 20]
    ]

async def set_temp_sp(sp: float) -> float:
    await asyncio.sleep(2)

async def set_temp_sp_source(source: str = 'Fixed'):
    await asyncio.sleep(2)