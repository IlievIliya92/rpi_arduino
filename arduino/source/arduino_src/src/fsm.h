#ifndef _FSM_H_
#define _FSM_H_

#ifdef __cplusplus
extern "C" {
#endif

/******************************** INCLUDE FILES *******************************/
#include "generic_t.h"

/*********************************** DEFINES **********************************/

/************************** INTERFACE DATA DEFINITIONS ************************/

/************************* INTERFACE FUNCTION PROTOTYPES **********************/
genericTask_t *getFsmTask(void);

#ifdef __cplusplus
}
#endif

#endif /* _FSM_H_ */
