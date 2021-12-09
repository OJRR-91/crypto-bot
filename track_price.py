def precio_bajo(precio,precio_anterior,precio_compra_bajo_anterior):
    if precio < precio_anterior:
        precio_compra_bajo = (precio * 1.3)
        return(precio_compra_bajo)
    else:
        return(precio_compra_bajo_anterior)


def compra_baja(precio, precio_compra_bajo):
    if precio >= precio_compra_bajo:
        print("Compra", precio)
        return True

precio_anterior,n,precio_compra_bajo_anterior = 100, 0, 0
for i in precios:
    precio_compra_bajo = precio_bajo(i,precio_anterior, precio_compra_bajo_anterior)
    precio_compra_bajo_anterior = precio_compra_bajo
    print (precio_compra_bajo, i)
    if compra_baja(i, precio_compra_bajo_anterior):
        break
    print(precio_anterior)
    precio_anterior = i
    n+=1
