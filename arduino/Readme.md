## Arduino boards SetUp

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
PORTB0 - PORTB1 are setup as digital outputs controled
by the commands available for digital I/O.

Arduino Server Schematic
![alt text](https://github.com/IlievIliya92/rpi_arduino/blob/master/arduino/source/arduino_server/schematic/arudino_servo_douts.png
 "Arduino Server Schemtaic")


### 4. Build the project
    sbuild

### 5. Upload to the target
    supload [name_of_the_serial_device]

### 6. Serial Port commands:

### 6.1. Server Side:

Command format:

| Field   | Value              | Size     |
|---------|--------------------|----------|
| Header  | (fixed) S>         | 2 bytes  |
| CMID    | 0x00 - 0xFF        | 2 bytes  |
| SID     | 0x00 - 0xFF        | 2 bytes  |
| DATA    | 0x0 - 0xFFFFFFFFFF | 10 bytes |
| Trailer | (fixed) <E         | 2 bytes  |
| CMD End | (fixed) *          | 1 byte   |


CMD ID field:

| CMD ID | Definition             |
|--------|------------------------|
| 01     | Start Command          |
| 02     | PWM                    |
| 03     | Digital I/O            |
| 04     | Empty slot for new CMD |
| 05     | Stop Command           |


##### Start Command:

Required to be sent first before starting a new
transmision of data.

| Field   | Value              | Size     |
|---------|--------------------|----------|
| Header  | (fixed) S>         | 2 bytes  |
| CMID    | 0x01               | 2 bytes  |


##### PWM Command:

| Field   | Value                        | Size     |
|---------|------------------------------|----------|
| Header  | (fixed) S>                   | 2 bytes  |
| CMID    | 0x02                         | 2 bytes  |
| SID     | 0x00 - 0x01 (Channel Number) | 2 bytes  |
| DATA    | 0x0 - 0xFFFF (Duty Cycle)    | 10 bytes |
| Trailer | (fixed) <E                   | 2 bytes  |
| CMD End | (fixed) *                    | 1 byte   |

Channels:
0x00 - PB5 - Channel 0
0x01 - PB4 - Channel 1


##### DIO Command:

| Field   | Value                    | Size     |
|---------|--------------------------|----------|
| Header  | (fixed) S>               | 2 bytes  |
| CMID    | 0x03                     | 2 bytes  |
| SID     | 0x0 - 0x04 (Digital I/O) | 2 bytes  |
| DATA    | 0x0 - 0x1 (State)        | 10 bytes |
| Trailer | (fixed) <E               | 2 bytes  |
| CMD End | (fixed) *                | 1 byte   |

Digital I/O:

0x00 - PB0
0x01 - PB1
0x02 - PB2
0x03 - PB3
0x04 - PB4

State:
0x0 - OFF
0x1 - ON

##### Stop Command:

Required to be sent last to close the current
exchange of data.

| Field   | Value              | Size     |
|---------|--------------------|----------|
| Header  | (fixed) S>         | 2 bytes  |
| CMID    | 0x05               | 2 bytes  |



### Usage
Run the test script:

Go to tests directory:
    cd [root_or_the_project]/arduino/source/arduino_server/tests/

Run the test:
    python serial_test.py
