/******************************** INCLUDE FILES *******************************/
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <linux/ip.h>
#include <linux/if_packet.h>
#include <netinet/ether.h>
#include <ctype.h>

#include "network.h"

/******************************** LOCAL DEFINES *******************************/

/******************************* LOCAL TYPEDEFS ******************************/

/********************************* LOCAL DATA *********************************/

/********************************* LOCAL FUNCTIONS *********************************/
static
bool_t network_isValidMacAddress(const char* macStr)
{
    if (macStr == NULL)
        return FALSE;

    int i = 0;
    int s = 0;

    while (*macStr) {
       if (isxdigit(*macStr)) {
          i++;
       } else if (*macStr == ':' || *macStr == '-') {
          if (i == 0 || i / 2 - 1 != s)
            break;
          ++s;
       } else {
           s = -1;
       }
       ++macStr;
    }

    return (i == 12 && (s == 5 || s == 0));
}


/********************************* INTERFACE FUNCTIONS *********************************/
bool_t network_getIface(const char *ifNameStr, char *ifName)
{
    bool_t ret = FALSE;

    if (ifNameStr != NULL) {
        strcpy(ifName, ifNameStr);
        ret = TRUE;
    } else {
        fprintf(stderr, "\n[%s] Failed to obtain host interface name!\n", __func__);
    }

    return ret;
}

bool_t network_getMacAddr(const char *macStr, __u8 *destMac)
{
    bool_t ret = FALSE;

    if (network_isValidMacAddress(macStr)) {
        sscanf(macStr, "%hhx:%hhx:%hhx:%hhx:%hhx:%hhx",
                        &destMac[0], &destMac[1], &destMac[2], &destMac[3], &destMac[4], &destMac[5]);
        ret = TRUE;
    } else {
        fprintf(stderr, "\n[%s] Failed to obtain the destination Mac address!\n", __func__);
    }

    return ret;
}

bool_t network_getIpAddr(const char *ipStr, ipParser_t *ip)
{
    bool_t ret = FALSE;

    ipParser_clear(ip);
    ret = ipParser_parse(ipStr, ip);
    if (ret) {
        ret = TRUE;
    } else {
        fprintf(stderr, "\n[%s] Failed to obtain ip address!\n", __func__);
    }

    return ret;
}
