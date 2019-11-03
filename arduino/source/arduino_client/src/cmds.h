#ifndef _CMDS_H_
#define _CMDS_H_

#ifdef __cplusplus
extern "C" {
#endif

/******************************** INCLUDE FILES *******************************/
#include "generic_t.h"

/*********************************** DEFINES **********************************/

/************************** INTERFACE DATA DEFINITIONS ************************/

/************************* INTERFACE FUNCTION PROTOTYPES **********************/
void cmds_pwmSendCmd(command_id_t id, uint8_t sid, uint16_t data);

#ifdef __cplusplus
}
#endif

#endif /* _CMDS_H_ */
