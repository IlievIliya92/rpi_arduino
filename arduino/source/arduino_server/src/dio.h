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
void dioInit(void);
int dioprocessData(uint8_t *sesionId, uint8_t *dataStr);

#ifdef __cplusplus
}
#endif

#endif /* _DIO_H_ */
