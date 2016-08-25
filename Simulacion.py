# Universidad del Valle de Guatemala
# Algoritmos y Estructura de datos
# Hoja de trabajo 5
#Joice Miranda 15552
#Mario Hernandez 15135



import simpy
import random


def proceso(env, tiempoProceso, nombre, ram, cantMemoria, cantInstrucciones, velocidadPros):
    global tiempoTotal
   
    
   #Paso: New
    yield env.timeout(tiempoProceso)
    print('tiempo: %f - %s (new) solicita %d de memoria ram' % (env.now, nombre, cantMemoria))
    tiempollegada = env.now 
    
    #ram que se va a utilizar
    yield ram.get(cantMemoria)
    print('tiempo: %f - %s (admited) solicitud aceptada por %d de memoria ram' % (env.now, nombre, cantMemoria))

    #Revisar si las intrucciones estan completas
    completo = 0
    
    while completo < cantInstrucciones:

    
        #pasa a ready
        with cpu.request() as req:
            yield req
            #instruccionss a realizar
            if (cantInstrucciones-completo)>=velocidadPros:
                realizar=velocidadPros
            else:
                realizar=(cantInstrucciones-completo)
            #tiempo de instrucciones a ejecutar
            print('tiempo: %f - %s (ready) cpu ejecutara %d instrucciones' % (env.now, nombre, realizar))
            yield env.timeout(realizar/velocidadPros)

            #instrucciones completas
            completo += realizar
            print('tiempo: %f - %s (runing) cpu (%d/%d) completado' % (env.now, nombre, completo, cantInstrucciones))

        #Decide si espera o pasa a ready
        verificar = random.randint(1,2)

        if verificar == 1 and completo<cantInstrucciones:
         
            with waiting.request() as req2:
                yield req2
                #tiempo de operaciones i/o
                yield env.timeout(1)                
                print('tiempo: %f - %s (waiting) realizadas operaciones (entrada/salida)' % (env.now, nombre))
    

    #paso exir
    #devolviendo cant ram
    yield ram.put(cantMemoria)
    print('tiempo: %f - %s (terminated), retorna %d de memoria ram' % (env.now, nombre, cantMemoria))
    #tiempo de todos los procesos
    tiempoTotal += (env.now -tiempollegada) 
    tiempos.append(env.now - tiempollegada)

    
#Variables

#instrucciones por tiempo
velocidadPros = 3.0
#cantidad de ram
memoriaRam= 100
#procesos a ejecutar
cantProcesos= 25
#guarda todos los tiempos individuales
tiempos= []
#tiempo total de los procesos
tiempoTotal= 0.0    

#crear ambiente de simulacion
env = simpy.Environment()
#cola (acceso a cpu)
cpu = simpy.Resource (env, capacity=2)
#simula ram
ram = simpy.Container(env, init=memoriaRam, capacity=memoriaRam)
#acceso i/o
waiting = simpy.Resource (env, capacity=2)




#Semilla de random 
random.seed(1904)
rank = 1 # numero de intervalos a ejecutar


# PROCESOS A SIMULAR
for inicial in range(cantProcesos):
    tiempoProceso = random.expovariate(1.0 / rank)
    #numero de instrucciones
    cantInstrucciones = random.randint(1,10)
    #memoria a utilizar
    cantMemoria = random.randint(1,10) 
    env.process(proceso(env, tiempoProceso, 'Proceso %d' % inicial, ram, cantMemoria, cantInstrucciones, velocidadPros))

#inicia simulacion
env.run()

#promedio de accessos 
print " "
promedio=(tiempoTotal/cantProcesos)
print('El tiempo promeido es: %f' % (promedio))


#Desviacion estandar
suma=0

for xinicial in tiempos:
    suma+=(xinicial-promedio)**2

desviacion=(suma/(cantProcesos-1))**0.5

print " "
print('La desviacion estandar es: %f' %(desviacion))
