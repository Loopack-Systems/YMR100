
class ConstCode:
    FRAME_BEGIN_HEX = "BB"
    FRAME_END_HEX = "7E"
    FRAME_BEGIN_BYTE = 187
    FRAME_END_BYTE = 126
    FRAME_TYPE_CMD = "00"
    FRAME_TYPE_ANS = "01"
    FRAME_TYPE_INFO = "02"
    
    # Commands
    CMD_GET_MODULE_INFO = "03"
    CMD_SET_QUERY = "0E"
    CMD_GET_QUERY = "0D"
    CMD_INVENTORY = "22"
    CMD_READ_MULTI = "27"
    CMD_STOP_MULTI = "28"
    CMD_READ_DATA = "39"
    CMD_WRITE_DATA = "49"
    CMD_LOCK_UNLOCK = "82"
    CMD_KILL = "65"
    CMD_SET_REGION = "07"
    CMD_SET_RF_CHANNEL = "AB"
    CMD_GET_RF_CHANNEL = "AA"
    CMD_SET_POWER = "B6"
    CMD_GET_POWER = "B7"
    CMD_SET_FHSS = "AD"
    CMD_SET_CW = "B0"
    CMD_SET_MODEM_PARA = "F0"
    CMD_READ_MODEM_PARA = "F1"
    CMD_SET_SELECT_PARA = "0C"
    CMD_GET_SELECT_PARA = "0B"
    CMD_SET_INVENTORY_MODE = "12"
    CMD_SCAN_JAMMER = "F2"
    CMD_SCAN_RSSI = "F3"
    CMD_IO_CONTROL = "1A"
    CMD_RESTART = "19"
    CMD_SET_READER_ENV_MODE = "F5"
    CMD_INSERT_FHSS_CHANNEL = "A9"
    CMD_SLEEP_MODE = "17"
    CMD_SET_SLEEP_TIME = "1D"
    CMD_LOAD_NV_CONFIG = "0A"
    CMD_SAVE_NV_CONFIG = "09"
    CMD_NXP_CHANGE_CONFIG = "E0"
    CMD_NXP_READPROTECT = "E1"
    CMD_NXP_RESET_READPROTECT = "E2"
    CMD_NXP_CHANGE_EAS = "E3"
    CMD_NXP_EAS_ALARM = "E4"
    CMD_IPJ_MONZA_QT_READ = "E5"
    CMD_IPJ_MONZA_QT_WRITE = "E6"
    CMD_EXE_FAILED = "FF"
    
    # Fail Codes
    FAIL_INVALID_PARA = "0E"
    FAIL_INVENTORY_TAG_TIMEOUT = "15"
    FAIL_INVALID_CMD = "17"
    FAIL_FHSS_FAIL = "20"
    FAIL_ACCESS_PWD_ERROR = "16"
    FAIL_READ_MEMORY_NO_TAG = "09"
    FAIL_READ_ERROR_CODE_BASE = "A0"
    FAIL_WRITE_MEMORY_NO_TAG = "10"
    FAIL_WRITE_ERROR_CODE_BASE = "B0"
    FAIL_LOCK_NO_TAG = "13"
    FAIL_LOCK_ERROR_CODE_BASE = "C0"
    FAIL_KILL_NO_TAG = "12"
    FAIL_KILL_ERROR_CODE_BASE = "D0"
    FAIL_NXP_CHANGE_CONFIG_NO_TAG = "1A"
    FAIL_NXP_READPROTECT_NO_TAG = "2A"
    FAIL_NXP_RESET_READPROTECT_NO_TAG = "2B"
    FAIL_NXP_CHANGE_EAS_NO_TAG = "1B"
    FAIL_NXP_CHANGE_EAS_NOT_SECURE = "1C"
    FAIL_NXP_EAS_ALARM_NO_TAG = "1D"
    FAIL_IPJ_MONZA_QT_NO_TAG = "2E"
    FAIL_CUSTOM_CMD_BASE = "E0"
    
    # Error Codes
    ERROR_CODE_OTHER_ERROR = 0
    ERROR_CODE_MEM_OVERRUN = 3
    ERROR_CODE_MEM_LOCKED = 4
    ERROR_CODE_INSUFFICIENT_POWER = 11
    ERROR_CODE_NON_SPEC_ERROR = 15
    
    # Success Message
    SUCCESS_MSG_DATA = "00"
    
    # Region Codes
    REGION_CODE_CHN2 = "01"
    REGION_CODE_US = "02"
    REGION_CODE_EUR = "03"
    REGION_CODE_CHN1 = "04"
    REGION_CODE_JAPAN = "05"
    REGION_CODE_KOREA = "06"
    
    # Settings
    SET_ON = "FF"
    SET_OFF = "00"
    INVENTORY_MODE0 = "00"
    INVENTORY_MODE1 = "01"
    INVENTORY_MODE2 = "02"
    
    # Module Fields
    MODULE_HARDWARE_VERSION_FIELD = "00"
    MODULE_SOFTWARE_VERSION_FIELD = "01"
    MODULE_MANUFACTURE_INFO_FIELD = "02"
    
    # EXTRA CONFIG
    MAX_POWER = 26
    MAX_MULTI_READ_LOOP = 65535

    class NVconfig:
        NVdisable = 0
        NVenable = 1

