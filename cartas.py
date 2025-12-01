# cartas.py
#es muy necesario saber el orden de ejecucion
def aplicar_carta(numero, estado):
    # Carta 1: Dia tranquilo:
    if numero == 1:
        return estado

    # Carta 2: Falla critica en maquinaria:
    elif numero == 2:
        if estado["Maquinas (total/activas/dañadas)"].split()[-2]>=2:
            estado["Maquinas (total/activas/dañadas)"]=str(estado["Maquinas (total/activas/dañadas)"].split()[0])+"/"+str(int(estado["Maquinas (total/activas/dañadas)"].split()[-2])-2)+"/"+str(int(estado["Maquinas (total/activas/dañadas)"].split()[-1])+2)
        else:
            estado["Maquinas (total/activas/dañadas)"] = str(
                estado["Maquinas (total/activas/dañadas)"].split()[0]) + "/" + str(0) + "/" + str((int(estado["Maquinas (total/activas/dañadas)"].split()[-1]) +int(estado["Maquinas (total/activas/dañadas)"].split()[-2])) )
        return estado

    # Carta 3: Virus informatico:
    # Se pierde visibilidad del inventario y de los insumos por 1 turno
    # No puedes producir porque no sabes cuantos insumos hay.
    # No puedes vender porque no sabes cuanto invnetario hay.
    # Los clientes se enteraron y bajo la reputacion 1 nivel
    # Duración: 2 turnos
    elif numero == 3:
        estado["r_produccion"]=2
        estado["Reputacion del mercado"] = "Nivel " + str(int(estado["Reputacion del mercado"].split[-1]) - 1)  # creo que se deberia usar el temporizador de 2

        return estado

    # Carta 4: Incendio en almacen
    #   - Se pierde el inventario total (al final del mes, despues de haber producido y vendido)
    elif numero == 4:
        estado["perdida"]=True
        return estado

    # Carta 5: Auditoria desfavorable
    elif numero == 5:
        estado["Multas e indemnizaciones"]+=5000
        estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"].split[-1])-1)
        return estado

    # Carta 6: Producto retirado del mercado /- no entiendo
    #   - Reputacion se reduce 2 niveles.
    #   - Tuvimos que reponer mercaderia equivalente a la demanda actual (elimina el inventario equivalente a la demanda)
    #   - Luego, la demanda actual se reduce en 50%
    # Duración: 2 turnos
    elif numero == 6:
        estado["Reputacion del mercado"] = "Nivel " + str(int(estado["Reputacion del mercado"].split[-1]) - 2)
        estado["uso_demanda"]=True # demanda de se debe calcular primero
        estado["r_demanda"]-=50

        return estado

    # Carta 7: Robo de insumos
    #   - Pierdes 30% de insumos disponibles.
    elif numero == 7:
        estado["Insumos disponibles"]-=round(estado["Insumos disponibles"]*0.7)
        return estado
    # Carta 8: Fuga de talento clave
    #   - Tras la fuga de talento, operarios sin experiencia manipularon y dañaron una maquina
    #   - Pierdes 1 maquina activa (pasa a dañada).
    #   - Pierdes 1 empleado.
    elif numero == 8:
        if estado["Maquinas (total/activas/dañadas)"].split()[-2]>=1:
            estado["Maquinas (total/activas/dañadas)"]=str(estado["Maquinas (total/activas/dañadas)"].split()[0])+"/"+str(int(estado["Maquinas (total/activas/dañadas)"].split()[-2])-1)+"/"+str(int(estado["Maquinas (total/activas/dañadas)"].split()[-1])+1)
        return estado

    # Carta 9: Huelga por ambiente laboral
    #   - La proxima ronda no se produce.
    #   - Los clientes se enteran de la huelga y baja la reputación 3 niveles
    # Duración: 2 turnos
    elif numero == 9:
        estado["r_sigProduccion"]=True
        return estado

    # Carta 10: Hacker secuestra datos
    #   - Pierdes 5,000 de caja (si no alcanza, la diferencia se convierte en deuda al 12%)
    #   - Reputacion baja 2 niveles
    #   - Te aplican una multa de 5,000 soles por malas practicas de seguridad de la informacion
    elif numero == 10:
        if estado["Caja disponible"]>=5000:
            estado["Caja disponible"] -= 5000
        else :
            estado["Deuda pendiente"]+=(5000-estado["Caja disponible"])*1.12
            estado["Caja disponible"] = 0
        estado["Multas e indemnizaciones"] += 5000
        estado["Reputacion del mercado"] = "Nivel " + str(int(estado["Reputacion del mercado"].split[-1]) - 2)
        return estado

 # Carta 11: Multa ambiental
    #   - Aumentan “Multas e indemnizaciones” en +5000.
    #   - Reputacion del mercado −1 nivel.
    elif numero == 11:
        estado["Multas e indemnizaciones"] += 5000
        estado["Reputacion del mercado"] = "Nivel " + str(int(estado["Reputacion del mercado"].split[-1]) - 1)
        return estado

    # Carta 12: Boicot de clientes # reversion de acciones
    #   - Ventas de esta semana reducidas al 50%:
    # Duración: 2 turnos
    elif numero == 12:
        estado["r_ventas"]=50
        return estado

    # Carta 13: Error de etiquetado // reversion de acciones
    #   - Devuelven todas las unidades vendidas el turno actual y el turno anterior
    #     • Debes devolver el dinero obtenido por dichas ventas
    #     • Además, gastas 15,000 soles en la logística inversa
    # Duración: 3 turnos
    elif numero == 13:
        return estado

    # Carta 14: Retraso en importacion
    #   - Prohibir insumos importados las siguientes 3 rondas:
    elif numero == 14:
        estado["p_insumosIm"]=3
        return estado

    # Carta 15: Proveedores en huelga
    #   - Prohibir compras nacionales las siguientes 4 rondas:
    elif numero == 15:
        estado["p_compras-int"]=4
        return estado

    # Carta 16: Estafa financiera
    #   - Pierdes 8,000 de caja
    elif numero == 16:
        if estado["Caja disponible"] >= 8000:
            estado["Caja disponible"] -= 8000
        else:
            estado["Deuda pendiente"] += 8000 - estado["Caja disponible"]
            estado["Caja disponible"] = 0

        return estado

    # Carta 17: Rumor de corrupcion
    #   - Reputacion del mercado −2 niveles.
    elif numero == 17:
        estado["Reputacion del mercado"] = "Nivel " + str(int(estado["Reputacion del mercado"].split[-1]) - 2)

        return estado

    # Carta 18: Plaga en planta // reversion de acciones
    #   - Produccion a la mitad este turno
    # Duración: 3 turnos
    elif numero == 18:
        estado["d_produccion"]=True
        return estado

    # Carta 19: Cliente corproativo VIP cancela pedido
    #   - Peirdes un tercio de los “Pedidos por atender”.
    elif numero == 19:
        estado["t_pedidos"]=True
        return estado

    # Carta 20: Producto defectuoso viral
    #   - Reputacion del mercado −3 niveles.
    elif numero == 20:
        estado["Reputacion del mercado"] = "Nivel " + str(int(estado["Reputacion del mercado"].split[-1]) - 3)
        return estado

    # Carta 21: Mal clima: inundacion
    #   - No se produce la siguiente ronda:
    # Duración: 2 turnos
    elif numero == 21:
        estado["r_ronda-sig"]=3
        return estado

    # Carta 22: Licencia vencida
    #   - Multas +30,000.
    #   - Prohibir produccion la siguiente ronda.
    elif numero == 22:
        estado["r_produccion"]=True
        return estado

    # Carta 23: Fake news en redes
    #   - Reputacion del mercado −2 niveles.
    elif numero == 23:
        estado["Reputacion del mercado"] = "Nivel " + str(int(estado["Reputacion del mercado"].split[-1]) - 2)
        return estado

    # Carta 24: Bloqueo logistico // reversion de acciones
    #   - No se venden unidades
    # Duración: 2 turnos
    elif numero == 24:
        estado["r_venta"]=True
        return estado

    # Carta 25: Demanda judicial
    #   - Multas e indemnizaciones +15,000.
    elif numero == 25:
        estado["Multas e indemnizaciones"]+=15000
        return estado

    # Carta 26: Nuevo competidor agresivo // reversion de acciones
    #   - Ventas −40%:
    #   - Debemos pagar 5,000 por almacén
    # Duración: 3 turnos

    elif numero == 26: # problema al definir ventas ya que no es una variable original
        estado["r_venta40%"]=True
        return estado

    # Carta 27: Robo interno
    #   - Caja se reduce en 10,000.
    elif numero == 27: #que pasa si tienes menos
        if estado["Caja disponible"] >= 10000:
            estado["Caja disponible"] -= 10000
        else:
            estado["Deuda pendiente"] += 10000 - estado["Caja disponible"]
            estado["Caja disponible"] = 0

        return estado

    # Carta 28: Crisis economica
    #   - Todos los costos +10% por los siguientes 5 turnos:
    elif numero == 28:
        estado["aumento"]=True
        return estado

    # Carta 29: Fuga de datos // reversion de acciones
    #   - Reputacion del mercado −2 nivel.
    #   - Ventas de este mes se reducen en un 75%
    elif numero == 29:
        estado["r_75%"]=True
        return estado

    # Carta 30: Huelga nacional // reversion de acciones
    #   - No ventas ni produccion
    #   - Debemos pagar 10,000 por almacén
    # Duración: 3 turnos
    elif numero == 30
        estado["p_ventas,produccion"]=True
        return estado

    # Carta 31: Rechazo de exportacion // reversion de acciones
    #   - Inventario acumulado (no se vende este mes).
    #   - Debemos pagar 10,000 por almacén
    elif numero == 31:
        estado["p_venta"]=True
        return estado

    # Carta 32: Error contable # reversion de acciones
    #   - Caja −7000.
    elif numero == 32:
        if estado["Caja disponible"] >= 7000:
            estado["Caja disponible"] -= 7000
        else:
            estado["Deuda pendiente"] += 7000 - estado["Caja disponible"]
            estado["Caja disponible"] = 0

        return estado

    # Carta 33: Error en codigo de barras // reversion de acciones
    #   - No se venden productos este mes:
    #   - reputación baja 2 niveles
    elif numero == 33:
        # if int(estado["Reputacion del mercado"][-1])>=2: si no puede ser negativo
        estado["Reputacion del mercado"]="Nivel "+str(int(estado["Reputacion del mercado"][-1])-2)
        # elif int(estado["Reputacion del mercado"][-1])<2:
        #estado["Reputacion del mercado"]="Nivel "+str(0)

        return estado

    # Carta 34: Mal diseño del empaque // reversion de las acciones
    #   - Ventas −25%
    #   - reputación baja 2 niveles
    # Duración: 2 turnos
    elif numero == 34:
        estado["carta34"]==2
        return estado

    # Carta 35: Cliente se intoxica
    #   - Reputacion del mercado −3 niveles.
    #   - Multas +30,000.
    elif numero == 35:
        return estado

    # Carta 36: Fraude en prestamo
    #   - Caja −15,000.
    #   - Deuda pendiente +15,000.
    #   - reputación baja 2 niveles
    elif numero == 36:
        if estado["Caja disponible"] >= 15000:
            estado["Caja disponible"] -= 15000
        else:
            estado["Deuda pendiente"] += 15000 - estado["Caja disponible"]
            estado["Caja disponible"] = 0
        estado["Deuda pendiente"] += 15000
        estado["Reputacion del mercado"] = "Nivel " + str(int(estado["Reputacion del mercado"][-1]) - 2)

        return estado

    # Carta 37: Trabajador se accidenta // reversion de las acciones
    #   - Multas +4000.
    #   - Produccion −50% este mes
    #   - Temporalmente -1 trabajador por 2 turnos
    elif numero == 37:
        estado["Multas e indemnizaciones"]+=4000
        estado["d_trabajador"]=2
        return estado

    # Carta 38: Derrame quimico // reversion de las acciones
    #   - Inventario e Insumos = 0
    #   - No puedes producir durante este mes y el siguiente
    elif numero == 38:
        estado["Inventario"],estado["Insumos Disponibles"]=0,0
        estado["r_producir"]=2
        return estado

    # Carta 39: Virus contagioso // necesario una reversion de las acciones
    #   Todos los empleados se quedaron en su casa por un mes
    #   No se vende ni se produce
    elif numero == 39:
        estado["r_produccion"]=True
        return estado

    # Carta 40: Hiring Freeze
    #   No puedes contratar empleados nuevos
    # Duración: 5 turnos
    elif numero == 40:
        estado["r_contrato"]=5
        return estado
    else:
        return estado
