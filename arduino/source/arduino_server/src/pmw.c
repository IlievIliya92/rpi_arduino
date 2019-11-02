/******************************** INCLUDE FILES *******************************/
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#include <avr/io.h>
#include <util/delay_basic.h>

#include "freeRTOS/FreeRTOS.h"
#include "freeRTOS/semphr.h"
#include "freeRTOS/queue.h"

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
void pwmSetValues(uint16_t pwA, uint16_t pwB)
{
    if (pwA < MIN_PULSE_WIDTH) {
        pwA = MIN_PULSE_WIDTH;
    } else if (pwA > MAX_PULSE_WIDTH) {
        pwA = MAX_PULSE_WIDTH;
    }

    if (pwB < MIN_PULSE_WIDTH) {
        pwB = MIN_PULSE_WIDTH;
    } else if (pwB > MAX_PULSE_WIDTH) {
        pwB = MAX_PULSE_WIDTH;
    }

    set_PWM_hardware(pwA, pwB);

    return;
}
/***************************** INTERFACE FUNCTIONS ****************************/
void pwmInit(void)
{
    start_PWM_hardware();

    return;
}


int pwmProcessData(uint8_t *dataStr)
{
    if (dataStr == NULL)
        return -1;
    char *token;
    uint16_t pw[2];

    /* get the first token */
    token = strtok((char *)dataStr, PWM_DATA_TOK);
    pw[0] = atoi(token);

    token = strtok(NULL, PWM_DATA_TOK);
    pw[1] = atoi(token);

    pwmSetValues(pw[0], pw[1]);

    return 0;
}
