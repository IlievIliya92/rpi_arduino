#ifndef _GENERIC_CMD_H_
#define _GENERIC_CMD_H_

#ifdef __cplusplus
extern "C" {
#endif


/******************************** INCLUDE FILES *******************************/

/*********************************** DEFINES **********************************/

/* S> / CMID / SED / 30 bytest DATA / <E */

/* S>01<E* */
/* S>0401DATA<E* */
/* S>0101DATAdsadadasdadasdasdadasdasdasdadadadasdadasdasdas<E* */

#define CMD_COKIE            "S>"

#define CMD_COKIE_LEN        3 /* 16bitsCOOKIE + \n */
#define CMD_ID_LEN           3 /* 16bitsID + \n */
#define CMD_SESION_ID_LEN    3 /* 16bitsSID + \n */
#define CMD_PAYLOAD_LEN      31 /* 30bytePayload + \n */
#define CMD_TRAILER_LEN      3 /* 16bitsTLR + \n */

#define CMD_TRAILER          "<E"

#define CMD_END              '*'

#define ERR         0
#define OK          1

#define CMD_SIZE (CMD_COKIE_LEN + CMD_ID_LEN  \
                  + CMD_SESION_ID_LEN + CMD_PAYLOAD_LEN \
                  + CMD_TRAILER_LEN)

#define CHECK_PAYLOAD(var, id) ((var) == (id))

/************************** INTERFACE DATA DEFINITIONS ************************/
typedef enum
{
    CMD1 = 1, // Preamble
    CMD2,     // Start
    CMD3,     // Stop
    CMD4,     // session_Id + Payload
    CMD5,     // session_Id + Payload
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
    RCV = 0,
    CKIE,
    TLR,
    RESPONSES
} response_id_t;

void cmd_sendResponse(response_id_t id, int status);

#ifdef __cplusplus
}
#endif

#endif /* _GENERIC_CMD_H_ */

