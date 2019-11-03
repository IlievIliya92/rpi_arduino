#ifndef _EMG_GENERIC_H_
#define _EMG_GENERIC_H_

#ifdef __cplusplus
extern "C" {
#endif



/******************************** INCLUDE FILES *******************************/
#include "freeRTOS/task.h"
#include "freeRTOS/semphr.h"

/*********************************** DEFINES **********************************/

/************************** INTERFACE DATA DEFINITIONS ************************/
typedef void (*emg_voidVoid_t)(void);
typedef void (*emg_voidVoidPtr_t)(void *);

/* Generic tasks structure */
typedef struct {
   emg_voidVoid_t initTask;
   emg_voidVoidPtr_t runTask;
   char *name;
   const configSTACK_DEPTH_TYPE stackDepth;
   UBaseType_t priority;
   void *data;
   void *args;
} genericTask_t;


#ifdef __cplusplus
}
#endif

#endif /* _EMG_GENERIC_H_ */

