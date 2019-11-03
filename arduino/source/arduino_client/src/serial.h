#ifndef _SERIAL_H_
#define _SERIAL_H_

#ifdef __cplusplus
extern "C" {
#endif

/******************************** INCLUDE FILES *******************************/
#include "generic_t.h"

/*********************************** DEFINES **********************************/

/************************** INTERFACE DATA DEFINITIONS ************************/

/************************* INTERFACE FUNCTION PROTOTYPES **********************/
genericTask_t *getSerialTask(void);

#ifdef __cplusplus
}
#endif

#endif /* _SERIAL_H_ */
