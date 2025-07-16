import asyncio

async def start_agit_to_temp(): 
    await asyncio.sleep(2)
    pass

async def restart_runtime() -> bool:
    await asyncio.sleep(2)
    return True

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