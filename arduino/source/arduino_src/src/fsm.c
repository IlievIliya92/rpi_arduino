/******************************** INCLUDE FILES *******************************/
#include <string.h>
#include <stdio.h>

#include <avr/io.h>
#include <util/delay_basic.h>

#include "freeRTOS/FreeRTOS.h"
#include "freeRTOS/semphr.h"
#include "freeRTOS/queue.h"

/* serial interface include file. */
#include "freeRTOS/lib_io/digitalAnalog.h"
#include "freeRTOS/lib_io/servoPWM.h"

#include "fsm.h"
#include "pwm.h"
#include "adc.h"
#include "dio.h"
#include "generic_cmd_t.h"
#include "utils/utils.h"

/******************************** LOCAL DEFINES *******************************/

/******************************** TYPEDEFS ************************************/
typedef enum {
    Idle_State,
    Start_State,
    Pwm_State,
    Do_State,
    Adc_State,
    Stop_State,
    last_State
}eSystemState;

typedef enum {
    start_Event,
    pwm_Event,
    do_Event,
    adc_Event,
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

typedef eSystemState (*const afEventHandler[last_State][last_Event])(void *args);

/******************************** GLOBALDATA *******************************/

/********************************* LOCAL DATA *********************************/
static eSystemState eNextState;
static eSystemState ePreviousState;

static genericCmdHandler_t *cmds[COMMAND_HANDLERS];
/******************************* INTERFACE DATA *******************************/

/************************ LOCAL FUNCTIONS PROTOTYPES***************************/
static eSystemState start_handler(void *args);
static eSystemState pwm_handler(void *args);
static eSystemState do_handler(void *args);
static eSystemState adc_handler(void *args);
static eSystemState stop_handler(void *args);

/******************************* LOCAL FUNCTIONS ******************************/
static afEventHandler StateMachine = {
    [Idle_State] = {
                    [start_Event] = start_handler,
                    [invalid_Event] = NULL
                    },

    [Start_State] = {
                    [pwm_Event] = pwm_handler,
                    [do_Event] = do_handler,
                    [adc_Event] = adc_handler,
                    [stop_Event] = stop_handler,
                    [invalid_Event] = NULL
                    },

    [Pwm_State] = {
                   [pwm_Event] = pwm_handler,
                   [do_Event] = do_handler,
                   [adc_Event] = adc_handler,
                   [stop_Event] = stop_handler,
                   [invalid_Event] = NULL
                   },

    [Do_State] = {
                   [pwm_Event] = pwm_handler,
                   [do_Event] = do_handler,
                   [adc_Event] = adc_handler,
                   [stop_Event] = stop_handler,
                   [invalid_Event] = NULL
                   },

    [Adc_State] = {
                   [pwm_Event] = pwm_handler,
                   [do_Event] = do_handler,
                   [adc_Event] = adc_handler,
                   [stop_Event] = stop_handler,
                   [invalid_Event] = NULL
                   },
};

static eSystemState start_handler(void *args)
{
    PORTB |= _BV(PORTB5);
    cmd_sendResponse(RDY, OK);

    return Start_State;
}

static eSystemState pwm_handler(void *args)
{
    genericCmdMsg_t *cmdMsg = (genericCmdMsg_t *)args;

    if (cmds[0]->processData(cmdMsg->cmd_sessionId, cmdMsg->cmd_payload) == 0) {
        cmd_sendResponse(PWM, OK);
    } else {
        cmd_sendResponse(INVD, ERR);
    }

    return Pwm_State;
}

static eSystemState do_handler(void *args)
{
    genericCmdMsg_t *cmdMsg = (genericCmdMsg_t *)args;

    if (cmds[1]->processData(cmdMsg->cmd_sessionId, cmdMsg->cmd_payload) == 0) {
        cmd_sendResponse(DO, OK);
    } else {
        cmd_sendResponse(INVD, ERR);
    }

    return Do_State;
}

static eSystemState adc_handler(void *args)
{
    xADCArray adcValues;
    char values[100];

    cmds[2]->getData(&adcValues);

    sprintf(values, "{\"c0\":%d,\"c1\":%d,\"c2\":%d,\"c3\":%d,\"c4\":%d}",
                    adcValues.adc0, adcValues.adc1, adcValues.adc2, adcValues.adc3, adcValues.adc4);
    cmd_sendData(ADCC, OK, values);

    return Adc_State;
}

static eSystemState stop_handler(void *args)
{
    PORTB &= ~_BV(PORTB5);
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
        case DO_ID:
            event = do_Event;
            break;
        case ADCC_ID:
            event = adc_Event;
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
    int i = 0;

    /* Initialize L diode as output */
    DDRB |= _BV(DDB5);

    eNextState = Idle_State;
    ePreviousState = eNextState;

    /* Initialize the command handlers */
    cmds[0] = getPwmCmdHandler();
    cmds[1] = getDioCmdHandler();
    cmds[2] = getAdcCmdHandler();

    for (i = 0; i < COMMAND_HANDLERS; i++)
        cmds[i]->initCmd();

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
            eNextState = (*StateMachine[eNextState][eNewEvent])(&cmdMsg);
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
