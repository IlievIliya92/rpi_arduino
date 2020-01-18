/******************************** INCLUDE FILES *******************************/

#include <stdlib.h>
#include <string.h>

#include "freeRTOS/lib_io/serial.h"

#include "freeRTOS/portable.h"

#include "generic_cmd_t.h"

extern xComPortHandle xSerialPort;

/******************************** LOCAL DEFINES *******************************/
typedef const uint8_t command_resp_t;

/******************************** GLOBALDATA *******************************/

/********************************* LOCAL DATA *********************************/

static command_resp_t *responses[RESPONSES] = {
    (command_resp_t *)"Rdy",
    (command_resp_t *)"!C",
    (command_resp_t *)"!T",
    (command_resp_t *)"PWM",
    (command_resp_t *)"DO",
    (command_resp_t *)"ADC",
    (command_resp_t *)"INVD",
    (command_resp_t *)"Stp",
};


/******************************* INTERFACE DATA *******************************/

/******************************* LOCAL FUNCTIONS ******************************/

/***************************** GLOBAL FUNCTIONS ****************************/
void cmd_sendResponse(response_id_t id, int status)
{
    if (status == ERR) {
        avrSerialxPrintf(&xSerialPort, "{\"Err\":\"%s\"}\r\n", responses[id]);
    } else if (status == OK) {
        avrSerialxPrintf(&xSerialPort, "{\"Ok\":\"%s\"}\r\n", responses[id]);
    }

    return;
}

void cmd_sendData(response_id_t id, int status, char *value)
{
    if (status == ERR) {
        avrSerialxPrintf(&xSerialPort, "{\"Err\":\"%s\"}\r\n", responses[id]);
    } else if (status == OK) {
        avrSerialxPrintf(&xSerialPort, "{\"Ok\":\"%s\",\"value\":%s}\r\n", responses[id], value);
    }

    return;
}

