#Universidad del Valle de Guatemala
#Algoritmos y estructura de datos
#Hoja de Trabajo 5
#Joice Andrea Miranda 15552
#Mario Hernandez 15135

import simpy
import random

def proceso(simpyEnv, velocidadPro,tiempoProceso, nombre, ram, cantMemoria, cantInstrucciones):
    global tmps
    global tiempoTotal

    #New
    yield simpyEnv.timeout(tiempoProceso)
    print ('tiempo: %f -%s (new) solicita %d de memoria ram' % (simpyEnv.now, nombre, cantMemoria))
    tiempoLlegada = simpyEnv.now

    #ram que se va a utilizar
    yield ram.get(cantMemoria)
    print('tiempo: %f-%s (admited) solicitud aceptada por %d de memoria ram' % (simpy.Env, nombre, cantMemoria))


    #Revisar si las intrucciones estan completas
    completo =0

    while completo < cantInstrucciones:
        with cpu.request() as req:
            yield req
            if (cantInstrucciones-completo)>= velocidadPro:
                        realizar=velocidadPro
            else:
                realizar=(cantInstrucciones-completo)
                print ('tiempo: %f-%s (ready) cpu ejecutara %d instrucciones' % (simpyEnv.now, nombre, realizar))
                yield simpyEnv.timeout(realizar/velocidadPro)

                completo++ realizar
                print('tiempo: %f-%s (running) cpu (%d/%d) completo' %(simpyEnv.now, nombre, completo, cantIntrucciones))
                
        

#variables
velocidadPro = 3.0
memoriaRAM= 100 
cant_procesos= 25
tiempos= []
tiempoTotal= 0.0
simpyEnv= simpy.Environment()
cpu= simpy.Resource (simpyEnv, capacity=2)
ram= simpy.Container (simpyEnv, init=memoriaRAM, capacity=memoriaRAM)
waiting =simpy.Resource(simpyEnv, capacity=2)

    
