from machine import Pin, ADC, PWM
from time import sleep_ms

# CONFIGURACIÓN DE LEDS

led1 = Pin(16, Pin.OUT)
led2 = Pin(17, Pin.OUT)

# LED con PWM
led3 = PWM(Pin(18))
led4 = PWM(Pin(19))

# Frecuencia PWM
led3.freq(1000)
led4.freq(1000)

# CONFIGURACIÓN DE BOTONES

boton1 = Pin(14, Pin.IN, Pin.PULL_DOWN)
boton2 = Pin(15, Pin.IN, Pin.PULL_DOWN)

# CONFIGURACIÓN DE ADC

slider1 = ADC(26)
slider2 = ADC(27)

# ESTADO INICIAL DE LOS LED

estado_led1 = 0
estado_led2 = 0

led1.value(0)
led2.value(0)

# VARIABLES PARA LOS BOTONES

anterior_boton1 = 0
anterior_boton2 = 0
# PROGRAMA PRINCIPAL

while True:

    # BOTÓN 1 - LED 1

    boton_actual1 = boton1.value()

    if boton_actual1 == 1 and anterior_boton1 == 0:

        estado_led1 = not estado_led1
        led1.value(estado_led1)

        sleep_ms(200)

    anterior_boton1 = boton_actual1

    # BOTÓN 2 - LED 2
    
    boton_actual2 = boton2.value()

    if boton_actual2 == 1 and anterior_boton2 == 0:

        estado_led2 = not estado_led2
        led2.value(estado_led2)

        sleep_ms(200)

    anterior_boton2 = boton_actual2


        # SLIDER 1 - LED 3

    valor1 = slider1.read_u16()

    led3.duty_u16(valor1)

    # SLIDER 2 - LED 4
    
    valor2 = slider2.read_u16()

    led4.duty_u16(valor2)

    # Pequeña pausa
    sleep_ms(10)
