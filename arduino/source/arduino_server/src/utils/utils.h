#ifndef _UTILS_H_
#define _UTILS_H_

#ifdef __cplusplus
extern "C" {
#endif

/******************************** INCLUDE FILES *******************************/
#include <stdint.h>
#include <stdbool.h>

/*********************************** DEFINES **********************************/

/**************************  DATA DEFINITIONS ************************/

/************************* FUNCTION PROTOTYPES **********************/
int utils_atoI(uint8_t *str, int base);
void utils_dbgPrint(char *str);

#ifdef __cplusplus
}
#endif

#endif /* _UTILS_H_ */
