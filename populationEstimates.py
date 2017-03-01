import sys, math

# Special import designed to handle errors opening openpyxl module
try:
    import openpyxl
except ImportError as iE:
    print("Python Excel module 'openpyxl' not found")
    sys.exit(1)



# List that will hold the names of the municipalities
munList = []

# Dictionary that will hold the data for each municipality.
# The dictionary has the structure: {munName:[t0,P0,t1,P1,t2,P2,tp1,..],...}
munData = {}

wb = openpyxl.Workbook()

# Name for the file
fileName = ''

# Dictionary that contains variable names
dataIndex = {0: 't0', 1: 'p0', 2: 't1', 3: 'p1', 4: 't2', 5: 'p2', 6: 't'}

"""Function that starts data collection for program to use.  It simply asks
    for an integer and validates the user's input."""


def getData():
    global munList
    cantidad_de_municipios = int(input("\n¿Cuántos municipios o barrios deseas incluir?: "))
    if cantidad_de_municipios < 1:
        print("""Ingresa una cantidad de municipios o barrios válida
    (Valor de 1 en adelante).\n""")
        getData()
    # If all is properly validated, munList() function is called to start collecting data
    else:
        munList(cantidad_de_municipios)
        munData(munList)
        popCalc()


"""This is the function that collects data for each of the municipalities"""


def munList(munNum):
    global munList
    munList = []
    count = 0
    munName = ""
    # This loop generates a list for the names of the municipalities.
    while count < munNum:
        munName = input("Ingresa el nombre del municipio o barrio #" + str(count + 1) + ": ")
        munList.append(munName)
        count += 1

    print("Se trabaja con " + str(munNum) + " municipio/s.")
    print("\nLos municipios son:\n")
    for i in range(len(munList)):
        print(str(i + 1) + '.' + munList[i])


"""This function generates a dictionary for each municipality containing
its pertinent data."""


# Function will only allow for one projection year for the time being.
def munData(municipios):
    t0 = 0
    t1 = 0
    t2 = 0
    p0 = 0
    p1 = 0
    p2 = 0
    t = 0
    global munData, fileName
    munData = {}
    for i in range(len(municipios)):
        munData[municipios[i]] = []
    for k in munData.keys():
        print("\nIngresemos los datos para: " + k + '\n')
        t0 = int(input("Ingresa el tiempo de origen (t0): "))
        p0 = int(input("Ingresa población de origen (p0): "))
        t1 = int(input("Ingresa tiempo 1 (t1): "))
        p1 = int(input("Ingresa población correspondiente a t1 (p1): "))
        t2 = int(input("Ingresa tiempo 2 (t2): "))
        p2 = int(input("Ingresa población correspondiente a t2 (p2): "))
        t = int(input("Ingresa año de proyección (t): "))
        munData[k] = [t0, p0, t1, p1, t2, p2, t]
    fileName = input("\nIngresa un nombre para el documento Excel a ser generado: ")


"""This is the function that creates the spreadsheet and maps given
values to their respective cells."""


# Function has an error in the loop.
def popCalc():
    global munData, wb, cellIndex, dataIndex
    wb.remove_sheet(wb.get_sheet_by_name('Sheet'))
    count = 0
    for k in munData.keys():
        wb.create_sheet(index=count, title=k)
        sheet = wb.get_sheet_by_name(k)
        countList = 0
        for i in munData[k]:
            cellLetter = 'A'
            cellNumber = countList + 1
            cellCode = cellLetter + str(cellNumber)
            sheet[cellCode] = dataIndex[countList]
            cellLetter = 'B'
            cellCode = cellLetter + str(cellNumber)
            sheet[cellCode] = i
            countList += 1
        count += 1
    pSat()


"""This function calculates the Saturation Population and maps its value for all
given municipalities to their respective cells and sheets"""


def pSat():
    global munList, fileName
    for i in range(len(munList)):
        sheet = wb.get_sheet_by_name(munList[i])
        p0 = sheet['B2'].value
        p1 = sheet['B4'].value
        p2 = sheet['B6'].value
        t1 = sheet['B3'].value
        t0 = sheet['B1'].value
        t = sheet['B7'].value - t0

        saturationPopulation = round((2 * p0 * p1 * p2 - (p1 ** 2) * (p0 + p2)) / (p0 * p2 - (p1 ** 2)))

        sheet['A9'].value = 'pSat'
        sheet['B9'].value = saturationPopulation

        a = round((saturationPopulation - p0) / p0, 2)
        n = t1 - t0
        b = round((1 / n) * math.log((p0 * (saturationPopulation - p1)) / (p1 * (saturationPopulation - p0))), 4)

        sheet['A10'].value = 'p' + str(sheet['B7'].value)
        print(str(projectedPop(a, b, saturationPopulation, t)))
        sheet['B10'].value = projectedPop(a, b, saturationPopulation, t)
        wb.save(fileName + '.xlsx')

        # Remember to add a handler for decreasing


"""This function simply takes four arguments a, b,sat and t, and performs the projected population
calculation according to the mathematical logistic curve method.  It returns it as
'projection' """


def projectedPop(a, b, sat, t):
    projection = sat // (1 + a * math.exp(b * t))
    return projection