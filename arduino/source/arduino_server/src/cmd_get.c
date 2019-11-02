/******************************** INCLUDE FILES *******************************/
#include <string.h>
#include <stdbool.h>
#include <util/delay_basic.h>

#include "freeRTOS/FreeRTOS.h"
#include "freeRTOS/semphr.h"
#include "freeRTOS/queue.h"

/* serial interface include file. */
#include "freeRTOS/lib_io/serial.h"
#include "freeRTOS/lib_io/digitalAnalog.h"

#include "utils/utils.h"

#include "cmd_get.h"
#include "generic_cmd_t.h"

/******************************** LOCAL DEFINES *******************************/
#define CMD_QUEUE_SIZE  5

/******************************** GLOBALDATA *******************************/
extern xComPortHandle xSerialPort;

/********************************* LOCAL DATA *********************************/
static SemaphoreHandle_t xCmdSemaphore;

/******************************* INTERFACE DATA *******************************/
QueueHandle_t xCmdQueue = NULL;

/************************ LOCAL FUNCTIONS PROTOTYPES***************************/

/******************************* LOCAL FUNCTIONS ******************************/
static void cmd_getReceiveInput(uint8_t *buff, uint8_t len)
{
    uint8_t c;
    uint8_t i = 0;

    for (;;) {
        while (!xSerialGetChar(&xSerialPort, &c))
            vTaskDelay(1);

        if (c == CMD_END) break;
        if ((c == '\b') && i) {
            --i;
            continue;
        }
        if (c >= ' ' && i < len - 1) {  /* Received chars */
            buff[i++] = c;
        }
    }

    xSerialRxFlush(&xSerialPort);
    buff[i] = 0;
}

static void cmd_getInit(void)
{
    xSerialPort = xSerialPortInitMinimal(USART0, BAUD, portSERIAL_BUFFER_TX, portSERIAL_BUFFER_RX);

    vSemaphoreCreateBinary(xCmdSemaphore);
    xCmdQueue = xQueueCreate(CMD_QUEUE_SIZE, sizeof(genericCmdMsg_t));

    return;
}

static void cmd_getStripTrailer(uint8_t *payload)
{
    uint8_t i = 0;

    for (i = 0; i != '\n'; i++) {
        if (payload[i] == '<') {
            payload[i] = '\n';
            payload[i++] = '\0';
        }
    }
    //avrSerialxPrintf(&xSerialPort, "SD :%s\r\n", payload);

    return;
}

static int cmd_getVerifyTrailer(uint8_t *payload)
{
    char *ret = strstr((const char *)payload, CMD_TRAILER);
    if (ret != NULL) {
        return OK;
    } else {
        return ERR;
    }
}


static void cmd_getToken(uint8_t *token, uint8_t *cmdBuff, int len)
{
    strncpy((char *)token, (char *)cmdBuff, len -1);
    token[len] = '\n';

    return;
}

static command_status_t cmd_getParse(genericCmdMsg_t *cmdMsg, uint8_t *cmd)
{
    command_status_t verified = ERR;
    response_id_t statusId;

    /* Get the magic cookie */
    cmd_getToken(cmdMsg->cmd_cookie, cmd, CMD_COKIE_LEN);
    cmd += CMD_COKIE_LEN - 1;

    /* Verify The Coockie */
    if (strcmp((char *)cmdMsg->cmd_cookie, CMD_COKIE) == 0) {
        verified = OK;
    } else {
        statusId = CKIE;
        verified = ERR;
    }

    /* Fill in the data for the command packet */
    if (verified == OK)
    {
        cmd_getToken(cmdMsg->cmd_id, cmd, CMD_ID_LEN);
        cmd += CMD_ID_LEN - 1;

        int cmdId = utils_atoI(cmdMsg->cmd_id, 10);
        /* Commands with session Id and payload */
        if (CHECK_PAYLOAD(cmdId, PWM_ID) ||
            CHECK_PAYLOAD(cmdId, DO_ID) ||
            CHECK_PAYLOAD(cmdId, CMD3_ID))
        {
            cmd_getToken(cmdMsg->cmd_sessionId, cmd, CMD_SESION_ID_LEN);
            cmd += CMD_SESION_ID_LEN - 1;
            cmd_getToken(cmdMsg->cmd_payload, cmd, CMD_PAYLOAD_LEN);
            cmd += CMD_PAYLOAD_LEN - 1;
            verified = cmd_getVerifyTrailer(cmdMsg->cmd_payload);
            if (verified == OK) {
                cmd_getStripTrailer(cmdMsg->cmd_payload);
            } else {
                 statusId = TLR;
            }
        }
        else
        {
            cmd_getToken(cmdMsg->cmd_trailer, cmd, CMD_TRAILER_LEN);
            verified = cmd_getVerifyTrailer(cmdMsg->cmd_trailer);
            if (verified == ERR) {
                statusId = TLR;
            }
        }
    }

    /* If the command is invalid return the response */
    if (verified == ERR)
        cmd_sendResponse(statusId, ERR);

    return verified;
}

static void cmd_getCmd(void)
{
    if( xCmdSemaphore != NULL )
    {
        uint8_t cmd_buff[CMD_SIZE];

        genericCmdMsg_t cmdMsg;
        memset(&cmdMsg, 0x0, sizeof(genericCmdMsg_t));

        if( xSemaphoreTake(xCmdSemaphore, (TickType_t)10) == pdTRUE)
        {
            cmd_getReceiveInput(cmd_buff, CMD_SIZE);
            if(cmd_getParse(&cmdMsg, cmd_buff) == OK)
            {
                /* Send command */
                xQueueSend(xCmdQueue, &cmdMsg, portMAX_DELAY);
            }

            xSemaphoreGive(xCmdSemaphore);
        }
    }

    return;
}

static void cmd_getTask(void *pvParameters)
{
    (void) pvParameters;
    TickType_t xLastWakeTime;

    xLastWakeTime = xTaskGetTickCount();

    while(1)
    {
        cmd_getCmd();
        vTaskDelayUntil( &xLastWakeTime, (30 / portTICK_PERIOD_MS));
    }

    return;
}

/***************************** INTERFACE FUNCTIONS ****************************/
genericTask_t cmd = {
    cmd_getInit,
    cmd_getTask,
    "CMDTASK",
    256,
    1,
    NULL,
    NULL
};

genericTask_t *getCmdGetTask(void)
{
    return &cmd;
}
