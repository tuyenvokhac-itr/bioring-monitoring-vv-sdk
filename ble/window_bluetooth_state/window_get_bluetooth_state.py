# import asyncio
# from winrt.windows.devices import radios
#
# async def get_bluetooth_state():
#     radios_list = await radios.Radio.get_radios_async()
#     for radio in radios_list:
#         if radio.kind == radios.RadioKind.BLUETOOTH:
#             if radio.state == radios.RadioState.ON:
#                 return "ON"
#             elif radio.state == radios.RadioState.OFF:
#                 return "OFF"
#             else:
#                 return f"Bluetooth state: {radio.state}"
#     return "Bluetooth radio not found"
