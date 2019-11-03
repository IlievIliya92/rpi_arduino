/******************************** INCLUDE FILES *******************************/
#include <string.h>
#include <stdlib.h>

#include <avr/io.h>
#include <util/delay_basic.h>

#include "freeRTOS/FreeRTOS.h"
#include "freeRTOS/semphr.h"
#include "freeRTOS/queue.h"

/* serial interface include file. */
#include "freeRTOS/lib_io/serial.h"
#include "freeRTOS/lib_io/digitalAnalog.h"

#include "freeRTOS/lib_io/servoPWM.h"

#include "generic_cmd_t.h"
#include "serial.h"
#include "cmds.h"

/******************************** LOCAL DEFINES *******************************/


/******************************** GLOBALDATA *******************************/

/********************************* LOCAL DATA *********************************/

/******************************* INTERFACE DATA *******************************/


/************************ LOCAL FUNCTIONS PROTOTYPES***************************/

/******************************* LOCAL FUNCTIONS ******************************/
static void serial_Init(void)
{
    /* Set as output */
    DDRB |= _BV(DDB5);

    return;
}

static void printAdcResults(xADCArray *adcValues)
{
    avrSerialPrintf("\r\n%u, %u\r\n", adcValues->adc0, adcValues->adc1);

    return;
}


static void serial_Task(void *pvParameters)
{
    (void) pvParameters;
    TickType_t xLastWakeTime;

    extern QueueHandle_t xAdcQueue;
    xADCArray adcValues;

    const TickType_t xBlockTime = pdMS_TO_TICKS(200);

    xLastWakeTime = xTaskGetTickCount();

    while(1)
    {
        xQueueReceive( xAdcQueue, &adcValues, xBlockTime);
        PORTB |=  _BV(PORTB5);

        cmds_pwmSendCmd(START_ID, 0, 0);

        cmds_pwmSendCmd(PWM_ID, PWMCH0, adcValues.adc0);
        cmds_pwmSendCmd(PWM_ID, PWMCH1, adcValues.adc1);

        cmds_pwmSendCmd(STOP_ID, 0, 0);

        vTaskDelayUntil( &xLastWakeTime, (10 / portTICK_PERIOD_MS));
        PORTB &= ~_BV(PORTB5);
        vTaskDelayUntil( &xLastWakeTime, (40 / portTICK_PERIOD_MS));
    }

    return;
}

/***************************** INTERFACE FUNCTIONS ****************************/
genericTask_t serial = {
    serial_Init,
    serial_Task,
    "Serial",
    256,
    3,
    NULL,
    NULL
};

genericTask_t *getSerialTask(void)
{
    return &serial;
}
