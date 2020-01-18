#ifndef _DIO_H_
#define _DIO_H_

#ifdef __cplusplus
extern "C" {
#endif

/******************************** INCLUDE FILES *******************************/
#include "generic_t.h"

/*********************************** DEFINES **********************************/

/************************** INTERFACE DATA DEFINITIONS ************************/

/************************* INTERFACE FUNCTION PROTOTYPES **********************/
genericCmdHandler_t *getDioCmdHandler(void);

#ifdef __cplusplus
}
#endif

#endif /* _DIO_H_ */
