import os
import serial
import threading
import time
from typing import List, Callable
from Reader_Cmds import ConstCode, Commands
#from dotenv import load_dotenv
#load_dotenv(override=True)

class StrArrEventArgs:
    def __init__(self, data):
        self.data = data

total_read_count = 0
# format: 'EPC' : 'count'
tags = {}

class ReceiveParser:
    def __init__(self, ser: serial.Serial):
        self.frame_begin_flag = False
        self.frame_end_flag = True
        self.frame_length = 0
        self.str_num = 0
        self.str_buff = [""] * 4096
        self.packet_received_callback = None
        self.ser = ser

    def set_packet_received_callback(self, callback: Callable[[StrArrEventArgs], None]):
        """Set a callback to handle received packets."""
        self.packet_received_callback = callback
    
    """   
    def _parse_frame(self, frame):
        try:
            buffer = frame
            str_array = [f"{byte:02X}".upper() for byte in buffer]
            
            for index in range(len(str_array)):
                if self.frame_begin_flag:
                    self.str_buff[self.str_num] = str_array[index]

                    # Determine frame length when enough bytes are received
                    if self.str_num == 4:
                        self.frame_length = (256 * int(self.str_buff[3], 16) + int(self.str_buff[4], 16))
                        if self.frame_length > 3072:
                            self.frame_begin_flag = False
                            continue

                    # Check if the entire frame is received
                    if self.str_num == self.frame_length + 6 and self.str_buff[self.str_num] == "7E":
                        # Validate checksum
                        checksum = sum(int(self.str_buff[i], 16) for i in range(1, self.str_num - 1))
                        if checksum % 256 != int(self.str_buff[self.str_num - 1], 16):
                            print("ERROR FRAME: Checksum is not correct!")
                            self.reset_frame()
                            continue

                        # Valid frame received, trigger the callback
                        self.frame_begin_flag = False
                        self.frame_end_flag = True
                        if self.packet_received_callback:
                            str_arr = self.str_buff[:self.str_num + 1]
                            self.packet_received_callback(StrArrEventArgs(str_arr))
                    elif self.str_num == self.frame_length + 6 and self.str_buff[self.str_num] != "7E":
                        print("ERROR FRAME: Missing FRAME_END")
                        self.reset_frame()
                        continue

                    self.str_num += 1
                elif str_array[index] == "BB" and not self.frame_begin_flag:
                    self.str_num = 0
                    self.str_buff[self.str_num] = str_array[index]
                    self.frame_begin_flag = True
                    self.frame_end_flag = False
                    self.str_num = 1
        except Exception as e:
            print(f"Error reading from serial port: {e}")
    """
    
    def data_received(self, ser : serial.Serial):
        """Read data from the serial port and parse it."""
        while ser.is_open:
            if ser.is_open and ser.in_waiting == 0:
                time.sleep(0.01)
                continue
            bytes_to_read = ser.in_waiting
                        
            try:
                buffer = ser.read(bytes_to_read)
                str_array = [f"{byte:02X}".upper() for byte in buffer]
                
                for index in range(len(str_array)):
                    if self.frame_begin_flag:
                        self.str_buff[self.str_num] = str_array[index]

                        # Determine frame length when enough bytes are received
                        if self.str_num == 4:
                            self.frame_length = (256 * int(self.str_buff[3], 16) + int(self.str_buff[4], 16))
                            if self.frame_length > 3072:
                                self.frame_begin_flag = False
                                continue

                        # Check if the entire frame is received
                        if self.str_num == self.frame_length + 6 and self.str_buff[self.str_num] == "7E":
                            # Validate checksum
                            checksum = sum(int(self.str_buff[i], 16) for i in range(1, self.str_num - 1))
                            if checksum % 256 != int(self.str_buff[self.str_num - 1], 16):
                                print("ERROR FRAME: Checksum is not correct!")
                                self.reset_frame()
                                continue

                            # Valid frame received, trigger the callback
                            self.frame_begin_flag = False
                            self.frame_end_flag = True
                            if self.packet_received_callback:
                                str_arr = self.str_buff[:self.str_num + 1]
                                self.packet_received_callback(StrArrEventArgs(str_arr))
                            else:
                                print("No callback set for packet received.")
                        elif self.str_num == self.frame_length + 6 and self.str_buff[self.str_num] != "7E":
                            print("ERROR FRAME: Missing FRAME_END")
                            self.reset_frame()
                            continue

                        self.str_num += 1
                    elif str_array[index] == "BB" and not self.frame_begin_flag:
                        self.str_num = 0
                        self.str_buff[self.str_num] = str_array[index]
                        self.frame_begin_flag = True
                        self.frame_end_flag = False
                        self.str_num = 1
            except Exception as e:
                print(f"Error reading from serial port: {e}")

    def reset_frame(self):
        """Reset the frame parsing state."""
        self.frame_begin_flag = False
        self.frame_end_flag = True
        self.str_num = 0
        
    def send_command(self, command_hex):
        """Send a command to the RFID reader."""
        # Construct the command frame
        #frame = bytes.fromhex(ConstCode.FRAME_BEGIN_HEX + command_hex + ConstCode.FRAME_END_HEX)
        frame = bytes.fromhex(command_hex)
        self.ser.write(frame)
        print(f"Sent Command: {command_hex} | Size: {len(frame)}")
        time.sleep(0.1)

