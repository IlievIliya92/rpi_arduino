#ifndef _ADC_H_
#define _ADC_H_

#ifdef __cplusplus
extern "C" {
#endif

/******************************** INCLUDE FILES *******************************/
#include "generic_t.h"

/*********************************** DEFINES **********************************/

/************************** INTERFACE DATA DEFINITIONS ************************/

/************************* INTERFACE FUNCTION PROTOTYPES **********************/
genericCmdHandler_t *getAdcCmdHandler(void);

#ifdef __cplusplus
}
#endif

#endif /* _ADC_H_ */
