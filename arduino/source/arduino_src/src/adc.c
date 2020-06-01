/******************************** INCLUDE FILES *******************************/
#include <stdlib.h>

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

/******************************* INTERFACE DATA *******************************/

/************************ LOCAL FUNCTIONS PROTOTYPES***************************/

/******************************* LOCAL FUNCTIONS ******************************/

static void adc_Init(void)
{
    /* Initialize analog inputs */
    enbAnalogInput(analogIn0);
    enbAnalogInput(analogIn1);
    enbAnalogInput(analogIn2);
    enbAnalogInput(analogIn3);
    enbAnalogInput(analogIn4);

    vSemaphoreCreateBinary(xADCSemaphore);

    return;
}

static void adc_readSensors(void *args)
{
    xADCArray *adcValues = (xADCArray *)args;

    if( xADCSemaphore != NULL )
    {
        if( xSemaphoreTake(xADCSemaphore, (TickType_t)10) == pdTRUE)
        {
            setAnalogMode(MODE_10_BIT);    // 10-bit analogue-to-digital conversions

            startAnalogConversion(analogIn0, EXTERNAL_REF);   // start next conversion
            while(analogIsConverting())
                _delay_loop_2(2);
            adcValues->adc0 = analogConversionResult();

            startAnalogConversion(analogIn1, EXTERNAL_REF);
            while(analogIsConverting())
                _delay_loop_2(2);
            adcValues->adc1 = analogConversionResult();

            startAnalogConversion(analogIn2, EXTERNAL_REF);   // start next conversion
            while(analogIsConverting())
                _delay_loop_2(2);
            adcValues->adc2 = analogConversionResult();

            startAnalogConversion(analogIn3, EXTERNAL_REF);
            while(analogIsConverting())
                _delay_loop_2(2);
            adcValues->adc3 = analogConversionResult();

            startAnalogConversion(analogIn4, EXTERNAL_REF);
            while(analogIsConverting())
                _delay_loop_2(2);
            adcValues->adc4 = analogConversionResult();

            xSemaphoreGive(xADCSemaphore);
        }
    }

    return;
}

static
genericCmdHandler_t adc = {
    adc_Init,
    NULL,
    adc_readSensors
};

/***************************** INTERFACE FUNCTIONS ****************************/
genericCmdHandler_t *getAdcCmdHandler(void)
{
    return &adc;
}

