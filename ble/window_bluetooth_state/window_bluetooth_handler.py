class WindowBluetoothHandler:
    @staticmethod
    async def get_bluetooth_state(on_bt_state):
        print('simulate BT checking')
        on_bt_state(True)