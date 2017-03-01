#!/usr/bin/env python3
# Variable to handle runtime
import populationEstimates, waterDemand
isRunning = True

def mainMenu():
    global isRunning
    print("""---------------------------------------
Bienvenidos a Capstone Tools (V Beta 1.2)
---------------------------------------
Creado por: Samuel R. Rivera Loubriel
email:      writesamr@gmail.com
---------------------------------------""")
    while (isRunning):
        print("""¿Qué deseas hacer?

1) Estimados de Población
2) Demanda de Agua
3) Salirt""")
        decision = int(input("\nElije una alternativa#: "))
        if (decision == 1):
            populationEstimates.getData()
        elif (decision == 2):
            waterDemand.test()
            isRunning = False
        elif (decision == 3):
            isRunning = False
        else:
            print("\nElije una opción válida.\n")


if __name__ == "__main__":
    if (isRunning):
        mainMenu()


