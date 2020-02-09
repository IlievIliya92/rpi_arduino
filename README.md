# Raspberry Pi & Arduino Smart Home Automation

The project consists of smart home system based on Rasberry Pi board running
REMI application providing web access to the device and an Arduino board.
The Arduino is running a freeRTOS and is exchanging data over the serial port with the
Rasberry Pi via simple predefined protocol.

## Getting Started

Clone the repository

git clone https://github.com/IlievIliya92/rpi_arduino.git

Set up the project following the image below

![Boards Setup](https://github.com/IlievIliya92/rpi_arduino/blob/master/media/smartHome.png)

For test and development purpouses the project can be set up in the following maner. Running the
remi application on a host PC and having the Arduino board connected to it.

![Boards Setup Dbg](https://github.com/IlievIliya92/rpi_arduino/blob/master/media/smartHomeDbg.png)

To build and run the Arduino application follow the instructions in the  Readme.md file insed the arduino directory.
To deploy the remi application follow the guide inside the pi directory.

## Web Interface

Once you have setup the project and the webserver has been started the web interface should
be accesible from a link like this: [ip_address_of_the_server_running_the_app]:8081

You should be able to see the following main page:

![Boards Setup Dbg](https://github.com/IlievIliya92/rpi_arduino/blob/master/media/disconnected.png)

Click the connect button in the lower left corner.
If everything is set up properly the status under the connect button should be
device authenticated.

![Boards Setup Dbg](https://github.com/IlievIliya92/rpi_arduino/blob/master/media/connected.png)

## Built With

* [Remi](https://github.com/dddomodossola/remi) - Rasbery Pi web server & web interface
* [freeRTOS](https://www.freertos.org/) - Arduino

## Authors

* **Iliya Iliev**

## License

This project is licensed under the MIT License. - see the [LICENSE.md](LICENSE.md) file for details
