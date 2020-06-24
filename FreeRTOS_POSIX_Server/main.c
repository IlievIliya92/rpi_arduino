/******************************** INCLUDE FILES *******************************/
/* System headers. */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/time.h>
#include <linux/ip.h>
#include <net/if.h>
#include <netinet/ether.h>


#include "Utils/network.h"
#include "FreeRTOS.h"
#include "task.h"


/********************************** DEFINES ***********************************/
typedef enum arguments
{
	APPNAME = 0,
	HOST_INTERFACE,
	DEST_MAC,
	DEST_IP,
	ARGUMENTS
}arguments_t;
/******************************* LOCAL FUNCTIONS ******************************/

static
void usage(const char *name)
{
    fprintf(stdout,"\n"
"\n"
"\n"
"Failed to start the Webserver!\n"
"\n"
"Usage:\n"
"\n"
"\n"
" %s [host interface] [destination mac] [destination ip]\n\n", name);

 	return;
}

/********************************* GLOBAL DATA ********************************/

/************************************** MAIN **********************************/
int main(int argc, char *argv[])
{
    char ifName[IFNAMSIZ];
    __u8 destMac[ETH_ALEN] = {0};
    ipParser_t dst_addr;

    if (argc < ARGUMENTS) {
        usage(argv[APPNAME]);
        goto exit;
    }

    if (! (network_getIface(argv[HOST_INTERFACE], ifName) &&
           network_getMacAddr(argv[DEST_MAC], destMac) &&
           network_getIpAddr(argv[DEST_IP], &dst_addr)))
        {
            usage(argv[APPNAME]);
            goto exit;
        }

    fprintf(stdout, "[%s] Starting Server Application on interface %s\n", __func__, ifName);

	/* Set the scheduler running.  This function will not return unless a task calls vTaskEndScheduler(). */
	vTaskStartScheduler();

exit:
	return 1;
}
/*-----------------------------------------------------------*/

/*-----------------------------------------------------------*/
static unsigned long uxQueueSendPassedCount = 0;
void vMainQueueSendPassed( void )
{
	/* This is just an example implementation of the "queue send" trace hook. */
	uxQueueSendPassedCount++;
}

/*-----------------------------------------------------------*/
void vApplicationIdleHook( void )
{

#ifdef __GCC_POSIX__
	struct timespec xTimeToSleep, xTimeSlept;
		/* Makes the process more agreeable when using the Posix simulator. */
		xTimeToSleep.tv_sec = 1;
		xTimeToSleep.tv_nsec = 0;
		nanosleep( &xTimeToSleep, &xTimeSlept );
#endif

	return;
}


