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
    NULL
};

/***************************** INTERFACE FUNCTIONS ****************************/
genericTask_t *getSchedulerTask(void)
{
    return &scheduler;
}


void rtos_start(genericTask_t *tasks[])
{
    taskId_t taskId = 0;

    for (taskId = 0; taskId < TASKS; taskId++) {
        tasks[taskId]->initTask();

        /* No need to run createTask to start the scheduler */
        if (taskId != SCHEDULER)
            rtos_createTask(tasks[taskId]);
    }

    return;
}
