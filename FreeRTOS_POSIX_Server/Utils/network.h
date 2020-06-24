#ifndef _NETWORK_H_
#define _NETWORK_H_

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

/******************************** INCLUDE FILES *******************************/
#include "Utils/plf.h"
#include "Utils/ip_parser.h"
#include <net/if.h>
#include <netinet/ether.h>

/*********************************** DEFINES **********************************/

/************************** INTERFACE DATA DEFINITIONS ************************/

/************************* INTERFACE FUNCTION PROTOTYPES **********************/
bool_t network_getIface(const char *ifNameStr, char *ifName);
bool_t network_getMacAddr(const char *macStr, __u8 *destMac);
bool_t network_getIpAddr(const char *ipStr, ipParser_t *ip);

/** @} */

#ifdef __cplusplus
}
#endif /* _cplusplus */

#endif /* _NETWORK_H_ */

