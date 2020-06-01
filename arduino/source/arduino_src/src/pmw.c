/******************************** INCLUDE FILES *******************************/
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>

#include <avr/io.h>
#include <util/delay_basic.h>

#include "freeRTOS/FreeRTOS.h"
#include "freeRTOS/semphr.h"
#include "freeRTOS/queue.h"

#include "pwm.h"
#include "generic_cmd_t.h"

/* serial interface include file. */
#include "freeRTOS/lib_io/serial.h"
#include "freeRTOS/lib_io/servoPWM.h"

/******************************** LOCAL DEFINES *******************************/
#define MIN_PULSE_WIDTH       300     // the shortest pulse sent to a servo
#define MAX_PULSE_WIDTH      1180     // the longest pulse sent to a servo

#define DEFAULT_PULSE_WIDTH  300     // default pulse width when servo is attached

/******************************** TYPEDEFS ************************************/

/******************************** GLOBALDATA *******************************/
extern xComPortHandle xSerialPort;

/********************************* LOCAL DATA *********************************/

/******************************* INTERFACE DATA *******************************/

/************************ LOCAL FUNCTIONS PROTOTYPES***************************/

/******************************* LOCAL FUNCTIONS ******************************/
static
int pwmIsValidCh(uint8_t ch)
{
    if (ch > PWMCHN)
        return -1;

    return 0;
}

static
int pwmIsValidData(uint16_t data)
{
    if (data == 0)
        return -1;

    return 0;
}

static
void pwmSetValue(uint16_t pw, uint8_t ch)
{
    pw += MIN_PULSE_WIDTH;

    if (pw < MIN_PULSE_WIDTH) {
        pw = MIN_PULSE_WIDTH;
    } else if (pw > MAX_PULSE_WIDTH) {
        pw = MAX_PULSE_WIDTH;
    }

    set_PWM_hardwareChannel(pw, ch);

    return;
}

static
void pwmInit(void)
{
    start_PWM_hardware();
    set_PWM_hardware(MIN_PULSE_WIDTH, MIN_PULSE_WIDTH);

    return;
}

static
int pwmProcessData(uint8_t *sesionId, uint8_t *dataStr)
{
    if (dataStr == NULL || sesionId == NULL)
        return -1;

    uint8_t ch = atoi((char *)sesionId);
    uint16_t data = atoi((char *)dataStr);

    if (pwmIsValidCh(ch) < 0 || pwmIsValidData(data) < 0)
        return -1;

    switch(ch)
    {
        case PWMCH0:
            pwmSetValue(data, PWMCH0);
        break;

        case PWMCH1:
            pwmSetValue(data, PWMCH1);
        break;

    }

    return 0;
}

static
genericCmdHandler_t pwm = {
    pwmInit,
    pwmProcessData,
    NULL
};

/***************************** INTERFACE FUNCTIONS ****************************/
genericCmdHandler_t *getPwmCmdHandler(void)
{
    return &pwm;
}
