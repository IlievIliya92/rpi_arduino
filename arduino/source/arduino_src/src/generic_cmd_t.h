#ifndef _GENERIC_CMD_H_
#define _GENERIC_CMD_H_

#ifdef __cplusplus
extern "C" {
#endif


/******************************** INCLUDE FILES *******************************/

/*********************************** DEFINES **********************************/

/* S> / CMID / SED / 30 bytest DATA / <E */

/* S>01<E*  - START */

/* S>02002000<E* - PWM */
/* S>0200300<E* - PWM */

/* S>03001<E* - DO - ON */
/* S>03000<E* - DO - OFF */

/* S>05<E*  - STOP */

/* Invalid command */
/* S>0101DATAdsadadasdadasdasdadasdasdasdadadadasdadasdasdas<E* */

#define CMD_COKIE            "S>"

#define CMD_COKIE_LEN        3 /* 16bitsCOOKIE + \n */
#define CMD_ID_LEN           3 /* 16bitsID + \n */
#define CMD_SESION_ID_LEN    3 /* 16bitsSID + \n */
#define CMD_PAYLOAD_LEN      11 /* 10bytePayload + \n */
#define CMD_TRAILER_LEN      3 /* 16bitsTLR + \n */

#define CMD_TRAILER          "<E"

#define CMD_END              '*'

#define CMD_SIZE (CMD_COKIE_LEN + CMD_ID_LEN  \
                  + CMD_SESION_ID_LEN + CMD_PAYLOAD_LEN \
                  + CMD_TRAILER_LEN)

#define CHECK_PAYLOAD(var, id) ((var) == (id))

/************************** INTERFACE DATA DEFINITIONS ************************/
typedef enum
{
    ERR = 0,
    OK
} command_status_t;

typedef enum
{
    START_ID = 1, // Start                      01
    PWM_ID,       // session_Id + Payload        02
    DO_ID,        // session_Id + Payload       03
    ADCC_ID,      // session_Id + Payload       04
    STOP_ID,      // Stop                       05
    COMMANDS
} command_id_t;

typedef enum pwmCh_t {
    PWMCH0 = 0,
    PWMCH1,
    PWMCHN
} pwmCh_t;

typedef enum dioCh_t {
    DIO0 = 0,
    DIO1,
    DIO2,
    DIO3,
    DIO4,
    DION
} dioCh_t;

typedef enum dioStates_t {
    OFF = 0,
    ON
} dioStates_t;

/* Generic tasks structure */
typedef struct {
    uint8_t cmd_cookie[CMD_COKIE_LEN];
    uint8_t cmd_id[CMD_ID_LEN];
    uint8_t cmd_sessionId[CMD_SESION_ID_LEN];
    uint8_t cmd_payload[CMD_PAYLOAD_LEN];
    uint8_t cmd_trailer[CMD_TRAILER_LEN];
} genericCmdMsg_t;

typedef enum
{
    RDY = 0,
    CKIE,
    TLR,
    PWM,
    DO,
    ADCC,
    INVD,
    END,
    RESPONSES
} response_id_t;

void cmd_sendResponse(response_id_t id, int status);
void cmd_sendData(response_id_t id, int status, char *value);

#ifdef __cplusplus
}
#endif

#endif /* _GENERIC_CMD_H_ */

