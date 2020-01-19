## Arduino board SetUp

### Build the project
    cd [PROJECT_PATH]]/pi_arduino/arduino
    source aconfigure
    acheck_requirements
    abuild

### Upload to the target
    aupload [name_of_the_serial_device]

* The name_of_the_serial_device argument is optional. The supload script will look for serial devices connected to the host pc and upload to the first found. In case you have more than one connected it is mandatory to specify the name of the serial device.

### Serial Port commands:

All of the commands follow the same basic protocol.
Header | CMID | SID / DATA / Trailer | CMD End symbol

| Field   | Value              | Size     |
|---------|--------------------|----------|
| Header  | (fixed) S>         | 2 bytes  |
| CMID    | 0x00 - 0xFF        | 2 bytes  |
| SID     | 0x00 - 0xFF        | 2 bytes  |
| DATA    | 0x0 - 0xFFFFFFFFFF | 10 bytes |
| Trailer | (fixed) <E         | 2 bytes  |
| CMD End | (fixed) *          | 1 byte   |


#### CMD ID field:

| CMD ID | Definition             |
|--------|------------------------|
| 01     | Start Command          |
| 02     | PWM                    |
| 03     | Digital I/O            |
| 04     | ADC                    |
| 05     | Stop Command           |


#### Start Command:

Required to be sent first before starting a new
transmision of data.

| Field   | Value              | Size     |
|---------|--------------------|----------|
| Header  | (fixed) S>         | 2 bytes  |
| CMID    | 0x01               | 2 bytes  |


#### PWM Command:

| Field   | Value                        | Size     |
|---------|------------------------------|----------|
| Header  | (fixed) S>                   | 2 bytes  |
| CMID    | 0x02                         | 2 bytes  |
| SID     | 0x00 - 0x01 (Channel Number) | 2 bytes  |
| DATA    | 0x0 - 0xFFFF (Duty Cycle)    | 10 bytes |
| Trailer | (fixed) <E                   | 2 bytes  |
| CMD End | (fixed) *                    | 1 byte   |

*Channels:*
0x00 - PB5 - Channel 0
0x01 - PB4 - Channel 1


#### DIO Command:

| Field   | Value                    | Size     |
|---------|--------------------------|----------|
| Header  | (fixed) S>               | 2 bytes  |
| CMID    | 0x03                     | 2 bytes  |
| SID     | 0x0 - 0x04 (Digital I/O) | 2 bytes  |
| DATA    | 0x0 - 0x1 (State)        | 10 bytes |
| Trailer | (fixed) <E               | 2 bytes  |
| CMD End | (fixed) *                | 1 byte   |

*Digital I/O:*

0x00 - PB0
0x01 - PB1
0x02 - PB2
0x03 - PB3
0x04 - PB4

*State:*
0x0 - OFF
0x1 - ON

#### Stop Command:

Required to be sent last to close the current
exchange of data.

| Field   | Value              | Size     |
|---------|--------------------|----------|
| Header  | (fixed) S>         | 2 bytes  |
| CMID    | 0x05               | 2 bytes  |


### Usage

Once uploaded the application verify that eveything is working using
the tests script inside the tests directory:

cd [PROJECT_PATH]/rpi_arduino/arduino/source/tests
python cmds_test.py

