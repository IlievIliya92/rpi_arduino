/******************************** INCLUDE FILES *******************************/
#include <stdlib.h>

#include "utils.h"
#include "../freeRTOS/lib_io/serial.h"

/******************************** LOCAL DEFINES *******************************/

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


void utils_dbgPrint(char *str)
{
#ifdef DEBUG
    avrSerialxPrintf(&xSerialPort, "%s", (uint8_t *)str);
    avrSerialxPrintf(&xSerialPort, "\r\n");

#endif

    return;
}


