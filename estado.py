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
        "venta_excedente": 0,
        "Contador_IP":0,
        "aumento_venta":0,
        "contador_co-branding":0,
        "duracion_branding":0,
        "bloqueador_campania":0,
        "lanzar_campania":0,
        "Contador_mantenimiento":0,
        "bloqueador_seguridad":0,
        "r_produccion":0,
        "r_insumos":0,
        "perdida":False,
        "duracion_6":0,
        "r_demanda":0,
        "r_sigProduccion":0,
        "R-12(duracion)":0,
        "R-12":0,
        "carta 13":0,
        "p_insumosImportados":0,
        "p_compras-nacionales":0,
        "d_produccion":0,
        "18":False,
        "t_pedidos":0,
        "r_ronda-sig-producciojn":0,
        "r_venta":0,
        "r_venta40%":False,
        "duracion_almacen":0,
        "carta 26":0,
        "carta29":0,
        "p_ventas,produccion":0,
        "p_venta":0,
        "R_ventas":0,
        "carta34(valor)":0,
        "carta34":0,
        "carta37":0,
        "37":False,
        "r_producir":0,
        "r_contrato-empleados":0,
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
    if estado["contador_co-branding"]>0 and estado["Inventario"] > estado["Pedidos por atender"]*1.2:
        estado["Pedidos por atender"]=round(estado["Pedidos por atender"]*1.2)
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
        if estado["contador_co-branding"]==2:
            estado["Demanda"]=estado["Demanda"]+300000
            estado["contador_co-branding"]-=1
        elif estado["contador_co-branding"]==1:
            estado["Demanda"]=estado["Demanda"]+150000
            estado["contador_co-branding"]-=1
    if estado["Contador_IP"] >0:
        estado["Contador_IP"]-=1
        estado["Demanda"] = estado["Demanda"]*1.5
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
        if estado["Caja disponible"] >= sum(estado["registro de ventas_precios"]):
            estado["Caja disponible"] -= sum(estado["registro de ventas_precios"])
        else:
            estado["Deuda pendiente"] += (sum(estado["registro de ventas_precios"]) - estado[
                "Caja disponible"]) * 1.12
            estado["Caja disponible"] = 0
# carta 38
    if estado["r_producir"]==2:
        estado["Inventario"], estado["Insumos Disponibles"] = 0, 0
        """estado["Inventario"]-=estado["contador_actual"]["antes_inventario"]
        estado["Insumos"]+=estado["contador_actual"]["antes_insumos"]"""
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
    if round(estado["Insumos disponibles"]*0.1)>estado["contador_actual"]["antes_insumos"]:
        estado["Insumos disponibles"]-=round(estado["Insumos disponibles"]*0.1)
    if estado["Prohibir Produccion"]==False and estado["r_producir"]==0 and estado["r_produccion"]==0 and estado["r_insumos"]==0 and estado["r_sigProduccion"]==0 and estado["p_ventas,produccion"]==0:
        estado["Insumos disponibles"] -= round(estado["Insumos disponibles"] * 0.1)
    if estado["EcommerceActivo"]==True:
        estado["Pedidos por atender"]+=5000
        if estado["Insumos disponibles"]>0:
            estado["Demanda"] += 2000
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
    if estado["contador_fondo_emergencia"]>0:
        estado["contador_fondo_emergencia"]-=1
        estado["Fondo emergencia"] = False
    if estado["venta_excedente"] > 0:
        estado["venta_excedente"] -= 1
    if estado["contador_co-branding"]>0:
        estado["contador_co-branding"]-=1
    elif estado["contador_co-branding"]==0:
        estado["aumento_venta"]=0
    if estado["duracion_ecommerce"] >0:
        estado["duracion_ecommerce"]-=1
    if estado["duracion_demanda"]>0:
        estado["duracion_demanda"]-=1
    if estado["competidores_nuevos"] :
        estado["competidores_nuevos"]-=1
    if estado["duracion_branding"]>0:
        estado["duracion_branding"]-=1
    elif estado["duracion_branding"]==0:
        estado["BrandingActivo"] = False
    if estado["lanzar_campania"]>0:
        estado["lanzar_campania"]-=1
    if estado["bloqueador_campania"]>0:
        estado["bloqueador_campania"]-=1
    if estado["bloqueador_seguridad"]>0:
        estado["bloqueador_seguridad"]-=1
    if estado["bloqueador_clima"]>0:
        estado["bloqueador_clima"]-=1
    if estado["IncentivosActivos"]>0:
        estado["IncentivosActivos"]-=1
    if estado["Contador_mantenimiento"]>0:
        estado["Contador_mantenimiento"]-=1
    elif estado["Contador_mantenimiento"]==0:
        estado["MantenimientoHecho"]=False
    if estado["TurnosProduccionExtra"]>0:
        estado["TurnosProduccionExtra"]-=1
    if estado["r_produccion"]>0:
        estado["r_produccion"]-=1
    if estado["r_insumos"]>0:
        estado["r_insumos"]-=1
    if estado["perdida"] :
        estado["perdida"]=False
        estado["Inventario"]=0
    if estado["duracion_6"]>0:
        estado["duracion_6"]-=1
    elif estado["duracion_6"]==0:
        estado["r_demanda"] =0
    if estado["r_sigProduccion"] >0:
        estado["r_sigProduccion"]-=1
    if estado["R-12(duracion)"]>0:
        estado["R-12(duracion)"]-=1
    elif estado["R-12(duracion)"]==0:
        estado["R-12"] = 0
    if estado["carta 13"]>0:
        estado["carta 13"]-=1
    if estado["p_insumosImportados"]>0:
        estado["p_insumosImportados"]-=1
    if estado["p_compras-nacionales"]>0:
        estado["p_compras-nacionales"]-=1
    if estado["d_produccion"]>0:
        estado["d_produccion"]-=1
    elif estado["d_produccion"]==0:
        estado["18"] = False
    if estado["r_venta"]>0:
        estado["r_venta"]-=1
    if estado["r_produccion"]>0:
        estado["r_produccion"]-=1
    if estado["r_ronda-sig-producciojn"]>0:
        estado["r_ronda-sig-producciojn"]-=1
    if estado["t_pedidos"]>0:
        estado["t_pedidos"]-=1
    if estado["duracion_almacen"]>0:
        estado["duracion_almacen"]-=1
    elif estado["duracion_almacen"]==0:
        estado["r_venta40%"] = False
        estado["carta 26"] = 0
    if estado["aumento_por 10%"]>0:
        estado["aumento_por 10%"]-=1
    estado["carta29"]=0
    if estado["p_ventas,produccion"]>0:
        estado["p_ventas,produccion"]-=1
    if estado["p_venta"]>0:
        estado["p_venta"]-=1
    if estado["R_ventas"]>0:
        estado["R_ventas"]-=1
    if estado["carta34"]>0:
        estado["carta34"]-=1
    elif estado["carta34"]==0:
        estado["carta34(valor)"]=0
    if estado["carta37"]>0:
        estado["carta37"]-=1
    elif estado["carta37"]==0:
        estado["37"]=False
    if estado["r_producir"]>0:
        estado["r_producir"]-=1
    if estado["r_produccion"]>0:
        estado["r_produccion"]-=1
    if estado["r_contrato-empleados"]>0:
        estado["r_contrato-empleados"]-=1
    return estado