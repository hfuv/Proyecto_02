# cartas.py
#es muy necesario saber el orden de ejecucion
def aplicar_carta(numero, estado):
    if numero == 1:
        return estado
    elif numero == 2:
        if estado["Contador_mantenimiento"] == 0:
            if estado["Maquinas (total/activas/dañadas)"].split("/")[-2] >= 2:
                estado["Maquinas (total/activas/dañadas)"] = str(
                    estado["Maquinas (total/activas/dañadas)"].split("/")[0]) + "/" + str(
                    int(estado["Maquinas (total/activas/dañadas)"].split("/")[-2]) - 2) + "/" + str(
                    int(estado["Maquinas (total/activas/dañadas)"].split("/")[-1]) + 2)
            else:
                estado["Maquinas (total/activas/dañadas)"] = str(
                    estado["Maquinas (total/activas/dañadas)"].split("/")[0]) + "/" + str(0) + "/" + str((int(
                    estado["Maquinas (total/activas/dañadas)"].split("/")[-1]) + int(
                    estado["Maquinas (total/activas/dañadas)"].split("/")[-2])))

        return estado

    elif numero == 3:
        if estado["bloqueador_seguridad"] == 0:
            estado["r_insumos"] = 1
            estado["r_produccion"] = 2
            if int(estado["Reputacion del mercado"][-1]) >= 1:
                estado["Reputacion del mercado"] = "Nivel " + str(int(estado["Reputacion del mercado"][-1]) - 1)
            elif int(estado["Reputacion del mercado"][-1]) < 1:
                estado["Reputacion del mercado"] = "Nivel " + str(0)
        return estado

    elif numero == 4:
        estado["perdida"]=True
        return estado
    elif numero == 5:
        estado["Multas e indemnizaciones"]+=5000
        if int(estado["Reputacion del mercado"][-1])>=1:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-1)
        elif int(estado["Reputacion del mercado"][-1])<1:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        return estado
    elif numero == 6: # dudoso
        if int(estado["Reputacion del mercado"][-1])>=2:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-2)
        elif int(estado["Reputacion del mercado"][-1])<2:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        estado["r_demanda"]=50
        estado["duracion_6"]=2

        return estado

    elif numero == 7:
        estado["Insumos disponibles"]=round(estado["Insumos disponibles"]*0.7)
        return estado
    elif numero == 8:
        if estado["Contador_mantenimiento"] == 0:
            if estado["Maquinas (total/activas/dañadas)"].split("/")[-2] >= 1:
                estado["Maquinas (total/activas/dañadas)"] = str(
                    estado["Maquinas (total/activas/dañadas)"].split("/")[0]) + "/" + str(
                    int(estado["Maquinas (total/activas/dañadas)"].split("/")[-2]) - 1) + "/" + str(
                    int(estado["Maquinas (total/activas/dañadas)"].split("/")[-1]) + 1)
        if estado["bloqueador_clima"]==0:
            if estado["Cantidad de empleados"] >= 1:
                estado["Cantidad de empleados"] -= 1
        return estado
    elif numero == 9: # listo
        if estado["bloqueador_clima"] == 0:
            estado["r_sigProduccion"] = 3
            if int(estado["Reputacion del mercado"][-1]) >= 2:
                estado["Reputacion del mercado"] = "Nivel " + str(int(estado["Reputacion del mercado"][-1]) - 2)
            elif int(estado["Reputacion del mercado"][-1]) < 2:
                estado["Reputacion del mercado"] = "Nivel " + str(0)
        return estado
    elif numero == 10:
        if estado["contador_fondo_emergencia"] == 0:
            if estado["Caja disponible"] >= 5000:
                estado["Caja disponible"] -= 5000
            else:
                estado["Deuda pendiente"] += (5000 - estado["Caja disponible"]) * 1.12
                estado["Caja disponible"] = 0
            estado["Multas e indemnizaciones"] += 5000
            if int(estado["Reputacion del mercado"][-1]) >= 2:
                estado["Reputacion del mercado"] = "Nivel " + str(int(estado["Reputacion del mercado"][-1]) - 2)
            elif int(estado["Reputacion del mercado"][-1]) < 2:
                estado["Reputacion del mercado"] = "Nivel " + str(0)

        return estado

    elif numero == 11:
        estado["Multas e indemnizaciones"] += 5000
        if int(estado["Reputacion del mercado"].split()[-1])>=1:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-1)
        elif int(estado["Reputacion del mercado"][-1])<1:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        return estado
    elif numero == 12: # listo
        estado["R-12"]=50
        estado["R-12(duracion)"]=2
        return estado
    elif numero == 13:
        if estado["contador_fondo_emergencia"] ==0:
            if estado["Caja disponible"] >= 15000:
                estado["Caja disponible"] -= 15000
            else:
                estado["Deuda pendiente"] += (15000 - estado["Caja disponible"]) * 1.12
                estado["Caja disponible"] = 0
            if estado["Caja disponible"] >= estado["registro de ventas_precios"]:
                estado["Caja disponible"] -= sum(estado["registro de ventas_precios"])
            else:
                estado["Deuda pendiente"] += (sum(estado["registro de ventas_precios"]) - estado[
                    "Caja disponible"]) * 1.12
                estado["Caja disponible"] = 0
            estado["carta 13"]=3
        return estado

    elif numero == 14:
        estado["p_insumosImportados"]=4
        return estado

    elif numero == 15:
        estado["p_compras-nacionales"]=5
        return estado

    elif numero == 16:
        if estado["contador_fondo_emergencia"] ==0:

            if estado["Caja disponible"] >= 8000:
                estado["Caja disponible"] -= 8000
            else:
                estado["Deuda pendiente"] += 8000 - estado["Caja disponible"]
                estado["Caja disponible"] = 0

        return estado

    elif numero == 17:
        if int(estado["Reputacion del mercado"][-1])>=2:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-2)
        elif int(estado["Reputacion del mercado"][-1])<2:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        return estado

    elif numero == 18: # listo
        estado["18"] = True
        estado["d_produccion"]=3
        return estado

    elif numero == 19: # listo
        if estado["bloqueador_campania"] ==0 or estado["duracion_demanda"] ==0:
           estado["t_pedidos"]=1
        return estado

    elif numero == 20:
        if int(estado["Reputacion del mercado"][-1])>=3:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-3)
        elif int(estado["Reputacion del mercado"][-1])<3:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        return estado
    elif numero == 21: # listo
        estado["r_ronda-sig-producciojn"]=2
        return estado

    elif numero == 22: # listo
        estado["Multas e indemnizaciones"] += 30000
        estado["r_produccion"]=1
        return estado

    elif numero == 23:
        if int(estado["Reputacion del mercado"][-1])>=2:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-2)
        elif int(estado["Reputacion del mercado"][-1])<2:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        return estado

    elif numero == 24: # listo
        estado["r_venta"]=2
        return estado

    elif numero == 25:
        estado["Multas e indemnizaciones"]+=15000
        return estado
    elif numero == 26: #listo
        if estado["competidores_nuevos"] ==0: #
            estado["r_venta40%"] = True
            if estado["Caja disponible"] >= 5000:
                estado["Caja disponible"] -= 5000
            else:
                estado["Deuda pendiente"] += (5000 - estado["Caja disponible"]) * 1.12
                estado["Caja disponible"] = 0
            estado["duracion_almacen"] = 3
            estado["carta 26"]=40
        return estado

    elif numero == 27:
        if estado["bloqueador_seguridad"] ==0 or estado["contador_fondo_emergencia"] ==0:
            if estado["Caja disponible"] >= 10000:
                estado["Caja disponible"] -= 10000
            else:
                estado["Caja disponible"] = 0

        return estado
    # costos
    elif numero == 28: # listo
        estado["aumento_por 10%"]=5
        return estado

    elif numero == 29: # listo
        if int(estado["Reputacion del mercado"][-1])>=2:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-2)
        elif int(estado["Reputacion del mercado"][-1])<2:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        estado["carta29"]= 75

        return estado

    elif numero == 30: # listo
        estado["p_ventas,produccion"]=3
        if estado["Caja disponible"] >= 10000:
            estado["Caja disponible"] -= 10000
        else:
            estado["Deuda pendiente"] += (10000 - estado["Caja disponible"])*1.12
            estado["Caja disponible"] = 0
        return estado

    elif numero == 31: # listo
        estado["p_venta"]=1
        if estado["Caja disponible"] >= 10000:
            estado["Caja disponible"] -= 10000
        else:
            estado["Deuda pendiente"] += (10000 - estado["Caja disponible"])*1.12
            estado["Caja disponible"] = 0

        return estado

    elif numero == 32:
        if estado["contador_fondo_emergencia"] == 0:
            if estado["Caja disponible"] >= 7000:
                estado["Caja disponible"] -= 7000
            else:
                estado["Caja disponible"] = 0

        return estado

    elif numero == 33: # listo
        estado["R_ventas"]=1
        if int(estado["Reputacion del mercado"][-1])>=2:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-2)
        elif int(estado["Reputacion del mercado"][-1])<2:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        return estado

    elif numero == 34: # listo
        estado["carta34"]=2
        estado["carta34(valor)"]=25
        if int(estado["Reputacion del mercado"][-1])>=2:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-2)
        else:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        return estado

    elif numero == 35: # listo
        estado["Multas e indemnizaciones"] += 30000
        if int(estado["Reputacion del mercado"][-1])>=3:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-3)
        else:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        return estado
    elif numero == 36: # listo
        if estado["contador_fondo_emergencia"] ==0:
            if estado["Caja disponible"] >= 15000:
                estado["Caja disponible"] -= 15000
            else:
                estado["Deuda pendiente"] += 15000 - estado["Caja disponible"]
                estado["Caja disponible"] = 0
            if int(estado["Reputacion del mercado"][-1]) >= 2:
                estado["Reputacion del mercado"] = "Nivel " + str(int(estado["Reputacion del mercado"][-1]) - 2)
            else:
                estado["Reputacion del mercado"] = "Nivel " + str(0)

            estado["Deuda pendiente"] += 15000
        return estado

    elif numero == 37 : # listo solo verificar
        s=['a','b','c']
        if estado["bloqueador_seguridad"]== 0:
            estado["Multas e indemnizaciones"] += 4000
            estado["carta37"] = 2
            estado["Registro_cambios37(tiempo)"][s[estado["indice_deudas(cambios)"]]]=2
            estado["Registro_cambios37"][s[estado["indice_deudas(cambios)"]]]=1
            estado["Cantidad de empleados"]-=1
            estado["37"]=True
        return estado

    elif numero == 38: # listo
        estado["Inventario"],estado["Insumos Disponibles"]=0,0
        estado["r_producir"]=2
        return estado

    elif numero == 39:
        estado["r_produccion"]=1
        return estado
    elif numero == 40: # listo
        estado["r_contrato-empleados"]=5
        return estado
    else:
        return estado