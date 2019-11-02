## EMG Project

### Clone the repository

    git clone https://github.com/IlievIliya92/rpi_arduino.git

### Prerequisites

* Run the following command to install required packages:

    sudo apt install cmake gcc-avr avr-libc avrdude python-tk

### 2. Configure the project.

#### 2.1. Configure the server.
    source sconfigure

### 3. Connect the boards

#### 3.1. Connect the server board

Arduino Server Schematic
![alt text](https://github.com/IlievIliya92/rpi_arduino/blob/master/arduino/source/arduino_server/schematic/arudino_servo_douts.png
 "Arduino Server Schemtaic")

### 4. Build the project
    sbuild

### 5. Upload to the target
    supload [name_of_the_serial_device]

### Usage
Run the test script:

Go to tests directory:

    cd [root_or_the_project]/arduino/source/arduino_server/tests/

Run the test:

    python serial_test.py
