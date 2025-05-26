#!/bin/bash

# Function to check if the device is connected
check_device() {
    echo "Checking if YRM100* device is connected..."
    lsusb | grep -i "11ca:0212" > /dev/null
    if [ $? -eq 0 ]; then
        echo "YRM100* device detected."
    else
        echo "YRM100* device not found. Please make sure it is connected to a USB 2.0 port."
        exit 1
    fi
}

# Function to load the driver and update the device ID
update_driver() {
    echo "Loading the cp210x driver..."
    sudo modprobe cp210x
    if [ $? -ne 0 ]; then
        echo "Failed to load the cp210x driver."
        exit 1
    fi

    echo "Updating the driver with vendor and product ID..."
    echo "11ca 0212" | sudo tee /sys/bus/usb-serial/drivers/cp210x/new_id
    if [ $? -eq 0 ]; then
        echo "Driver updated successfully."
    else
        echo "Failed to update the driver."
        exit 1
    fi
}

# Main script execution
echo "Starting setup for YRM100*..."
check_device
update_driver
echo "Setup complete."
