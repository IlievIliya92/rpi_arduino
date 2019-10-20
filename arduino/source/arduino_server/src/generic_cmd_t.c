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
    (command_resp_t *)"Ckie!",
    (command_resp_t *)"Trl!"
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


