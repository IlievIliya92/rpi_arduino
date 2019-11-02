#ifndef _GENERIC_CMD_H_
#define _GENERIC_CMD_H_

#ifdef __cplusplus
extern "C" {
#endif


/******************************** INCLUDE FILES *******************************/

/*********************************** DEFINES **********************************/

/* S> / CMID / SED / 30 bytest DATA / <E */

/* S>01<E*  - START */
/* S>0201500&700<E* - PWM */
/* S>05<E*  - STOP */

/* Invalid command */
/* S>0101DATAdsadadasdadasdasdadasdasdasdadadadasdadasdasdas<E* */

#define CMD_COKIE            "S>"

#define CMD_COKIE_LEN        3 /* 16bitsCOOKIE + \n */
#define CMD_ID_LEN           3 /* 16bitsID + \n */
#define CMD_SESION_ID_LEN    3 /* 16bitsSID + \n */
#define CMD_PAYLOAD_LEN      31 /* 30bytePayload + \n */
#define CMD_TRAILER_LEN      3 /* 16bitsTLR + \n */

#define CMD_TRAILER          "<E"

#define CMD_END              '*'

#define CMD_SIZE (CMD_COKIE_LEN + CMD_ID_LEN  \
                  + CMD_SESION_ID_LEN + CMD_PAYLOAD_LEN \
                  + CMD_TRAILER_LEN)

#define CHECK_PAYLOAD(var, id) ((var) == (id))

#define PWM_DATA_TOK    "&"

/************************** INTERFACE DATA DEFINITIONS ************************/
typedef enum
{
    ERR = 0,
    OK
} command_status_t;

typedef enum
{
    START_ID = 1, // Start                      01
    PWM_ID,      // session_Id + Payload        02
    CMD2_ID,      // session_Id + Payload       03
    CMD3_ID,      // session_Id + Payload       04
    STOP_ID,      // Stop                       05
    COMMANDS
} command_id_t;

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
    CMD2,
    CMD3,
    INVD,
    END,
    RESPONSES
} response_id_t;

void cmd_sendResponse(response_id_t id, int status);

#ifdef __cplusplus
}
#endif

#endif /* _GENERIC_CMD_H_ */

