#ifndef _PWM_H_
#define _PWM_H_

#ifdef __cplusplus
extern "C" {
#endif

/******************************** INCLUDE FILES *******************************/
#include "generic_t.h"

/*********************************** DEFINES **********************************/

/************************** INTERFACE DATA DEFINITIONS ************************/

/************************* INTERFACE FUNCTION PROTOTYPES **********************/
genericCmdHandler_t *getPwmCmdHandler(void);

#ifdef __cplusplus
}
#endif

#endif /* _PWM_H_ */
