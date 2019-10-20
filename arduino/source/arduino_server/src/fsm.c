/******************************** INCLUDE FILES *******************************/
#include <string.h>

#include <avr/io.h>
#include <util/delay_basic.h>

#include "freeRTOS/FreeRTOS.h"
#include "freeRTOS/semphr.h"
#include "freeRTOS/queue.h"

/* serial interface include file. */
#include "freeRTOS/lib_io/serial.h"
#include "freeRTOS/lib_io/digitalAnalog.h"
#include "freeRTOS/lib_io/servoPWM.h"

#include "fsm.h"
#include "generic_cmd_t.h"

/******************************** LOCAL DEFINES *******************************/

/******************************** TYPEDEFS ************************************/
typedef enum {
    Idle_State,
    last_State
}eSystemState;

typedef enum {
    last_Event
} eSystemEvent;

typedef eSystemState (*pfEventHandler)(void);

typedef struct
{
    eSystemState eStateMachine;
    eSystemEvent eStateMachineEvent;
    pfEventHandler pfStateMachineEvnentHandler;
} sStateMachine;

/******************************** GLOBALDATA *******************************/
extern xComPortHandle xSerialPort;

/********************************* LOCAL DATA *********************************/
static eSystemState eNextState;
static eSystemEvent eNewEvent;

/******************************* INTERFACE DATA *******************************/

/************************ LOCAL FUNCTIONS PROTOTYPES***************************/

/******************************* LOCAL FUNCTIONS ******************************/
sStateMachine asStateMachine [] = {
    {}
};

static eSystemEvent fsm_readEvent(genericCmdMsg_t *cmd)
{
//    xSerialPrint(cmd);
//    xSerialPrint((uint8_t *)"\r\n");

    return Idle_State;
}

static void fsm_Init(void)
{
    eNextState = Idle_State;

    return;
}

static void fsm_Task(void *pvParameters)
{
    (void) pvParameters;

    extern QueueHandle_t xCmdQueue;
    genericCmdMsg_t cmdMsg;

    while(1)
    {
        xQueueReceive(xCmdQueue, &cmdMsg, portMAX_DELAY);

        eNewEvent = fsm_readEvent(&cmdMsg);
        if((eNextState < last_State) && (eNewEvent < last_Event)&& (asStateMachine[eNextState].eStateMachineEvent == eNewEvent) && (asStateMachine[eNextState].pfStateMachineEvnentHandler != NULL))
        {
            eNextState = (*asStateMachine[eNextState].pfStateMachineEvnentHandler)();
        }
        else
        {
            //Invalid
        }

        memset(&cmdMsg, 0x0, sizeof(genericCmdMsg_t));
    }

    return;
}





/***************************** INTERFACE FUNCTIONS ****************************/
genericTask_t fsm = {
    fsm_Init,
    fsm_Task,
    "FSMTASK",
    256,
    2,
    NULL,
    NULL
};

genericTask_t *getFsmTask(void)
{
    return &fsm;
}
