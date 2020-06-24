/*
 * ip_parser.c
 *
 *  Created on: Jul 9, 2019
 *      Author: lars
 */


#include "ip_parser.h"
#include <arpa/inet.h>
#include <netinet/in.h>
#include <string.h>


void ipParser_clear(ipParser_t *ip_out)
{
  ip_out->ipv = 0;
}

bool_t ipParser_parseIpv4(const char *ip_str, ipParser_t *ip_out)
{
  struct in_addr ipv4;

  if (inet_aton(ip_str, &ipv4) != 0)
  {
    // IPv4 success
    ip_out->ipv = 4;
    ip_out->dwords[0] = ipv4.s_addr;
    strcpy(ip_out->ipStr, ip_str);
  }
  else
  {
    // Parsing failed
    ip_out->ipv = 0;
    return FALSE;
  }

  return TRUE;
}


bool_t ipParser_parseIpv6(const char *ip_str, ipParser_t *ip_out)
{
  struct in6_addr ipv6;

  if (inet_pton(AF_INET6, ip_str, &ipv6))
  {
    // IPv6 success
    ip_out->ipv = 6;

    // Naive copying of the bytes results in:
    //    memcpy(&(ip_out->dwords[0]), &ipv6, 16);
    //  fe80:0000:0000:691f:aa9e:a74c:427f   ->
    //  a74c:427f:691f:aa9e:0000:fe80:0000
    strcpy(ip_out->ipStr, ip_str);

    // Deal with this by reordering it in the 16 bit domain
    uint16_t *src = (uint16_t *) &ipv6;
    uint16_t *dst = (uint16_t *) &(ip_out->dwords[0]);

    dst[0] = src[6];
    dst[1] = src[7];
    dst[2] = src[4];
    dst[3] = src[5];
    dst[4] = src[2];
    dst[5] = src[3];
    dst[6] = src[0];
    dst[7] = src[1];
  }
  else
  {
    // Parsing failed
    ip_out->ipv = 0;
    return FALSE;
  }

  return TRUE;
}

bool_t ipParser_parse(const char *ip_str, ipParser_t *ip_out)
{
  if (ipParser_parseIpv4(ip_str, ip_out))
  {
    // IPv4 success
  }
  else if (ipParser_parseIpv6(ip_str, ip_out))
  {
    // IPv6 success
  }
  else
  {
    // Parsing failed
    return FALSE;
  }

  return TRUE;
}

bool_t ipParser_isIpv6(const ipParser_t *ip)
{
  return (ip->ipv == 6);
}

bool_t ipParser_isIpv4(const ipParser_t *ip)
{
  return (ip->ipv == 4);
}

uint32_t ipParser_getDword(const ipParser_t *ip, int dword_no)
{
  if ((ip->ipv == 4) && (dword_no < 1))
  {
    return ip->dwords[dword_no];
  }
  else if ((ip->ipv == 6) && (dword_no < 4))
  {
    return ip->dwords[dword_no];
  }

  return 0;
}

