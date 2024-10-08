from typing import Any, Callable, Awaitable

from bleak import BleakClient

from ble.ble_constant import BleConstant
from core.models.settings.bt_settings import BTSettings
from proto import brp_pb2 as brp


class SetBluetoothSettingsCommand:
    @staticmethod
    async def send(
            sid: int,
            client: BleakClient,
            bt_settings: BTSettings,
            write_char: Callable[[BleakClient, str, Any], Awaitable[None]]
    ):
        pkt = brp.Packet()
        pkt.sid = sid
        pkt.type = brp.PacketType.PACKET_TYPE_COMMAND
        pkt.command.cid = brp.CommandId.CID_BLE_SETTINGS_SET

        if bt_settings.adv_name is not None:
            pkt.command.all_dev_settings.ble_settings.advertising_name = bt_settings.adv_name

        if bt_settings.adv_interval is not None:
            pkt.command.all_dev_settings.ble_settings.advertising_interval = bt_settings.adv_interval

        if bt_settings.connection_interval_min is not None:
            pkt.command.all_dev_settings.ble_settings.connect_params.connect_intv_min = bt_settings.connection_interval_min

        if bt_settings.connection_interval_max is not None:
            pkt.command.all_dev_settings.ble_settings.connect_params.connect_intv_max = bt_settings.connection_interval_max

        if bt_settings.slave_latency is not None:
            pkt.command.all_dev_settings.ble_settings.connect_params.slave_latency = bt_settings.slave_latency

        if bt_settings.supervision_timeout is not None:
            pkt.command.all_dev_settings.ble_settings.connect_params.supervision_timeout = bt_settings.supervision_timeout

        if bt_settings.transmit_power_level is not None:
            pkt.command.all_dev_settings.ble_settings.tx_power_level = bt_settings.transmit_power_level.to_brp_power_level()

        pkt_value = pkt.SerializeToString()
        await write_char(client, BleConstant.BRS_UUID_CHAR_TX, pkt_value)