class Commands:
    @staticmethod
    def hex_to_dbm(hex_bytes):
        """
        Convert a 2-byte hexadecimal string to a dBm value.
        Example: '0A28' -> 26.00 dBm
        """
        # Convert hex string to decimal
        decimal_value = int(hex_bytes, 16)
        # Convert to dBm (divide by 100)
        dbm_value = decimal_value / 100
        return dbm_value
    @staticmethod

    def dbm_to_hex(dbm_value):
        """
        Convert a dBm value to a 2-byte hexadecimal string.
        Example: 26.00 dBm -> '0A28'
        """
        # Multiply dBm by 100 and convert to a 4-character hex string
        decimal_value = int(dbm_value * 100)
        hex_bytes = f"{decimal_value:04X}"
        return hex_bytes
    
    @staticmethod
    def calc_checksum(data):
        """Calculate the checksum of the given hex string."""
        if data is None:
            return ""
        num = 0
        data = data.replace(" ", "")
        try:
            for i in range(0, len(data), 2):
                num += int(data[i:i + 2], 16)
        except Exception as e:
            print(f"Checksum error: {e}")
        return f"{num % 256:02X}"

    @staticmethod
    def build_frame(data):
        """Build a frame using the given data."""
        if data is None:
            return ""
        data = data.replace(" ", "")
        checksum = Commands.calc_checksum(data)
        return f"BB{data}{checksum}7E"

    @staticmethod
    def build_frame_with_msg(msg_type, cmd_code):
        """Build a frame with message type and command code."""
        if msg_type is None or cmd_code is None:
            return ""
        msg_type = msg_type.replace(" ", "").zfill(2)
        cmd_code = cmd_code.replace(" ", "").zfill(2)
        return Commands.auto_add_space(f"BB{msg_type}{cmd_code}0000{cmd_code}7E")

    @staticmethod
    def build_frame_with_data(msg_type, cmd_code, data):
        """Build a frame with message type, command code, and data."""
        if msg_type is None or cmd_code is None:
            return ""
        msg_type = msg_type.replace(" ", "").zfill(2)
        cmd_code = cmd_code.replace(" ", "").zfill(2)
        if data:
            data = data.replace(" ", "").zfill(2)
            length = len(data) // 2
            data = data[:length * 2]
        else:
            length = 0
        frame_data = f"{msg_type}{cmd_code}{length:04X}{data}"
        checksum = Commands.calc_checksum(frame_data)
        return Commands.auto_add_space(f"BB{frame_data}{checksum}7E")

    @staticmethod
    def auto_add_space(data):
        """Add a space after every two characters."""
        if data is None or len(data) == 0:
            return ""
        return " ".join(data[i:i+2] for i in range(0, len(data), 2))

    @staticmethod
    def build_read_multi_frame(loop_num):
        """Build a frame to start multi-reading."""
        if loop_num <= 0 or loop_num > 65536:
            return ""
        return Commands.build_frame_with_data("00", "27", f"22{loop_num:04X}")

    @staticmethod
    def build_stop_read_frame():
        """Build a frame to stop multi-reading."""
        return Commands.build_frame_with_msg("00", "28")

    @staticmethod
    def build_set_pa_power_frame(power_dbm):
        """Build a frame to set PA power."""
        assert -9 <= power_dbm <= 26
        power_dbm = Commands.dbm_to_hex(power_dbm)
        return Commands.build_frame_with_data("00", "B6", power_dbm)

    @staticmethod
    def build_get_pa_power_frame():
        """Build a frame to get PA power."""
        return Commands.build_frame_with_msg("00", "B7")

    @staticmethod
    def build_set_inventory_mode_frame(mode):
        """Build a frame to set the inventory mode."""
        if mode not in [ConstCode.INVENTORY_MODE0, ConstCode.INVENTORY_MODE1, ConstCode.INVENTORY_MODE2]:
            return ""
        return Commands.build_frame_with_data("00", "12", mode)
    
    @staticmethod
    def build_set_region_frame(region):
        """Build a frame to set the region."""
        if region not in [ConstCode.REGION_CODE_CHN2, ConstCode.REGION_CODE_US, ConstCode.REGION_CODE_EUR,
                          ConstCode.REGION_CODE_CHN1, ConstCode.REGION_CODE_JAPAN, ConstCode.REGION_CODE_KOREA]:
            return ""
        return Commands.build_frame_with_data("00", ConstCode.CMD_SET_REGION, region)

    @staticmethod
    def build_read_data_frame(access_pwd, mem_bank, sa, dl):
        """Build a frame to read data."""
        access_pwd = access_pwd.replace(" ", "")
        if len(access_pwd) != 8:
            return ""
        return Commands.build_frame_with_data("00", "39", f"{access_pwd}{mem_bank:02X}{sa:04X}{dl:04X}")

    @staticmethod
    def build_write_data_frame(access_pwd, mem_bank, sa, dl, data):
        """Build a frame to write data."""
        access_pwd = access_pwd.replace(" ", "")
        if len(access_pwd) != 8:
            return ""
        data = data.replace(" ", "")
        return Commands.build_frame_with_data("00", "49", f"{access_pwd}{mem_bank:02X}{sa:04X}{dl:04X}{data}")

    @staticmethod
    def build_lock_frame(access_pwd, ld):
        """Build a frame to lock a tag."""
        access_pwd = access_pwd.replace(" ", "")
        if len(access_pwd) != 8:
            return ""
        return Commands.build_frame_with_data("00", "82", f"{access_pwd}{ld:06X}")

    @staticmethod
    def build_kill_frame(kill_pwd, rfu=0):
        """Build a frame to kill a tag."""
        kill_pwd = kill_pwd.replace(" ", "")
        if len(kill_pwd) != 8:
            return ""
        data = kill_pwd + (f"{rfu:02X}" if rfu != 0 else "")
        return Commands.build_frame_with_data("00", "65", data)
