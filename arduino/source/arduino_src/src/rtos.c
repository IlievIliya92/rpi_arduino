/******************************** INCLUDE FILES *******************************/
#include "freeRTOS/FreeRTOS.h"
#include "freeRTOS/task.h"
#include "freeRTOS/queue.h"
#include "freeRTOS/semphr.h"

#include "utils/utils.h"

#include "rtos.h"
/******************************** LOCAL DEFINES *******************************/

/******************************** GLOBALDATA *******************************/

/********************************* LOCAL DATA *********************************/

/******************************* INTERFACE DATA *******************************/

/******************************* LOCAL FUNCTIONS ******************************/
static void rtos_schedulerInit(void)
{
    utils_dbgPrint("Server Started!");
    vTaskStartScheduler();

    return;
}

static void rtos_createTask(genericTask_t *task)
{
    xTaskCreate(task->runTask, (const portCHAR *)task->name,
                task->stackDepth, task->args, task->priority, NULL );

    return;
}


static
genericTask_t scheduler = {
    rtos_schedulerInit,
    NULL,
    "SHDLRTASK",
    256,
    1,
    NULL,
    NULL
};

/***************************** INTERFACE FUNCTIONS ****************************/
genericTask_t *getSchedulerTask(void)
{
    return &scheduler;
}


void rtos_start(genericTask_t *task[])
{
    int i = 0;

    for (i = 0; i < TASKS; i++) {
        task[i]->initTask();
        rtos_createTask(task[i]);
    }

    return;
}
