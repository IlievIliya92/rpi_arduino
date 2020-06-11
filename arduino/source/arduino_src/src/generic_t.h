#ifndef _GENERIC_H_
#define _GENERIC_H_

#ifdef __cplusplus
extern "C" {
#endif



/******************************** INCLUDE FILES *******************************/
#include "freeRTOS/task.h"
#include "freeRTOS/semphr.h"

/*********************************** DEFINES **********************************/
typedef enum {
    C_PWM = 0,
    C_DIO,
    C_ADC,
    COMMAND_HANDLERS
} cmd_hndlrs_t;

/************************** INTERFACE DATA DEFINITIONS ************************/
typedef void (*voidVoid_t)(void);
typedef void (*voidVoidPtr_t)(void *);
typedef int (*voidVoid2Uint8_t)(uint8_t *, uint8_t *);
typedef void (*voidVoid)(void *);

/* Generic tasks structure */
typedef struct {
   voidVoid_t initTask;
   voidVoidPtr_t runTask;
   char *name;
   const configSTACK_DEPTH_TYPE stackDepth;
   UBaseType_t priority;
   void *args;
} genericTask_t;

typedef struct {
   voidVoid_t initCmd;
   voidVoid2Uint8_t processData;
   voidVoid getData;
} genericCmdHandler_t;


#ifdef __cplusplus
}
#endif

#endif /* _GENERIC_H_ */

