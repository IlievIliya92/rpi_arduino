/******************************** INCLUDE FILES *******************************/
/* I/O include files */
#include "freeRTOS/lib_io/serial.h"

#include "fsm.h"
#include "cmd_get.h"

#include "rtos.h"
#include "generic_t.h"

#include "freeRTOS/lib_io/digitalAnalog.h"

/******************************** LOCAL DEFINES *******************************/

/******************************** GLOBALDATA *******************************/
extern xComPortHandle xSerialPort;

/********************************* LOCAL DATA *********************************/

/******************************* LOCAL FUNCTIONS ******************************/

/***************************** MAIN  ****************************/
int main(void) __attribute__((OS_main));
int main(void)
{
    /* Tasks array */
    genericTask_t *rtosTasks[TASKS];

    rtosTasks[0] = getCmdGetTask();
    rtosTasks[1] = getFsmTask();

    /* Starts all the tasks from Tasks array & starts the scheduler */
    rtos_start(rtosTasks);

    avrSerialxPrint_P(&xSerialPort, PSTR("\r\n\n Failed to the emg application!\r\n"));
}

