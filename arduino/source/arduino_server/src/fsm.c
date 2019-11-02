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
#include "pwm.h"
#include "generic_cmd_t.h"
#include "utils/utils.h"

/******************************** LOCAL DEFINES *******************************/

/******************************** TYPEDEFS ************************************/
typedef enum {
    Idle_State,
    Start_State,
    Pwm_State,
    Cmd2_State,
    Cmd3_State,
    Stop_State,
    last_State
}eSystemState;

typedef enum {
    start_Event,
    pwm_Event,
    cmd2_Event,
    cmd3_Event,
    stop_Event,
    invalid_Event,
    last_Event
} eSystemEvent;

//typedef of function pointer
typedef eSystemState (*pfEventHandler)(void);

typedef struct sStateMachine
{
    eSystemState eStateMachine;
    eSystemEvent eStateMachineEvent;
    pfEventHandler pfStateMachineEvnentHandler;
} sStateMachine_t;

typedef eSystemState (*const afEventHandler[last_State][last_Event])(void);

/******************************** GLOBALDATA *******************************/
extern xComPortHandle xSerialPort;

/********************************* LOCAL DATA *********************************/
static eSystemState eNextState;
static eSystemState ePreviousState;

/******************************* INTERFACE DATA *******************************/

/************************ LOCAL FUNCTIONS PROTOTYPES***************************/
static eSystemState start_handler(void);
static eSystemState pwm_handler(void);
static eSystemState cmd2_handler(void);
static eSystemState cmd3_handler(void);
static eSystemState stop_handler(void);

/******************************* LOCAL FUNCTIONS ******************************/
static afEventHandler StateMachine = {
    [Idle_State] = {
                    [start_Event] = start_handler,
                    [invalid_Event] = NULL
                    },

    [Start_State] = {
                    [pwm_Event] = pwm_handler,
                    [cmd2_Event] = cmd2_handler,
                    [cmd3_Event] = cmd3_handler,
                    [stop_Event] = stop_handler,
                    [invalid_Event] = NULL
                    },

    [Pwm_State] = {
                   [pwm_Event] = pwm_handler,
                   [stop_Event] = stop_handler,
                   [invalid_Event] = NULL
                   },

    [Cmd2_State] = {
                   [cmd2_Event] = cmd2_handler,
                   [stop_Event] = stop_handler,
                   [invalid_Event] = NULL
                   },

    [Cmd3_State] = {
                   [cmd3_Event] = cmd3_handler,
                   [stop_Event] = stop_handler,
                   [invalid_Event] = NULL
                   },
};

static eSystemState start_handler(void)
{
    cmd_sendResponse(RDY, OK);

    return Start_State;
}

static eSystemState pwm_handler(void)
{
    #if 0
    if (pwmProcessData() == 0) {
        cmd_sendResponse(PWM, OK);
    } else {
        cmd_sendResponse(INVD, ERR);
    }
#endif

    return Pwm_State;
}

static eSystemState cmd2_handler(void)
{
    cmd_sendResponse(CMD2, OK);

    return Cmd2_State;
}

static eSystemState cmd3_handler(void)
{
    cmd_sendResponse(CMD3, OK);

    return Cmd3_State;
}

static eSystemState stop_handler(void)
{
    cmd_sendResponse(END, OK);

    return Idle_State;
}

static eSystemEvent fsm_readEvent(uint8_t *cmd)
{
    uint8_t cmdId = utils_atoI(cmd, 10);
    eSystemEvent event = invalid_Event;

    switch(cmdId) {
        case START_ID:
            event = start_Event;
            break;
        case STOP_ID:
            event = stop_Event;
            break;
        case PWM_ID:
            event = pwm_Event;
            break;
        case CMD2_ID:
            event = cmd2_Event;
            break;
        case CMD3_ID:
            event = cmd3_Event;
            break;

        default:
            /* You should be here */
            event = invalid_Event;
            break;
    }

    return event;
}

static void fsm_Init(void)
{
    eNextState = Idle_State;
    ePreviousState = eNextState;

    pwmInit();

    return;
}

static void fsm_Task(void *pvParameters)
{
    (void) pvParameters;

    extern QueueHandle_t xCmdQueue;
    genericCmdMsg_t cmdMsg;
    memset(&cmdMsg, 0x0, sizeof(genericCmdMsg_t));

    while(1)
    {
        xQueueReceive(xCmdQueue, &cmdMsg, portMAX_DELAY);
        utils_dbgPrint("Fsm_Task");

        eSystemEvent eNewEvent = fsm_readEvent(cmdMsg.cmd_id);

        ePreviousState = eNextState;
        if((eNextState < last_State) && (eNewEvent < last_Event) && StateMachine[eNextState][eNewEvent] != NULL)
        {
            eNextState = (*StateMachine[eNextState][eNewEvent])();
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
