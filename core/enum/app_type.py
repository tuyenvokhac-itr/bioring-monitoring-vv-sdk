from enum import Enum

import proto.brp_pb2 as brp


class AppType(Enum):
    BOOT_LOADER = 0
    APPLICATION = 1

    def to_brp_app_type(self) -> brp.AppType:
        mapping = {
            AppType.BOOT_LOADER: brp.AppType.APP_TYPE_BOOT_LOADER,
            AppType.APPLICATION: brp.AppType.APP_TYPE_APPLICATION,
        }
        return mapping.get(self, None)
