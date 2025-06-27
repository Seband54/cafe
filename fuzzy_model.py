import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Variables
acidez = ctrl.Antecedent(np.arange(0, 8.1, 0.1), 'acidez')
cafeina = ctrl.Antecedent(np.arange(0, 3.1, 0.1), 'cafeina')
humedad = ctrl.Antecedent(np.arange(0, 13, 1), 'humedad')
aroma = ctrl.Antecedent(np.arange(0, 11, 1), 'aroma')
calidad = ctrl.Consequent(np.arange(0, 101, 1), 'calidad')

# Funciones de pertenencia
acidez['baja'] = fuzz.trimf(acidez.universe, [0, 4.0, 4.8])
acidez['optima'] = fuzz.trimf(acidez.universe, [4.6, 5.0, 5.4])
acidez['alta'] = fuzz.trimf(acidez.universe, [5.2, 6.0, 8])

cafeina['baja'] = fuzz.trimf(cafeina.universe, [0, 0.8, 1.2])
cafeina['media'] = fuzz.trimf(cafeina.universe, [1.0, 1.5, 2.0])
cafeina['alta'] = fuzz.trimf(cafeina.universe, [1.8, 2.5, 3.0])

humedad['baja'] = fuzz.trimf(humedad.universe, [0, 2, 5])
humedad['media'] = fuzz.trimf(humedad.universe, [4, 6, 8])
humedad['alta'] = fuzz.trimf(humedad.universe, [7, 10, 12])

aroma['bajo'] = fuzz.trimf(aroma.universe, [0, 2, 4])
aroma['medio'] = fuzz.trimf(aroma.universe, [3, 5, 7])
aroma['alto'] = fuzz.trimf(aroma.universe, [6, 8, 10])

calidad['baja'] = fuzz.trimf(calidad.universe, [0, 25, 50])
calidad['media'] = fuzz.trimf(calidad.universe, [40, 60, 80])  # más centrada y más solapada
calidad['alta'] = fuzz.trimf(calidad.universe, [70, 85, 100])

# Reglas
reglas = [
    ctrl.Rule(acidez['optima'] & cafeina['media'] & humedad['baja'] & aroma['alto'], calidad['alta']),
    ctrl.Rule(acidez['optima'] & cafeina['media'] & humedad['media'] & aroma['alto'], calidad['alta']),
    ctrl.Rule(acidez['optima'] & cafeina['media'] & humedad['baja'] & aroma['medio'], calidad['media']),
    ctrl.Rule(acidez['alta'] | acidez['baja'], calidad['baja']),
    ctrl.Rule(humedad['alta'], calidad['baja']),
    ctrl.Rule(aroma['bajo'], calidad['baja']),
    ctrl.Rule(acidez['optima'] & cafeina['media'] & humedad['media'] & aroma['medio'], calidad['media']),
    ctrl.Rule(acidez['optima'] & cafeina['alta'] & humedad['baja'] & aroma['alto'], calidad['alta']),
    ctrl.Rule(acidez['optima'] & cafeina['baja'] & humedad['baja'] & aroma['medio'], calidad['media']),
    ctrl.Rule(acidez['optima'] & cafeina['media'] & humedad['media'] & aroma['medio'], calidad['media']),
    ctrl.Rule(acidez['optima'] & cafeina['alta'] & humedad['media'] & aroma['medio'], calidad['media']),
    ctrl.Rule(acidez['optima'] & cafeina['media'] & humedad['baja'] & aroma['bajo'], calidad['media']),
    ctrl.Rule(acidez['optima'] & cafeina['baja'] & humedad['media'] & aroma['medio'], calidad['media']),
    ctrl.Rule(acidez['optima'] & cafeina['media'] & humedad['alta'] & aroma['medio'], calidad['media']),
]

# Sistema (esto es clave)
sistema_calidad = ctrl.ControlSystem(reglas)

# Evaluador expuesto
def evaluar_calidad_cafe(acidez_val, cafeina_val, humedad_val, aroma_val):
    try:
        simulador = ctrl.ControlSystemSimulation(sistema_calidad)

        simulador.input['acidez'] = np.clip(acidez_val, 0, 8)
        simulador.input['cafeina'] = np.clip(cafeina_val, 0, 3)
        simulador.input['humedad'] = np.clip(humedad_val, 0, 12)
        simulador.input['aroma'] = np.clip(aroma_val, 0, 10)

        simulador.compute()
        resultado = simulador.output['calidad']

        if np.isnan(resultado):
            return 0, "No evaluable"

        if resultado <= 40:
            categoria = "Baja"
        elif 40 < resultado <= 70:
            categoria = "Media"
        else:
            categoria = "Alta"

        return round(resultado, 1), categoria

    except Exception as e:
        print("Error interno:", e)
        return 0, "Error"
