/******************************** INCLUDE FILES *******************************/
#include <stdlib.h>
#include <avr/io.h>
#include <util/delay_basic.h>

#include "utils.h"
#include "../freeRTOS/lib_io/serial.h"
#include "../generic_cmd_t.h"

/******************************** LOCAL DEFINES *******************************/
#define HEART_STATE_ITERATIONS 50

#define ANIMATION_SPEED        0.1
#define ANIMATION_CYCLES       50

/******************************** GLOBALDATA *******************************/
extern xComPortHandle xSerialPort;

/********************************* LOCAL DATA *********************************/

/******************************* INTERFACE DATA *******************************/

/******************************* LOCAL FUNCTIONS ******************************/

/***************************** GLOBAL FUNCTIONS ****************************/
int utils_atoI(uint8_t *str, int base)
{
    return strtol((const char *)str, NULL, base);
}

/* Init animation */
void utils_initAnimation(void)
{
    dioStates_t animationState = ON;
    int animation = 0;

    while(animation < ANIMATION_CYCLES) {
        animation++;
        animationState == ON ? (animationState = OFF) : (animationState = ON);
        animationState == ON ? PORTB |=  _BV(PORTB5) : (PORTB &= ~_BV(PORTB5));
        _delay_loop_2(ANIMATION_SPEED);
    }

    return;
}


/* This function should be called within the IDLE hook */
/* not to worry about concurency issues for the led control
   since this will work in the IDLE taks */
void utils_hearBeat(void)
{
    static dioStates_t hearState = ON;
    static int hearStateTime = 0;

    hearStateTime = (hearStateTime + 1) % HEART_STATE_ITERATIONS;

    if (hearStateTime == 0) {
        hearState == ON ? (hearState = OFF) : (hearState = ON);
        hearState == ON ? PORTB |=  _BV(PORTB5) : (PORTB &= ~_BV(PORTB5));
    }

    return;
}

void utils_dbgPrint(char *str)
{
#ifdef DEBUG
    avrSerialxPrintf(&xSerialPort, "%s", (uint8_t *)str);
    avrSerialxPrintf(&xSerialPort, "\r\n");

#endif

    return;
}


