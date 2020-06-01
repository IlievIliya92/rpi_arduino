#ifndef _RTOS_H_
#define _RTOS_H_

#ifdef __cplusplus
extern "C" {
#endif

/******************************** INCLUDE FILES *******************************/
#include "generic_t.h"

/*********************************** DEFINES **********************************/
typedef enum tasks_t
{
    GETCMD = 0,
    FSM,
    SCHEDULER,
    TASKS
} tasks_t;

/************************** INTERFACE DATA DEFINITIONS ************************/

/************************* INTERFACE FUNCTION PROTOTYPES **********************/
genericTask_t *getSchedulerTask(void);

void rtos_start(genericTask_t *task[]);

#ifdef __cplusplus
}
#endif

#endif /* _RTOS_H_ */
