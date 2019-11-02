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
void pwmInit(void);
void pwmSetValues(uint16_t pwA, uint16_t pwB);

#ifdef __cplusplus
}
#endif

#endif /* _PWM_H_ */
