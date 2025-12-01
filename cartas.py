# cartas.py
#es muy necesario saber el orden de ejecucion
def aplicar_carta(numero, estado):
    if numero == 1:
        return estado
    elif numero == 2:
        if estado["Contador_mantenimiento"] == 0:
            if estado["Maquinas (total/activas/dañadas)"].split()[-2] >= 2:
                estado["Maquinas (total/activas/dañadas)"] = str(
                    estado["Maquinas (total/activas/dañadas)"].split()[0]) + "/" + str(
                    int(estado["Maquinas (total/activas/dañadas)"].split()[-2]) - 2) + "/" + str(
                    int(estado["Maquinas (total/activas/dañadas)"].split()[-1]) + 2)
            else:
                estado["Maquinas (total/activas/dañadas)"] = str(
                    estado["Maquinas (total/activas/dañadas)"].split()[0]) + "/" + str(0) + "/" + str((int(
                    estado["Maquinas (total/activas/dañadas)"].split()[-1]) + int(
                    estado["Maquinas (total/activas/dañadas)"].split()[-2])))

        return estado

    # Carta 3: Virus informatico:
    # Se pierde visibilidad del inventario y de los insumos por 1 turno
    # No puedes producir porque no sabes cuantos insumos hay.
    # No puedes vender porque no sabes cuanto invnetario hay.
    # Los clientes se enteraron y bajo la reputacion 1 nivel
    # Duración: 2 turnos
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
    #   - Tuvimos que reponer mercaderia equivalente a la demanda actual (elimina el inventario equivalente a la demanda)
    #   - Luego, la demanda actual se reduce en 50%
    # Duración: 2 turnos
    elif numero == 6:
        if int(estado["Reputacion del mercado"][-1])>=2:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-2)
        elif int(estado["Reputacion del mercado"][-1])<2:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        estado["r_demanda"]+=50
        estado["duracion_6"]=2

        return estado

    elif numero == 7:
        estado["Insumos disponibles"]=round(estado["Insumos disponibles"]*0.7)
        return estado
    elif numero == 8:
        if estado["Contador_mantenimiento"] == 0:
            if estado["Maquinas (total/activas/dañadas)"].split()[-2] >= 1:
                estado["Maquinas (total/activas/dañadas)"] = str(
                    estado["Maquinas (total/activas/dañadas)"].split()[0]) + "/" + str(
                    int(estado["Maquinas (total/activas/dañadas)"].split()[-2]) - 1) + "/" + str(
                    int(estado["Maquinas (total/activas/dañadas)"].split()[-1]) + 1)
        if estado["bloqueador_clima"]==0:
            if estado["Cantidad de empleados"] >= 1:
                estado["Cantidad de empleados"] -= 1
        return estado
    elif numero == 9:
        if estado["bloqueador_clima"] == 0:
            estado["r_sigProduccion"] = 2
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
        if int(estado["Reputacion del mercado"][-1])>=1:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-1)
        elif int(estado["Reputacion del mercado"][-1])<1:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        return estado

    # Carta 12: Boicot de clientes # reversion de acciones
    #   - Ventas de esta semana reducidas al 50%:
    # Duración: 2 turnos
    elif numero == 12:
        estado["R-12"]=2
        return estado

    # Carta 13: Error de etiquetado // reversion de acciones
    #   - Devuelven todas las unidades vendidas el turno actual y el turno anterior
    #     • Debes devolver el dinero obtenido por dichas ventas
    #     • Además, gastas 15,000 soles en la logística inversa
    # Duración: 3 turnos
    elif numero == 13: # falta solucionar para que se ejecute en estado
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
            return estado

    elif numero == 14:
        estado["p_insumosImportados"]=3
        return estado

    elif numero == 15:
        estado["p_compras-nacionales"]=4
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

    elif numero == 18:
        estado["d_produccion"]=3
        return estado

    elif numero == 19:
        if estado["bloqueador_campania"] ==0 or estado["duracion_demanda"] ==0:
           estado["t_pedidos"]=1
        return estado

    elif numero == 20:
        if int(estado["Reputacion del mercado"][-1])>=3:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-3)
        elif int(estado["Reputacion del mercado"][-1])<3:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        return estado
    elif numero == 21:
        estado["r_ronda-sig-producciojn"]=2
        return estado

    elif numero == 22:
        estado["Multas e indemnizaciones"] += 30000
        estado["r_produccion"]=1
        return estado

    elif numero == 23:
        if int(estado["Reputacion del mercado"][-1])>=2:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-2)
        elif int(estado["Reputacion del mercado"][-1])<2:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        return estado

    elif numero == 24: # falta
        estado["r_venta"]=2
        return estado

    elif numero == 25:
        estado["Multas e indemnizaciones"]+=15000
        return estado

    # Carta 26: Nuevo competidor agresivo // reversion de acciones
    #   - Ventas −40%:
    #   - Debemos pagar 5,000 por almacén
    # Duración: 3 turnos

    elif numero == 26:
        if estado["competidores_nuevos"] ==0:
            estado["r_venta40%"] = True
            if estado["Caja disponible"] >= 5000:
                estado["Caja disponible"] -= 5000
            else:
                estado["Deuda pendiente"] += (5000 - estado["Caja disponible"]) * 1.12
                estado["Caja disponible"] = 0
            estado["duracion_almacen"] = 3
        return estado

    elif numero == 27:
        if estado["bloqueador_seguridad"] ==0 or estado["contador_fondo_emergencia"] ==0:
            if estado["Caja disponible"] >= 10000:
                estado["Caja disponible"] -= 10000
            else:
                estado["Caja disponible"] = 0

        return estado
    # costos
    elif numero == 28:
        estado["aumento_por 10%"]=5
        return estado

    elif numero == 29:
        if int(estado["Reputacion del mercado"][-1])>=2:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-2)
        elif int(estado["Reputacion del mercado"][-1])<2:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        estado["d_ventas-75%"]=1

        return estado

    elif numero == 30:
        estado["p_ventas,produccion"]=3
        if estado["Caja disponible"] >= 10000:
            estado["Caja disponible"] -= 10000
        else:
            estado["Deuda pendiente"] += (10000 - estado["Caja disponible"])*1.12
            estado["Caja disponible"] = 0
        return estado

    elif numero == 31:
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

    elif numero == 33:
        estado["R_ventas"]=1
        if int(estado["Reputacion del mercado"][-1])>=2:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-2)
        elif int(estado["Reputacion del mercado"][-1])<2:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        return estado

    elif numero == 34:
        estado["carta34"]=2
        if int(estado["Reputacion del mercado"][-1])>=2:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-2)
        else:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        return estado

    elif numero == 35:
        estado["Multas e indemnizaciones"] += 30000
        if int(estado["Reputacion del mercado"][-1])>=3:
            estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-3)
        else:
            estado["Reputacion del mercado"]="Nivel "+str(0)

        return estado
    elif numero == 36:
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

    elif numero == 37: # aplicacion de 50%
        s=['a','b','c']
        if estado["bloqueador_seguridad"]== 0:
            estado["Multas e indemnizaciones"] += 4000
            estado["carta37"] = 2  # Produccion −50% este mes#   - Temporalmente -1 trabajador por 2 turnos
            estado["Registro_cambios37(tiempo)"][s[estado["indice_deudas(cambios)"]]]=2
            estado["Registro_cambios37"][s[estado["indice_deudas(cambios)"]]]=1
            estado["Cantidad de empleados"]-=1
            estado["37"]=True
        return estado

    elif numero == 38:
        estado["Inventario"],estado["Insumos Disponibles"]=0,0
        estado["r_producir"]=2
        return estado

    elif numero == 39:
        estado["r_produccion"]=1
        return estado
    elif numero == 40:
        estado["r_contrato-empleados"]=5
        return estado
    else:
        return estado