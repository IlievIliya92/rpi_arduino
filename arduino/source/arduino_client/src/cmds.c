/******************************** INCLUDE FILES *******************************/
#include <string.h>
#include <stdlib.h>

#include <avr/io.h>
#include <util/delay_basic.h>

#include "freeRTOS/FreeRTOS.h"
#include "freeRTOS/lib_io/serial.h"

/* serial interface include file. */
#include "generic_cmd_t.h"
#include "serial.h"

/******************************** LOCAL DEFINES *******************************/


/******************************** GLOBALDATA *******************************/

/********************************* LOCAL DATA *********************************/

/******************************* INTERFACE DATA *******************************/


/************************ LOCAL FUNCTIONS PROTOTYPES***************************/

/******************************* LOCAL FUNCTIONS ******************************/
static void cmds_sendMc(char *ck)
{
    avrSerialPrintf(ck);

    return;
}

static void cmds_sendId(char *id, cmdFieldVersion_t version)
{
    if (version == SRT)
        avrSerialPrintf("0%s", id);
    else if (version == EXTD)
        avrSerialPrintf("%s", id);

    return;
}

static void cmds_sendPayload(char *payload)
{
    avrSerialPrintf(payload);

    return;
}

static void cmds_sendTrailer(char *trl)
{
    avrSerialPrintf(trl);
    avrSerialPrintf("*\r\n");

    return;
}

/******************************* INTERFACE FUNCTIONS ******************************/
void cmds_pwmSendCmd(command_id_t id, uint8_t sid,  uint16_t data) {
    genericCmdMsg_t cmd;

    cmds_sendMc(CMD_COKIE);

    switch(id)
    {
        case START_ID:
        case STOP_ID:
            itoa(id, (char *)cmd.cmd_id, 10);
            cmds_sendId((char *)cmd.cmd_id, SRT);
            break;

        case PWM_ID:
        case DO_ID:
            itoa(id, (char *)cmd.cmd_id, 10);
            cmds_sendId((char *)cmd.cmd_id, SRT);
            itoa(sid, (char *)cmd.cmd_sessionId, 10);
            cmds_sendId((char *)cmd.cmd_sessionId, SRT);
            itoa(data, (char *)cmd.cmd_payload, 10);
            cmds_sendPayload((char *)cmd.cmd_payload);
            break;

        default:
            break;
    }

    cmds_sendTrailer(CMD_TRAILER);
}

