/******************************** INCLUDE FILES *******************************/
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <ctype.h>

#include <avr/io.h>
#include <util/delay_basic.h>

#include "freeRTOS/FreeRTOS.h"

#include "dio.h"
#include "generic_cmd_t.h"

/* serial interface include file. */
#include "freeRTOS/lib_io/serial.h"

/******************************** LOCAL DEFINES *******************************/

/******************************** TYPEDEFS ************************************/

/******************************** GLOBALDATA *******************************/
extern xComPortHandle xSerialPort;

/********************************* LOCAL DATA *********************************/

/******************************* INTERFACE DATA *******************************/

/******************************* LOCAL FUNCTIONS ******************************/
static
int dioIsValidDio(dioCh_t dio)
{
    if (dio > DION)
        return -1;

    return 0;
}

static
int dioIsValidState(dioStates_t state)
{
    if (state == ON || state == OFF)
        return 0;

    return -1;
}

static
void dioSetValue(uint16_t state, uint8_t dio)
{
    switch (dio)
    {
        case DIO0:
            state == ON ? PORTB |=  _BV(PORTB0) : (PORTB &= ~_BV(PORTB0));
        break;

        case DIO1:
            state == ON ? PORTB |=  _BV(PORTB1) : (PORTB &= ~_BV(PORTB1));
        break;

        case DIO2:
            state == ON ? PORTB |=  _BV(PORTB2) : (PORTB &= ~_BV(PORTB2));
        break;

        case DIO3:
            state == ON ? PORTB |=  _BV(PORTB3) : (PORTB &= ~_BV(PORTB3));
        break;

        case DIO4:
            state == ON ? PORTB |=  _BV(PORTB4) : (PORTB &= ~_BV(PORTB4));
        break;

        default:
            break;
    }

    return;
}

static
uint8_t dioGetValue(uint8_t dio)
{
    return !!(PINB & (1 << dio));
}

static
void dioInit(void)
{
    /* Set as outputs B0 - B0 */
    DDRB |= _BV(DDB0);
    DDRB |= _BV(DDB1);
    DDRB |= _BV(DDB2);
    DDRB |= _BV(DDB3);
    DDRB |= _BV(DDB4);

    return;
}

static
int dioProcessData(uint8_t *sesionId, uint8_t *dataStr)
{
    if (dataStr == NULL || sesionId == NULL)
        return -1;

    dioCh_t dio = (dioCh_t)atoi((char *)sesionId) & 0xF;
    dioStates_t state = (dioStates_t)atoi((char *)dataStr);

    if (dioIsValidDio(dio) < 0 || dioIsValidState(state) < 0)
        return -1;

    dioSetValue(state, dio);

    return 0;
}


static
void dioGetData(void *arg)
{
    xDIOArray *dioValues = (xDIOArray *)arg;

    int i = 0;

    for (i = 0; i < DION; i++)
        dioValues->data[i] = dioGetValue(i);

    return;
}

static
genericCmdHandler_t dio = {
    dioInit,
    dioProcessData,
    dioGetData
};

/***************************** INTERFACE FUNCTIONS ****************************/
genericCmdHandler_t *getDioCmdHandler(void)
{
    return &dio;
}

