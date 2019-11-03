/******************************** INCLUDE FILES *******************************/
/* I/O include files */
#include "freeRTOS/lib_io/serial.h"

#include "adc.h"
#include "serial.h"

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
    xSerialPort = xSerialPortInitMinimal(USART0, BAUD, portSERIAL_BUFFER_TX, portSERIAL_BUFFER_RX);

    /* Tasks array */
    genericTask_t *rtosTasks[TASKS];

    rtosTasks[0] = getAdcTask();
    rtosTasks[1] = getSerialTask();

    /* Starts all the tasks from Tasks array & starts the scheduler */
    rtos_start(rtosTasks);

    avrSerialxPrint_P(&xSerialPort, PSTR("\r\n\n Failed to start the emg application!\r\n"));
}
