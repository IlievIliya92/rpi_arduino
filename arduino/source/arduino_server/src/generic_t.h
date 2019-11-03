#ifndef _GENERIC_H_
#define _GENERIC_H_

#ifdef __cplusplus
extern "C" {
#endif



/******************************** INCLUDE FILES *******************************/
#include "freeRTOS/task.h"
#include "freeRTOS/semphr.h"

/*********************************** DEFINES **********************************/
#define COMMAND_HANDLERS    2

/************************** INTERFACE DATA DEFINITIONS ************************/
typedef void (*voidVoid_t)(void);
typedef void (*voidVoidPtr_t)(void *);
typedef int (*voidVoid2Uint8_t)(uint8_t *, uint8_t *);

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

typedef struct {
   voidVoid_t initCmd;
    voidVoid2Uint8_t processData;
} genericCmdHandler_t;


#ifdef __cplusplus
}
#endif

#endif /* _GENERIC_H_ */

