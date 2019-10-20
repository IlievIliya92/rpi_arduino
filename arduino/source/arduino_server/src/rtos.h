#ifndef _RTOS_H_
#define _RTOS_H_

#ifdef __cplusplus
extern "C" {
#endif

/******************************** INCLUDE FILES *******************************/
#include "generic_t.h"

/*********************************** DEFINES **********************************/
#define TASKS   2

/************************** INTERFACE DATA DEFINITIONS ************************/

/************************* INTERFACE FUNCTION PROTOTYPES **********************/
void rtos_start(genericTask_t *task[]);

#ifdef __cplusplus
}
#endif

#endif /* _RTOS_H_ */
