/******************************** INCLUDE FILES *******************************/

#include <stdlib.h>
#include <stdio.h>
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
    (command_resp_t *)"DOD",
    (command_resp_t *)"ADC",
    (command_resp_t *)"INVD",
    (command_resp_t *)"Stp",
};


/******************************* INTERFACE DATA *******************************/

/******************************* LOCAL FUNCTIONS ******************************/

/***************************** GLOBAL FUNCTIONS ****************************/
void cmd_sendResponse(response_id_t id, int status, char *value)
{
    switch(id)
    {
        case RDY:
            (status == OK) ? avrSerialxPrintf(&xSerialPort, "{\"Ok\":\"%s\", \"ID\":\"%d\"}\r\n", responses[id], DEVICE_ID) :
                             avrSerialxPrintf(&xSerialPort, "{\"Err\":\"%s\"}\r\n", responses[id]);
            break;

        case CKIE:
        case  TLR:
        case  PWM:
        case   DO:
        case  END:
        case INVD:
            (status == OK) ? avrSerialxPrintf(&xSerialPort, "{\"Ok\":\"%s\"}\r\n", responses[id]) :
                             avrSerialxPrintf(&xSerialPort, "{\"Err\":\"%s\"}\r\n", responses[id]);
            break;

        case DODAT:
        case ADCC:
            (status == OK) ? avrSerialxPrintf(&xSerialPort, "{\"Ok\":\"%s\",\"value\":%s}\r\n", responses[id], value) :
                             avrSerialxPrintf(&xSerialPort, "{\"Err\":\"%s\"}\r\n", responses[id]);
            break;

        default:
            break;
    }

    return;
}
