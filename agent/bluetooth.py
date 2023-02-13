# SPDX-License-Identifier: MIT
# Copyright (c) 2020 Henrik Blidh
# Copyright (c) 2022 The Pybricks Authors

import asyncio
from bleak import BleakScanner, BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

CHAR_UUID = "f000aa65-0451-4000-b000-000000000000"

def notification_handler(characteristic: BleakGATTCharacteristic, data: bytearray):
    """Simple notification handler which prints the data received."""
    print(f"{characteristic.description}: {data}")

async def main():
    address = await get_address()


    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")
        #breakpoint()
        #paired = await client.pair()
        #print(f"Paired: = {paired}")
        for service in client.services:
            for char in service.characterstics:
                print(char)
                print(service)
        await client.start_notify(CHAR_UUID, notification_handler)

async def get_address():
    devices = await BleakScanner.discover(return_adv=True)
    steve = None

    for d, a in devices.values():
        if (a[0] == "Steve"):
            steve = d

    return steve.address

if __name__ == "__main__":
    asyncio.run(main())