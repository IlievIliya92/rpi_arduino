/******************************** INCLUDE FILES *******************************/
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <ifaddrs.h>
#include <net/if.h>
#include <arpa/inet.h>
#include <linux/ip.h>
#include <sys/ioctl.h>
#include <linux/in6.h>
#include <netinet/ip6.h>
#include <netinet/ether.h>



#include <stdlib.h>

#include "packet.h"

/******************************** LOCAL DEFINES *******************************/
#define IPV6_ADDR_GLOBAL        0x00U
#define IPV6_ADDR_LOOPBACK      0x10U
#define IPV6_ADDR_LINKLOCAL     0x20U
#define IPV6_ADDR_SITELOCAL     0x40U
#define IPV6_ADDR_COMPATv4      0x80U

/******************************* LOCAL TYPEDEFS ******************************/
/* Kt header description */
typedef struct ard_header
{
    __u16 version;
} ard_header_t;

/* Kt data description */
typedef struct ard_Payload
{
    __u8 *payload;
} ard_Payload_t;


typedef struct pkt {
    struct ether_header eh;
    struct iphdr iph;
    struct ard_header ardh;
    struct ard_Payload ardPayload;
 } pkt_t;


/********************************* LOCAL DATA *********************************/

/******************************* LOCAL FUNCTIONS ******************************/
static void hexDump(const unsigned char *data, unsigned int n)
{
    const unsigned char *p;

    p = data;
    while (p - data < n) {
        unsigned int i;

        for (i = 0; p - data + i < n && i < 8; i++)
            fprintf(stdout, " %02X", p[i]);
        if (p - data < n)
            fprintf(stdout, "  ");
        for (; p - data + i < n && i < 16; i++)
            fprintf(stdout, " %02X", p[i]);
        fprintf(stdout, "\n");
        p += i;
    }
}

static unsigned short csum(unsigned short *buf, int nwords)
{
    unsigned long sum = 0;

    for(sum = 0; nwords > 0; nwords--) {
        sum += *buf++;
    }
    sum = (sum >> 16) + (sum & 0xffff);
    sum += (sum >> 16);

    return (unsigned short)(~sum);
}

/******************************* GLOBAL FUNCTIONS ******************************/
    /*
     * Packet structure
     * eth header  - eth source host
     *             - eth dest host
     *             - eth type
     * ip header   - ihl - const 5 (lenght of the internet header)
     *             - version - ipv4
     *             - tos - type of service 0x00
     *             - tot_len  -total len = ipheader + ktheader + ktdata
     *             - id - identifier set to 0
     *             - ttl - time to live 64 hops
     *             - protocol - 17 - UDP
     *             - csum - checksum
     *             - src_addr
     *             - dst_addr
     * ardHeader    - session_id
     *             - version   const =  4
     *             - ident
     * ardPayload  - payload - variable len
     *
     */
int packetGenerate(int sockfd, __u8 *sendbuf, __u8 dataLen, char *ifName, __u8 *destMac, ipParser_t *dst_addr)
{
    int pktLen = 0;
    struct ifreq if_mac;

    struct pkt *pkt = NULL;
    struct ether_header *eh = NULL;
    struct iphdr *iph = NULL;
    struct ard_header *ardh = NULL;
    struct ard_Payload *ardPayload = NULL;

    pkt = (struct pkt_t *) sendbuf;

    eh = &pkt->eh;
    iph = &pkt->iph;
    ardh = &pkt->ardh;
    ardPayload = &pkt->ardPayload;

    /* Get the MAC address of the interface to send on */
    memset(&if_mac, 0, sizeof(struct ifreq));
    strncpy(if_mac.ifr_name, ifName, IFNAMSIZ-1);
    if (ioctl(sockfd, SIOCGIFHWADDR, &if_mac) < 0) {
        fprintf(stderr, "\n[%s] FSIOCGIFHWADDR\n", __func__);
        return -1;
    }

    memset(sendbuf, 0x00, SEND_BUFF_SIZE);


    /* Construct the Ethernet header */
    /* Ethernet header */
    eh->ether_shost[0] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[0];
    eh->ether_shost[1] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[1];
    eh->ether_shost[2] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[2];
    eh->ether_shost[3] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[3];
    eh->ether_shost[4] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[4];
    eh->ether_shost[5] = ((uint8_t *)&if_mac.ifr_hwaddr.sa_data)[5];

    eh->ether_dhost[0] = destMac[0];
    eh->ether_dhost[1] = destMac[1];
    eh->ether_dhost[2] = destMac[2];
    eh->ether_dhost[3] = destMac[3];
    eh->ether_dhost[4] = destMac[4];
    eh->ether_dhost[5] = destMac[5];

    /* Ethertype field */
    pktLen += sizeof(struct ether_header);

    if (ipParser_isIpv4(dst_addr))
    {
        /* Set next protocol after the Eth Frame to be Ipv4 */
        eh->ether_type = htons(ETH_P_IP);

        int nwords = 0;     /* Used to calculate amount of words in ip header */

        /* Used for source Ipv4 Address */
        struct ifaddrs *ifap, *ifa;
        struct sockaddr_in *sa = NULL;

        __u32 sourceAddr;

        iph = (struct iphdr *) (sendbuf + sizeof(struct ether_header));

        /*
         * If from the configuration file the src_addrr is set to auto get the src
         * addr of the interface
         */
        /* Get the IP address of the interface to send on */
        if (getifaddrs(&ifap) == 0) {
            for (ifa = ifap; ifa; ifa = ifa->ifa_next) {
                if (ifa->ifa_addr->sa_family == AF_INET) {
                    if(strcmp(ifa->ifa_name, ifName) == 0) {
                        sa = (struct sockaddr_in *) ifa->ifa_addr;
                    }
                }
            }
        }
        if (sa != NULL){
            sourceAddr = inet_addr(inet_ntoa(sa->sin_addr));
        } else {
            fprintf(stderr, "[%s] Failed to obtain source internet address!\n", __func__);
            return -1;
        }

        /* IPv4 header */
        iph->version  = 4;
        iph->ihl      = 5;
        iph->tos      = 0;
        iph->frag_off = htons(0x4000);
        iph->tot_len  = htons(sizeof(struct iphdr) + sizeof(struct ard_header) + sizeof(__u8) * dataLen);
        iph->id       = htons(0);
        iph->ttl      = 64;
        iph->protocol = 17; // UDP
        iph->saddr    = sourceAddr;
        iph->daddr    = dst_addr->dwords[0];
        iph->check    = 0x0000; /* The checksum field is set to zero before csum calc */

        /*
         * Pass the ip header buffer and the amount of 16bit blocks in it.
         * 4 * 5 = 20 bytest;
         * nwords = 20 / 2 = 10;
         */
        nwords = (4 * iph->ihl) / 2;
        iph->check = csum((unsigned short *)iph, nwords);

        pktLen += sizeof(struct iphdr);
    }
    else
    {
        /* Return 0 length of the packet indicating packet creation failure */
        return 0;
    }

/*
    pktLen += sizeof(ktHdr_t);
    pktLen += sizeof(__u8) * dataLen;
*/
    return pktLen;
}

void packet_Dump(__u8 *buf, __u32 dummplen)
{
    fprintf(stdout, "\n[%s] | Packet Dump |\n", __func__);
    hexDump(buf, dummplen);

    return;
}
