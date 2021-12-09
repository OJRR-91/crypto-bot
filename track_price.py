import numpy as np
precios =[]
for i in np.arange(10,1,-0.1):
    precios.append(i)


for i in np.arange(1,7,0.1):
    precios.append(i)


def precio_bajo(precio,precio_anterior):
    if precio < precio_anterior:
        precio_compra_bajo = (precio * 1.01)
        return(precio_compra_bajo)

def compra_baja(precio, precio_compra_bajo):
    if precio <= precio_anterior:
        print("Compra", precio)
        return True

precio_anterior,n = 0, 0
for i in precios:
    precio_compra_bajo = precio_bajo(i,precio_anterior)
    #print (precio_compra_bajo)
    if compra_baja(i, precio_compra_bajo):
        break
    precio_anterior = i
    n+=1
