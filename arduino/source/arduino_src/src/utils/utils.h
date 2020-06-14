#ifndef _UTILS_H_
#define _UTILS_H_

#ifdef __cplusplus
extern "C" {
#endif

/******************************** INCLUDE FILES *******************************/
#include <stdint.h>
#include <stdbool.h>

/*********************************** DEFINES **********************************/
#define bit_get(p,m) ((p) & (m))
#define bit_set(p,m) ((p) |= (m))
#define bit_clear(p,m) ((p) &= ~(m))
#define bit_flip(p,m) ((p) ^= (m))
#define bit_write(c,p,m) (c ? bit_set(p,m) : bit_clear(p,m))
#define BIT(x) (0x01 << (x))
#define LONGBIT(x) ((unsigned long)0x00000001 << (x))

/**************************  DATA DEFINITIONS ************************/

/************************* FUNCTION PROTOTYPES **********************/
void utils_hearBeat(void);
void utils_initAnimation(void);

int utils_atoI(uint8_t *str, int base);
void utils_dbgPrint(char *str);

#ifdef __cplusplus
}
#endif

#endif /* _UTILS_H_ */
