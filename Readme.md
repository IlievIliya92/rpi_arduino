# Raspberry Pi & Arduino Smart Home Automation

The project consists of smart home system based on Rasberry Pi board running
REMI application providing web access to the device and an Arduino board.
The Arduino is running a freeRTOS and is exchanging data over the serial port with the
Rasberry Pi via simple predefined protocol.

## Getting Started

Set up the project following the image below

![Boards Setup](https://github.com/IlievIliya92/rpi_arduino/blob/master/media/smartHome.png)

For test and development purpouses the project can be set up in the following maner. Running the
remi application on a host PC and having the Arduino board connected to it.

![Boards Setup Dbg](https://github.com/IlievIliya92/rpi_arduino/blob/master/media/smartHomeDbg.png)

To build and run the arduino application follow the instructions in the arduino directory Readme.md file.
To deploy the remi application follow the guide inside the pi directory.

## Built With

* [Remi](https://github.com/dddomodossola/remi) - Rasbery Pi web server & web interface
* [freeRTOS](https://www.freertos.org/) - Arduino

## Authors

* **Iliya Iliev**

## License

This project is licensed under the MIT License.
