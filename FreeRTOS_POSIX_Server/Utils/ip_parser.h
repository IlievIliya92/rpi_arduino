/*
 * ip_parser.h
 *
 *  Created on: Jul 9, 2019
 *      Author: lars
 */

#ifndef SRC_UTIL_IP_PARSER_H_
#define SRC_UTIL_IP_PARSER_H_

#include <stdint.h>
#include "plf.h"

typedef struct {
  int ipv; // 0 empty, 4 ipv4, 6 ipv6
  uint32_t dwords[4];
  char ipStr[50];
} ipParser_t;

void ipParser_clear(ipParser_t *ip_out);

bool_t ipParser_parse(const char *ip_str, ipParser_t *ip_out);
bool_t ipParser_parseIpv4(const char *ip_str, ipParser_t *ip_out);
bool_t ipParser_parseIpv6(const char *ip_str, ipParser_t *ip_out);

bool_t ipParser_isIpv6(const ipParser_t *ip);
bool_t ipParser_isIpv4(const ipParser_t *ip);

uint32_t ipParser_getDword(const ipParser_t *ip, int dword_no);


#endif /* SRC_UTIL_IP_PARSER_H_ */