def packet_received_handler(event_args: StrArrEventArgs):
    """Handle a received packet and decode it."""
    frame = event_args.data
    print(f"Raw Packet Received: {frame}")

    # Ensure the frame starts and ends correctly
    if frame[0] != 'BB' or frame[-1] != '7E':
        print("Invalid frame format")
        return

    # Extract key parts of the frame
    msg_type = frame[1]
    cmd_code = frame[2]
    data_length = int(frame[3] + frame[4], 16)  # Convert hex length to integer
    data = frame[5:-2]  # Extract the data payload (excluding checksum and frame end)
    checksum = frame[-2]

    # Verify checksum
    calculated_checksum = Commands.calc_checksum("".join(frame[1:-2]))
    if calculated_checksum != checksum:
        print(f"Checksum mismatch! Expected {checksum}, got {calculated_checksum}")
        return
    
    if msg_type not in [ConstCode.FRAME_TYPE_ANS, ConstCode.FRAME_TYPE_INFO]:
        print(f"Invalid message type: {msg_type}")
        return
    
    if data_length != len(data):
        print(f"Data length mismatch: Expected {data_length}, got {len(data)}")
        return

    cmd_handler(cmd_code, data)

def cmd_handler(cmd_code, data):
    if cmd_code == ConstCode.CMD_INVENTORY:  # Inventory response
        decode_inventory_response(data)
    elif cmd_code == ConstCode.CMD_STOP_MULTI:  # Stop multi-read response
        print("Stopped multi-reading")
    elif cmd_code == ConstCode.CMD_SET_REGION:  # Set region response
        data = "".join(data)        
        if data == ConstCode.SUCCESS_MSG_DATA:
            print("Region set successfully")
        else:
            print("Failed to set region")
    elif cmd_code == ConstCode.CMD_GET_POWER:  # Get PA power response
        data = "".join(data)
        data = Commands.hex_to_dbm(data)
        print(f"PA Power: {data}")
    elif cmd_code == ConstCode.CMD_SET_POWER:  # Set PA power response
        data = "".join(data)        
        if data == ConstCode.SUCCESS_MSG_DATA:
            print("Power set successfully")
        else:
            print("Failed to set power")
    elif cmd_code == ConstCode.CMD_EXE_FAILED:
        print("Command execution failed")
    else:
        print(f"Unhandled command code: {cmd_code}")
        
    print("--------------------")

def decode_inventory_response(data):
    """Decode the inventory response frame."""
    global total_read_count, tags
    if len(data) < 12:
        print("Incomplete inventory response")
        return

    try:
        # Extract RSSI, EPC, and other fields from the data
        rssi = int(data[0], 16)  # RSSI (first byte)
        pc = data[1:3]  # Protocol Control (PC) bits
        epc_length = len(data[3:-2])  # Remaining bytes are EPC
        epc = "".join(data[3:-2])  # Extract the EPC
        crc = data[-2:]  # Last two bytes are CRC

        total_read_count += 1
        if epc in tags:
            tags[epc] += 1
        else:
            tags[epc] = 1

        # Print the decoded values
        print(f"Decoded Inventory Response:")
        #print(f"  RSSI: {Commands.hex_to_dbm(str(rssi))}dBm")
        print(f"  RSSI: {rssi}")
        print(f"  PC: {''.join(pc)}")
        print(f"  EPC: {epc}")
        print(f"  CRC: {''.join(crc)}")
    except Exception as e:
        print(f"Error decoding inventory response: {e}")
        
def setup(parser: ReceiveParser):
    parser.send_command(Commands.build_set_region_frame(ConstCode.REGION_CODE_EUR))
    parser.send_command(Commands.build_set_pa_power_frame(26))
    parser.send_command(Commands.build_get_pa_power_frame())
    
def main():
    # Configure the serial connection
    #port = os.getenv("SERIAL_PORT", "COM6")
    port =  "/dev/ttyUSB0" # for raspberry  pi or COM6 if windows. Check ls /dev/ttyUSB* to make sure
    ser = serial.Serial(port, baudrate=115200, timeout=1)
    
    try:
        # Create the parser and set the callback
        parser = ReceiveParser(ser=ser)
        parser.set_packet_received_callback(packet_received_handler)
        
        # Run the data received parser in a separate thread
        thread = threading.Thread(target=parser.data_received, args=(ser,))
        thread.start()
        
        # setup(parser)
        
        # Start multi-reading
        print("Starting multi-reading...")
        parser.send_command(Commands.build_read_multi_frame(10))
        
        time.sleep(1)
        
        # Stop multi-reading
        print("Stopping multi-reading...")
        parser.send_command(Commands.build_stop_read_frame())
        
        print(f"Total read count: {total_read_count}")
        print("Tags:")
        for epc, count in tags.items():
            print(f"  {epc}: {count}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()
        print("Serial port closed.")

if __name__ == "__main__":
    main()
