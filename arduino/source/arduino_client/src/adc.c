/******************************** INCLUDE FILES *******************************/
#include <util/delay_basic.h>

#include "freeRTOS/FreeRTOS.h"
#include "freeRTOS/semphr.h"
#include "freeRTOS/queue.h"

/* serial interface include file. */
#include "freeRTOS/lib_io/serial.h"
#include "freeRTOS/lib_io/digitalAnalog.h"

#include "adc.h"
/******************************** LOCAL DEFINES *******************************/


/******************************** GLOBALDATA *******************************/
extern xComPortHandle xSerialPort;

/********************************* LOCAL DATA *********************************/
static SemaphoreHandle_t xADCSemaphore;
static xADCArray adcValues;

/******************************* INTERFACE DATA *******************************/
QueueHandle_t xAdcQueue = NULL;

/************************ LOCAL FUNCTIONS PROTOTYPES***************************/

/******************************* LOCAL FUNCTIONS ******************************/

static void adc_Init(void)
{
    /* Initialize analog inputs */
    enbAnalogInput(analogIn0);
    enbAnalogInput(analogIn1);

    /* Initialize adc values to 0 */
    adcValues.adc0 = 0;
    adcValues.adc1 = 0;

    /* Initialize msg Queue */
    xAdcQueue = xQueueCreate(5, sizeof(uint32_t));

    vSemaphoreCreateBinary(xADCSemaphore);

    return;
}

static void adc_readSensors(void)
{
    const TickType_t xBlockTime = pdMS_TO_TICKS(200);

    if( xADCSemaphore != NULL )
    {
        if( xSemaphoreTake(xADCSemaphore, (TickType_t)10) == pdTRUE)
        {
            setAnalogMode(MODE_10_BIT);    // 10-bit analogue-to-digital conversions

            startAnalogConversion(analogIn0, EXTERNAL_REF);   // start next conversion
            while(analogIsConverting())
                _delay_loop_2(5);

            adcValues.adc0 = analogConversionResult();

            startAnalogConversion(analogIn1, EXTERNAL_REF);
            while(analogIsConverting())
                 _delay_loop_2(5);

            adcValues.adc1 = analogConversionResult();

            /* Send indication to serialPort task */
            xQueueSend(xAdcQueue, &adcValues, xBlockTime);

            xSemaphoreGive(xADCSemaphore);
        }
    }

    return;
}

static void adc_Task(void *pvParameters)
{
    (void) pvParameters;
    TickType_t xLastWakeTime;

    xLastWakeTime = xTaskGetTickCount();

    while(1)
    {
        adc_readSensors();
        vTaskDelayUntil( &xLastWakeTime, (30 / portTICK_PERIOD_MS));
    }

    return;
}

/***************************** INTERFACE FUNCTIONS ****************************/
genericTask_t adc = {
    adc_Init,
    adc_Task,
    "ADC TASK",
    256,
    1,
    &adcValues,
    NULL
};

genericTask_t *getAdcTask(void)
{
    return &adc;
}
