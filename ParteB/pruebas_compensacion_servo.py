"""Pruebas sin hardware de la compensación común del tramo final."""
import math
import unittest
from types import SimpleNamespace
from hardware import CONFIG, Raspberry, pulso_servo, parametros_servo

class Compensacion(unittest.TestCase):
    def test_tramo_inicial_y_final(self):
        for angulo, esperado in ((0,500),(45,1000),(90,1500),(135,2000),(180,2550)):
            self.assertAlmostEqual(pulso_servo(angulo, CONFIG), esperado)
        valores = [pulso_servo(a / 10, CONFIG) for a in range(1801)]
        self.assertTrue(all(b > a for a,b in zip(valores, valores[1:])))
        self.assertLess(pulso_servo(135.0001, CONFIG)-pulso_servo(135, CONFIG), .002)

    def test_sin_compensacion(self):
        cfg = dict(CONFIG, servo_compensacion_final_us=0)
        for a in (0,45,90,135,160,170,180):
            self.assertAlmostEqual(pulso_servo(a,cfg), 500+2000*a/180)

    def test_libreria_ambos_canales(self):
        h = Raspberry.__new__(Raspberry)
        h.servos = [SimpleNamespace(fraction=None), SimpleNamespace(fraction=None)]
        minimo,maximo,_,extra = parametros_servo(CONFIG)
        for indice in (0,1):
            for angulo in (0,45,90,135,160,170,180):
                h.servo(indice,angulo)
                fraccion=h.servos[indice].fraction
                self.assertTrue(0 <= fraccion <= 1)
                self.assertAlmostEqual(minimo+fraccion*(maximo+extra-minimo),
                                       pulso_servo(angulo,CONFIG))

    def test_entradas_invalidas(self):
        for valor in (-1,181,math.nan,math.inf):
            with self.assertRaises(ValueError):
                pulso_servo(valor,CONFIG)
        for extra in (-1,101,math.nan):
            with self.assertRaises(ValueError):
                parametros_servo(dict(CONFIG,servo_compensacion_final_us=extra))

if __name__ == "__main__":
    unittest.main()
