# YRM100\* RFID Reader on Raspberry Pi

This project sets up and runs a UHF RFID reader (YRM100\*) on a Raspberry Pi using Python. It supports sending commands to the reader, receiving and parsing RFID tag data, and displaying results such as EPC, RSSI, and read counts.

---

## 📦 Project Structure

- `Reader_Cmds.py` — Defines protocol constants and builds command frames.
- `YMR100.py` — Main script. Handles serial communication, parses incoming data, and runs the main logic.
- `setup_yrm100.sh` — (optional) shell script to bind the correct USB driver for YRM100\*.

---

## 🚀 Getting Started

### 1. ⚙️ Hardware Setup

- Make sure the **YRM100\*** RFID reader is connected a **USB 2.0 port** on your Raspberry Pi.
- Run:
  ```
  lsusb
  ```
- You should see a line like:
    ```
    ID 11ca:0212 VeriFone Inc Verifone USB to Printer
    ```

---

### 2. 🧠 Configure the Serial Port

- Check Serial Port
- Run:
  ```
  ls /dev/ttyUSB*
  ```
You should see something like /dev/ttyUSB0 for Raspberry Pi (COM6 for windows)

In `YMR100.py`, set the correct serial port. Under main():

```
port = "/dev/ttyUSB0"
```

Alternatively, create a `.env` file:

```
SERIAL_PORT=/dev/ttyUSB0
```

---

### 3. ▶️ Run the Reader

Start the full RFID reader pipeline:

```
python3 YMR100.py
```

This will:

- Connect to the reader
- Start a background thread to listen for tag data
- Send a multi-read command
- Print each tag's EPC, RSSI, PC bits, and CRC
- Print the total read count

---

### 🧪 Example Output

```
plaintext
CopyEdit
Starting multi-reading...
Stopping multi-reading...
Decoded Inventory Response:
  RSSI: 44
  PC: 3000
  EPC: E20034120123456789000000
  CRC: 1234
Total read count: 1
Tags:
  E20034120123456789000000: 1
Serial port closed.
```

---

### 🧰 Dependencies

Install required Python packages:

```
pip install pyserial python-dotenv
```
-- 

### 📥 (Optional) Driver Setup (only if Raspberry Pi does not recognize YMR100 as a serial)

Run the included shell script to load and bind the driver:

```
chmod +x setup_yrm100.sh
./setup_yrm100.sh
```

This:

- Loads the CP210x driver
- Binds the YRM100* vendor/device ID (`11ca:0212`) to it

✅ Afterward, verify:

```bash
bash
CopyEdit
ls /dev/ttyUSB*
# You should see something like /dev/ttyUSB0
```

---
