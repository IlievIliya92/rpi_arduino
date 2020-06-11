/******************************** INCLUDE FILES *******************************/
/* I/O include files */
#include "freeRTOS/lib_io/serial.h"

#include "fsm.h"
#include "cmd_get.h"

#include "rtos.h"
#include "generic_t.h"

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

    rtosTasks[GETCMD] = getCmdGetTask();
    rtosTasks[FSM] = getFsmTask();
    rtosTasks[SCHEDULER] = getSchedulerTask();

    /* Starts all the tasks from Tasks array & starts the scheduler */
    rtos_start(rtosTasks);

    avrSerialxPrint_P(&xSerialPort, PSTR("\r\n\n Failed to start the application!\r\n"));

    return 0;
}

