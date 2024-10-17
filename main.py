from bioring_tool import BioRingTool
from logger.custom_logger import enable_logger
from psoc6_dfu.src.dfu_utils import DfuUtils


def main():
    enable_logger()
    tool = BioRingTool()


if __name__ == "__main__":
    main()


    # a = 0x03 + 0x00 + 0xb0 + 0x00 + 0x10 + 0xfc +0x7f + 0x06 + 0x00
    # b = 0x02 + 0x44
    # print(a)
    # print(b)
    # DfuUtils.build_cmd_set_metadata2(3, 268480512, 425980)