from ble.bt_device import BTDevice
from core.handler.notification.data_recording.acc.record_acc_data_handler import RecordAccDataHandler
from core.handler.notification.data_recording.afe.record_afe_data_handler import RecordAfeDataHandler
from core.handler.notification.data_recording.temp.record_temp_data_handler import RecordTempDataHandler
from core.handler.notification.streaming.acc.live_acc_data_handler import LiveAccDataHandler
from core.handler.notification.streaming.afe.live_afe_data_handler import LiveAfeDataHandler
from core.handler.notification.streaming.temp.live_temp_data_handler import LiveTempDataHandler
from core.handler.response.dfu.res_enter_dfu_handler import ResEnterDfuHandler
from core.handler.response.general.res_device_info_handler import ResDeviceInfoHandler
from core.handler.response.general.res_device_status_handler import ResDeviceStatusHandler
from core.handler.response.general.res_protocol_info_handler import ResProtocolInfoHandler
from core.handler.response.res_common_result_handler import ResCommonResultHandler
from core.handler.response.self_tests.res_bist_handler import ResBistHandler
from core.handler.response.self_tests.res_post_handler import ResPostHandler
from core.handler.response.settings.res_all_settings_handler import ResAllSettingsHandler
from core.handler.response.time_syncing.res_time_syncing_handler import ResTimeSyncingHandler
from proto import brp_pb2 as brp


class RxCharHandler:
    def __init__(
            self,
            device: BTDevice,
            response_callbacks,
            streaming_callbacks,
    ):
        self.device = device
        self.response_callbacks = response_callbacks
        self.streaming_callbacks = streaming_callbacks
        self.prev_acc_sequence_number = 0
        self.prev_afe_sequence_number = 0
        self.prev_temp_sequence_number = 0

    def handle(self, _sender, data: bytearray):
        rx_packet = brp.Packet()
        rx_packet.ParseFromString(bytes(data))

        pkt_type = rx_packet.WhichOneof("payload")
        if pkt_type == "response":
            cid = rx_packet.response.cid
            self.rx_response_handlers(cid, rx_packet)

        elif pkt_type == "notification":
            nid = rx_packet.notification.nid
            self.rx_notif_handlers(nid, rx_packet)

    def rx_response_handlers(self, cid: int, pkt: brp.Packet):
        print(f"Received response: {pkt}")
        match cid:
            case brp.CommandId.CID_DEV_INFO_GET:
                ResDeviceInfoHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_BLE_SETTINGS_SET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_SELF_TEST_POST_GET:
                ResPostHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_SELF_TEST_BIST_GET:
                ResBistHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_SELF_TEST_BIST_ENABLE:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_SELF_TEST_BIST_DISABLE:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_SELF_TEST_BIST_SET_INTERVAL:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_ALL_SETTINGS_GET:
                ResAllSettingsHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_LOG_SETTINGS_SET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_ECG_SETTINGS_SET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_PPG_SETTINGS_SET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_ACCEL_SETTINGS_SET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_DEV_PRE_SLEEP_TIMEOUT_SET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_TIME_SET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_TIME_GET:
                ResTimeSyncingHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_DEV_INFO_GET:
                ResDeviceInfoHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_DEV_STATUS_GET:
                ResDeviceStatusHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_PROTOCOL_INFO_GET:
                ResProtocolInfoHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_DEV_FACTORY_RESET:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_REBOOT:
                ResCommonResultHandler.handle(pkt, self.response_callbacks)
            case brp.CommandId.CID_DFU_ENTER:
                ResEnterDfuHandler.handle(pkt, self.response_callbacks)
            case _:
                pass

    def rx_notif_handlers(self, nid: int, pkt: brp.Packet):
        match nid:
            case brp.NotificationId.NID_STREAMING_DATA_RAW_ACCEL:
                LiveAccDataHandler.handle(
                    pkt, self.streaming_callbacks,
                    self.prev_acc_sequence_number,
                    self.on_acc_sequence_number_updated,
                )
            case brp.NotificationId.NID_STREAMING_DATA_RAW_AFE:
                LiveAfeDataHandler.handle(
                    pkt, self.streaming_callbacks,
                    self.prev_afe_sequence_number,
                    self.on_afe_sequence_number_updated,
                )
            case brp.NotificationId.NID_STREAMING_DATA_TEMP:
                LiveTempDataHandler.handle(
                    pkt, self.streaming_callbacks,
                    self.prev_temp_sequence_number,
                    self.on_temp_sequence_number_updated,
                )
            case brp.NotificationId.NID_RECORD_DATA_RAW_ACCEL:
                RecordAccDataHandler.handle(self.device, pkt)
            case brp.NotificationId.NID_RECORD_DATA_RAW_AFE:
                RecordAfeDataHandler.handle(self.device, pkt)
            case brp.NotificationId.NID_RECORD_DATA_TEMP:
                RecordTempDataHandler.handle(self.device, pkt)
            case _:
                pass

    def on_acc_sequence_number_updated(self, sequence_number: int):
        self.prev_acc_sequence_number = sequence_number

    def on_afe_sequence_number_updated(self, sequence_number: int):
        self.prev_afe_sequence_number = sequence_number

    def on_temp_sequence_number_updated(self, sequence_number: int):
        self.prev_temp_sequence_number = sequence_number
