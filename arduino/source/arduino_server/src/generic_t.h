#ifndef _GENERIC_H_
#define _GENERIC_H_

#ifdef __cplusplus
extern "C" {
#endif



/******************************** INCLUDE FILES *******************************/
#include "freeRTOS/task.h"
#include "freeRTOS/semphr.h"

/*********************************** DEFINES **********************************/

/************************** INTERFACE DATA DEFINITIONS ************************/
typedef void (*voidVoid_t)(void);
typedef void (*voidVoidPtr_t)(void *);

/* Generic tasks structure */
typedef struct {
   voidVoid_t initTask;
   voidVoidPtr_t runTask;
   char *name;
   const configSTACK_DEPTH_TYPE stackDepth;
   UBaseType_t priority;
   void *data;
   void *args;
} genericTask_t;


#ifdef __cplusplus
}
#endif

#endif /* _GENERIC_H_ */

