def test():
    print("Hello, this is working quite well")

def getData():
    print("Se necesita proveer el ADD o los datos necesarios para calcularlo.")
    print("""¿Cuál de las siguientes opciones aplica?

1.  Ya se tiene el ADD
2.  Se desea calcular el ADD""")
    decision =  int(input("\n Elije una opción: "))
    if decision == 1:
