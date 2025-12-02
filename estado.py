def calcular_estado_inicial():
    """
    Inicializa el diccionario `estado` con los indicadores clave de la empresa,
    incluyendo todos los flags y contadores que luego se referencian en
    calcular_estado_final().
    """
    precio_venta = 4.5
    return {
        # Indicadores financieros y operativos
        "Caja disponible":                   50000,
        "Precio Venta": precio_venta,# agregado por mi
        "Inventario":                        0,
        "Pedidos por atender":               0,
        "Unidades vendidas":                 0,
        "Insumos disponibles":               100,
        "Cantidad de empleados":             4,
        "Costo por empleado":                2000,
        "Sueldos por pagar":                 4 * 2000,
        "Deuda pendiente":                   20000,
        "Reputacion del mercado":            "Nivel 3",
        "Multas e indemnizaciones":          0,
        "Maquinas (total/activas/dañadas)":  "5/5/0",

        # Banderas de prohibicion y seguro
        "Prohibir Produccion":               False,
        "Prohibir Compras":                  False,
        "Prohibir Importaciones":            False,
        "Fondo emergencia":                  False,

        # Contadores y flags temporales
        "TurnosProduccionExtra":             0,
        "DemandaExtraTemporal":              0,
        "DuracionRestante->Temporal":0 ,# agregado por mi
        "EmpleadosTemporales":               0,
        "MejoraProceso":                     False,
        "BrandingActivo":                    False,
        "MantenimientoHecho":                False,
        "EcommerceActivo":                   False,
        "IncentivosActivos":                 False, # agregado por mi
        "InventarioMesAnterior":             0,

        # contadores agregados por mi
        "Insumos":0,
        "registro de ventas_precios": [0, 0],
        "registro de ventas_indice": 0,
        "mejora_proceso":0,
        "duracion_demanda": 0,
        "competidores_nuevos": 0,
        "duracion_ecommerce": 0,
        "contador_fondo_emergencia": 0,
        "Ventas": 0,  # vinculado al estado final
        "Subida de sueldo":0,
        "bloqueador_clima":0, # uso de registro para tener doble control sobre las cartas
        "contador_actual":{"antes_inventario":0,"antes_insumos":0},
        "Registro_cambios37(tiempo)": {'a': 0, 'b': 0, 'c': 0}, # reiniciar pasado eso
        "Registro_cambios37": {'a': 0, 'b': 0, 'c': 0},
        "indice_deudas(cambios)": 0,
        "aumento_por 10%":0,

        #
        "Registro_de_deudas(duracion)":{'a':0,'b':0,'c':0,'d':0}, # relacionado al credito de proveedores
        "Registro_de_deudas(cantidad)": {'a': 0, 'b': 0, 'c': 0, 'd': 0},
        "indice_deudas":0
        #
    }

def calcular_estado_final(estado): # falta usar estado["r_produccion"] para la venta
    # funcion agregada por mi para multi deudas
    for s, d in estado["Registro_de_deudas(duracion)"].items():
       if d != 0:
          estado["Registro_de_deudas(duracion)"][s] -= 1
       if d ==0:
           if estado["Caja disponible"]>=estado["Registro_de_deudas(cantidad)"][s]:
              estado["Caja disponible"]-=estado["Registro_de_deudas(cantidad)"][s]
           else:
               estado["Deuda pendiente"]+=(estado["Registro_de_deudas(cantidad)"][s]-estado["Caja disponible"])*1.12
               estado["Caja disponible"]=0
    if estado["indice_deudas"] < 4:
        estado["indice_deudas"] += 1
    elif estado["indice_deudas"] == 4:
        estado["indice_deudas"] = 0
    #----------------------------------------------------------------------------------------

    #1-------------------
    if estado["R_ventas"]==0 and estado["p_venta"]==0 and estado["p_ventas,produccion"]==0 and estado["r_venta"]==0:
        r=(100-(estado["carta34(valor)"]+estado["carta29"]+estado["carta 26"]+estado["R-12"]))
        if r <0:
            r=0
        if r==100:
            while estado["Inventario"] > 0:
                if estado["Pedidos por atender"] > 0:
                    estado["Pedidos por atender"] -= 1
                    estado["Unidades vendidas"] += 1
                    estado["Caja disponible"] += estado["Precio Venta"]
                    estado["Ventas"] += 1
                elif estado["Pedidos por atender"] == 0:
                    break
                estado["Inventario"] -= 1
        else:
            qw = int(estado["Inventario"] * r/100)
            if qw!=0:
                estado["Inventario"] = qw
                while qw > 0:
                    if estado["Pedidos por atender"] > 0:
                        estado["Pedidos por atender"] -= 1
                        estado["Unidades vendidas"] += 1
                        estado["Caja disponible"] += estado["Precio Venta"]
                        estado["Ventas"] += 1
                    elif estado["Pedidos por atender"] == 0:
                        break
                    qw -= 1
    if estado["registro de ventas_indice"]==0:
        estado["registro de ventas_precios"][estado["registro de ventas_indice"]]=estado["Ventas"]
        estado["registro de ventas_indice"]+=1
    elif estado["registro de ventas_indice"]==1:
        estado["registro de ventas_precios"][estado["registro de ventas_indice"]] = estado["Ventas"]
        estado["registro de ventas_indice"]=0
    if estado["Pedidos por atender"]>0:
        estado["Reputacion del mercado"]="Nivel"+" "+ str(int(estado["Reputacion del mercado"].split()[-1])-1)
#2----------------------------------------------------
    estado["Demanda"]=1000*int(estado["Reputacion del mercado"].split()[-1])
    if estado["BrandingActivo"]==True and estado["duracion_branding"]>0:
        estado["Demanda"]=estado["Demanda"]*1.1
        estado["duracion_branding"]-=1
    if estado["EcommerceActivo"]==True and estado["duracion_ecommerce"]>0:
        estado["Demanda"]=estado["Demanda"]+5000
        estado["duracion_ecommerce"] -=1
    if estado["DemandaExtraTemporal"]==True:
        if estado["DuracionRestante->Temporal"]==2:
            estado["Demanda"]=estado["Demanda"]+300000
            estado["DuracionRestante->Temporal"]-=1
        elif estado["DuracionRestante->Temporal"]==1:
            estado["Demanda"]=estado["Demanda"]+150000
            estado["DuracionRestante->Temporal"]-=1
    if estado["duracion_6"]>0: # dudoso
        estado["Demanda"]=estado["Demanda"]-(estado["Demanda"]*estado["r_demanda"]/100)
    estado["Pedidos por atender"]=estado["Demanda"]
#3-------------------------------------
    if estado ["Caja disponible"] >= estado["Sueldos por pagar"]:
           estado["Caja disponible"]-=estado["Sueldos por pagar"]
    elif estado["Caja disponible"] < estado["Sueldos por pagar"]:
           estado["Deuda pendiente"]+=(estado["Sueldos por pagar"]-estado["Caja disponible"])*1.12
           estado["Caja disponible"]=0
#4----------------------------------------------
    estado["Sueldos por pagar"]=estado["Cantidad de empleados"]*estado["Costo por empleado"]
#5------------------------------------------------
    # carta 37
    if estado["indice_deudas(cambios)"]<=0:
        estado["indice_deudas(cambios)"]+=1
        estado["indice_deudas(cambios)"]+=1
    elif estado["indice_deudas(cambios)"]==2:
        estado["Cantidad de empleados"]+=1
        estado["indice_deudas(cambios)"]=0
    if estado["37"]==True or estado["18"]==True: # "contador_actual":{"antes_empleados":0,"antes_inventario":0,"antes_insumos":0},
        estado["Inventario"]-=(estado["contador actual"]["antes_inventario"])/2
        estado["Insumos disponibles"]+=(estado["contador actual"]["antes_insumos"]/2)
# carta 4
    if estado["perdida"]==True:
       estado["Inventario"]=0
# carta 13
    if 0<estado["carta 13"]<=3:
        if estado["Caja disponible"] >= estado["registro de ventas_precios"]:
            estado["Caja disponible"] -= sum(estado["registro de ventas_precios"])
        else:
            estado["Deuda pendiente"] += (sum(estado["registro de ventas_precios"]) - estado[
                "Caja disponible"]) * 1.12
            estado["Caja disponible"] = 0
# carta 38
    if estado["r_producir"]==2:
        estado["Inventario"]-=estado["contador_actual"]["antes_inventario"]
        estado["Insumos"]+=estado["contador_actual"]["antes_insumos"]
# carta 19
    if estado["t_pedidos"]!=0:
        estado["Pedidos por atender"]=round(estado["Pedidos por atender"]*2/3)
    if estado["Caja disponible"] >= estado["Multas e indemnizaciones"]:
        estado["Caja disponible"] -=estado["Multas e indemnizaciones"]
        estado["Multas e indemnizaciones"]=0
    else:
        estado["Deuda pendiente"] += (estado["Multas e indemnizaciones"] - estado["Caja disponible"]) * 1.12
        estado["Caja disponible"] = 0
#6-----------------------------------------------------
#no entiendo como usar
    if estado["TurnosProduccionExtra"]>0:
        estado["Inventario"]+=estado["contador_actual"]["antes_inventario"]
#7------------------------------------------------------
    if round(estado["Insumos"]*0.1)>estado["contador_actual"]["antes_insumos"]:
        estado["Insumos disponibles"]-=round(estado["Insumos"]*0.1)
    if not(estado["Prohibir Produccion"]==False and estado["r_producir"]==0 and estado["r_produccion"]==0 and estado["r_insumos"]==0 and estado["r_sigProduccion"]==0 and estado["p_ventas,produccion"]==0):
        estado["Insumos disponibles"] -= round(estado["Insumos disponibles"] * 0.1)
    if estado["EcommerceActivo"]==True:
        estado["Pedidos por atender"]+=5000
        if estado["Insumos disponibles"]>0:
            estado["Ventas"] += 2000
    if estado["TurnosProduccionExtra"]==0:
       estado["TurnosProduccionExtra"] = 0
    elif estado["TurnosProduccionExtra"]!=0:
       estado["TurnosProduccionExtra"] -= 1
    if estado["DemandaExtraTemporal"]==0:
       estado["DemandaExtraTemporal"] = 0
    elif estado["DemandaExtraTemporal"]!=0:
       estado["DemandaExtraTemporal"] -= 1
    if estado["EmpleadosTemporales"]==0:
       estado["EmpleadosTemporales"] = 0
    elif estado["EmpleadosTemporales"]!=0:
       estado["EmpleadosTemporales"]-=1
    estado["MejoraProceso"]= False
    estado["BrandingActivo"]= False
    estado["MantenimientoHecho"]=False
    estado["EcommerceActivo"]= False
    """
    
    7) Actualizacion de flags temporales y decremento de contadores
       - Reducir en 1 las variables contadoras. Por ejemplo:
         • ‘TurnosProduccionExtra’
         • ‘DemandaExtraTemporal’
         • ‘EmpleadosTemporales’
         • Duracion de ‘MejoraProceso’, ‘BrandingActivo’, ‘MantenimientoHecho’, etc.
       - Desactivar (poner a False o 0) cualquier flag cuyo contador llegue a cero
    """
    return estado