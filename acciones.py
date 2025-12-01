# acciones.py

# ---------------- Produccion ----------------

def produccion_producir(estado):
    f=1
    if estado["Cantidad de empleados"]>4:
        f=estado["Cantidad de empleados"]-4
    if estado["Prohibir Produccion"]==False:
        for a in range(1,int(estado["Maquinas (total/activas/dañadas)"].split("/")[-2])+1):
            if estado["Insumos disponibles"]>=40000:
                estado["Insumos disponibles"]-=40000*f*0.1
                estado["Inventario"]+=2000
            else:
                break
        estado["TurnosProduccionExtra"]=2

    """
    - Por cada empleado adicional contratado, la produccion aumenta en 10%, sin gastar insumos.
        • Esto se debe a que los empelados introducen eficiencias en el proceso productivo
    """
    return estado

def produccion_pedido_encargo(estado):
    if estado["Prohibir Produccion"] == False:
        for a in range(1, int(estado["Maquinas (total/activas/dañadas)"].split("/")[-2]) + 1):
            if estado["Insumos disponibles"] >= 10000:
                estado["Insumos disponibles"] -= 10000
                estado["Caja disponible"] += 50000
            else:
                break
    return estado

def produccion_mejorar_proceso(estado): # maquinas
    if estado["mejora_proceso"]==1:
       estado["mejora_proceso"]=0
    estado["mejora_proceso"]+=5

    return estado

def produccion_mantenimiento_maquinaria(estado):
    estado["Maquinas (total/activas/dañadas)"]=str(int(estado["Maquinas (total/activas/dañadas)"].split("/")[-3]))+"/"+str(int(estado["Maquinas (total/activas/dañadas)"].split("/")[-2])+int(estado["Maquinas (total/activas/dañadas)"].split("/")[-1]))+"/"+"0"
    estado["MantenimientoHecho"]=True
    estado["Contador_mantenimiento"]=3
    return estado

def produccion_comprar_nueva_maquina(estado):
    if estado["Caja disponible"]>10000:
        estado["Caja disponible"]-=10000
    elif estado["Caja disponible"]<=10000:
        estado["Caja disponible"] =0
        estado["Deuda pendiente"]+=11200
    estado["Maquinas (total/activas/dañadas)"] = str(int(estado["Maquinas (total/activas/dañadas)"].split("/")[-3]) + 1) + "/" + str(int(estado["Maquinas (total/activas/dañadas)"].split("/")[-2]) + 1) +"/"+ str(estado["Maquinas (total/activas/dañadas)"].split("/")[-1])
    return estado

def produccion_no_hacer_nada(estado):
    return estado

# ---------------- Recursos Humanos ----------------

def rh_contratar_personal_permanente(estado):
    estado["Cantidad de empleados"] += 1
    estado["Sueldos por pagar"] += 4000
    return estado

def rh_contratar_personal_temporal(estado):
    if estado["Caja disponible"] > 10000:
        estado["Caja disponible"] -= 10000
    elif estado["Caja disponible"] <= 10000:
        estado["Caja disponible"] = 0
        estado["Deuda pendiente"] += 11200
    # falta los empleados temporales aumento de 4
    estado["Contador_empleadosTemp"]=1
    return estado

def rh_implementar_incentivos(estado):
    if estado["Caja disponible"] >= 5000:
        estado["Caja disponible"] -= 5000
    elif estado["Caja disponible"] < 5000:
        estado["Deuda pendiente"] += (5000 - estado["Caja disponible"]) * 1.12
        estado["Caja disponible"] = 0
    estado["IncentivosActivos"]=5
    """
    3. Implementar incentivos:
      el inventario producido por 5 turnos se multiplique por 1.2 (20 % extra).
    """
    return estado

def rh_medicion_clima(estado):
    estado["bloqueador_clima"]=5
    return estado

def rh_capacitar_seguridad(estado):
    estado["bloqueador_seguridad"]=3
    return estado

def rh_subir_sueldos(estado):
    if estado["Subida de sueldo"]==0:
        estado["Costo por empleado"]=estado["Costo por empleado"]*1.1
    elif estado["Subida de sueldo"]==1:
        estado["Costo por empleado"]=estado["Costo por empleado"]*1.07
    elif estado["Subida de sueldo"]==2:
        estado["Costo por empleado"]=estado["Costo por empleado"]*1.04
    elif estado["Subida de sueldo"]==1:
        estado["Costo por empleado"]=estado["Costo por empleado"]*1.015
    estado["Subida de sueldo"] += 1 # aumentar cada que se haga
    return estado

def rh_no_hacer_nada(estado):
    return estado


# ---------------- Marketing ----------------

def marketing_lanzar_campania(estado):
    if estado["Caja disponible"] >= 8000:
        estado["Caja disponible"] -= 8000
    elif estado["Caja disponible"] < 8000:
        estado["Deuda pendiente"] += (8000 - estado["Caja disponible"]) * 1.12
        estado["Caja disponible"] = 0
    if int(estado["Reputacion del mercado"].split()[-1])<7:
        estado["Reputacion del mercado"]="Nivel 7"
    estado["lanzar_campania"]=2
    estado["bloqueador_campania"]=5
    """
    - Añade “DemandaExtraTemporal” de +4000 unidades para el turno actual y el siguiente.
    - Aumenta nuestras ventas en 20% por dos turnos
      • Solo aumenta si existe inventario disponible para la venta.           // en estado final creo
      • Es posible vender por encima de los pedidos que teniamos (porque aparece demanda espontanea para este mismo mes).
    """
    return estado

def marketing_invertir_branding(estado):
    if estado["Caja disponible"] >= 12000:
        estado["Caja disponible"] -= 12000
    elif estado["Caja disponible"] < 12000:
        estado["Deuda pendiente"] += (12000 - estado["Caja disponible"]) * 1.12
        estado["Caja disponible"] = 0
    if int(estado["Reputacion del mercado"].split()[-1])<8:
        estado["reputacion anterior"] =int(estado["Reputacion del mercado"].split()[-1])
        estado["Reputacion del mercado"]="Nivel 8"
        estado["Temporizador_nivel"]=5
    estado["BrandingActivo"]=True
    estado["duracion_branding"]=5
    """
    - Puedes fijar el flag “BrandingActivo = True” para que la demanda base
      suba un 10 % en calcular_estado_final durante estos 5 turnos.
    """
    return estado

def marketing_estudio_mercado(estado):
    if estado["Caja disponible"] >= 5000:
        estado["Caja disponible"] -= 5000
    elif estado["Caja disponible"] < 5000:
        estado["Deuda pendiente"] += (5000 - estado["Caja disponible"]) * 1.12
        estado["Caja disponible"] = 0
    estado["Reputacion del mercado"] = "Nivel "+ str(int(estado["Reputacion del mercado"].split()[-1])+2)
    estado["duracion_demanda"] = 5
    estado["competidores_nuevos"] = 3

    return estado

def marketing_abrir_ecommerce(estado):
    if estado["EcommerceActivo"] == False:
        if estado["Caja disponible"] >= 20000:
            estado["EcommerceActivo"] = True
            estado["Caja disponible"] -= 20000
        elif estado["Caja disponible"] < 20000:
            estado["Deuda pendiente"] += (20000 - estado["Caja disponible"]) * 1.12
            estado["EcommerceActivo"] = True
            estado["Caja disponible"] = 0
    elif estado["EcommerceActivo"] == True:
        if estado["Caja disponible"] >= 2000:
            estado["Caja disponible"] -= 2000
        elif estado["Caja disponible"] < 2000:
            estado["Deuda pendiente"] += (2000 - estado["Caja disponible"]) * 1.12
            estado["Caja disponible"] = 0
    estado["duracion_ecommerce"] = 3
    """
            • Aumenta permanentemente “Pedidos por atender” en +5,000 por turno
              (se aplica en calcular_estado_final).
            • Aumenta permanentemente “Ventas” en +2,000 por turno
              (siempre y cuando exista inventario disponible para la venta).
            • Esto bloquea por 3 turnos cualquier Carta del Caos que afecte el e-comerce.
    """

    return estado

def marketing_co_branding(estado):
    if estado["Caja disponible"] >= 3000:
        estado["Caja disponible"] -= 3000
    elif estado["Caja disponible"] < 3000:
        estado["Deuda pendiente"] += (3000 - estado["Caja disponible"]) * 1.12
        estado["Caja disponible"] = 0
    estado["contador_co-branding"]=2
    estado["aumento_venta"]=20 #      (siempre y cuando exista inventario disponible para la venta).

    # demanda extra temporal se activara de 300000 turno 1 y 100000 turno 2 y se debe restablecer si no se cumple
    return estado


def marketing_no_hacer_nada(estado):
    return estado


# ---------------- Compras ----------------

def compras_comprar_insumos_nacionales(estado):
    if estado["Caja disponible"] >= 10000:
        estado["Caja disponible"] -= 10000
    elif estado["Caja disponible"] < 10000:
        estado["Deuda pendiente"] += (10000 - estado["Caja disponible"]) * 1.12
        estado["Caja disponible"] = 0
    estado["Insumos disponibles"]+=500000
    return estado

def compras_comprar_insumos_importados(estado):
    if estado["Caja disponible"] >= 14000:
        estado["Caja disponible"] -= 14000
    elif estado["Caja disponible"] < 14000:
        estado["Deuda pendiente"] += (14000 - estado["Caja disponible"]) * 1.12
        estado["Caja disponible"] = 0
    estado["Insumos disponibles"]+=800000
    return estado

def compras_comprar_insumos_importados_premium(estado):
    if estado["Caja disponible"] >= 25000:
        estado["Caja disponible"] -= 25000
    elif estado["Caja disponible"] < 25000:
        estado["Deuda pendiente"] += (25000 - estado["Caja disponible"]) * 1.12
        estado["Caja disponible"] = 0
    estado["Insumos disponibles"]+=900000
    estado["Contador_IP"]=3
    return estado

def compras_vender_excedentes_insumos(estado):
    estado["Caja disponible"] += 0.03 * estado["Insumos disponibles"] # mejor aplicar en estado final
    estado["Insumos disponibles"]=int(0.9*estado["Insumos disponibles"])
    estado["venta_excedente"]=3
    return estado

def compras_negociar_precio(estado):
    if estado["Caja disponible"] >= 5000:
        estado["Caja disponible"] -= 5000
    elif estado["Caja disponible"] < 5000:
        estado["Deuda pendiente"] += (5000 - estado["Caja disponible"]) * 1.12
        estado["Caja disponible"] = 0
    estado["Activacion_descuento"]=True
    estado["Descuento_compra"]=0.7
    return estado

def compras_negociar_credito(estado): # falta ajustar
    if estado["Caja disponible"] >= 2000:
        estado["Caja disponible"] -= 2000
    elif estado["Caja disponible"] < 2000:
        k = ['a', 'b', 'c', 'd']  # indice se reinicia
        estado["Registro_de_deudas(cantidad)"][estado["indice_deudas"]]=2000* 1.12
        if estado["indice_deudas"] < 4:
            estado["Registro_de_deudas(duracion)"][k[estado["indice_deudas"]]] = 3
            estado["indice_deudas"] += 1
        elif estado["indice_deudas"] == 4:
            estado["indice_deudas"] = 0
            estado["Registro_de_deudas(duracion)"][k[estado["indice_deudas"]]] = 3
            estado["indice_deudas"] += 1
    estado["CreditoConcedido"]=True
    return estado


def compras_no_hacer_nada(estado):
    return estado

# ---------------- Finanzas ----------------

def finanzas_pagar_proveedores(estado): # no entiendo
    if estado["Caja disponible"]>=(sum(estado["Registro_de_deudas(cantidad)"].values())*0.95):
        estado["Caja disponible"]-=sum(estado["Registro_de_deudas(cantidad)"].values())*0.95
    else:
        estado["Deuda pendiente"]+=1.12*(sum(estado["Registro_de_deudas(cantidad)"].values())*0.95-estado["Caja disponible"])
        estado["Caja disponible"]=0
    for f in ['a', 'b', 'c', 'd']:
        estado["Registro_de_deudas(cantidad)"][f]=0
        estado["Registro_de_deudas(duracion)"][f] = 0
    estado["indice_deudas"] = 0
    # falta el if para cuando este activo y no este activo
    """
    1. Pagar proveedores:
    Esta funcion esta relacionada con compras_negociar_credito.
    Aplica para compras de insumos al credito.
    Efecto:
    Pagar al contado todas las cuentas por pagar, obteniendo un descuento del 5% por pronto pago.
    - Solo aplica para compra de insumos
    - Si no tenemos deudas a 90, 60 o 30 dias, esta accion no hace nada.
    """
    return estado
def finanzas_pagar_deuda(estado):
    if estado["Caja disponible"]!=0 and estado["Deuda pendiente"]!=0:
        if estado["Caja disponible"] >= 10000 and estado["Deuda pendiente"] >= 10000:
            estado["Caja disponible"] -= 10000
            estado["Deuda pendiente"] -= 10000
        elif estado["Caja disponible"] >= 10000 and estado["Deuda pendiente"] < 10000:
            estado["Caja disponible"] -= estado["Deuda pendiente"]
            estado["Deuda pendiente"] = 0
        elif estado["Caja disponible"] < 10000 and estado["Deuda pendiente"] >= 10000:
            estado["Deuda pendiente"] -= estado["Caja disponible"]
            estado["Caja disponible"] = 0
        elif 0 < estado["Caja disponible"] < 10000 and 0 < estado["Deuda pendiente"] < 10000:
            if estado["Caja disponible"] > estado["Deuda pendiente"]:
               estado["Caja disponible"] -= estado["Deuda pendiente"]
            else:
                estado["Deuda pendiente"] -= estado["Caja disponible"]
                estado["Caja disponible"] = 0
    return estado

def finanzas_solicitar_prestamo(estado):
    estado["Caja disponible"] += 40000
    estado["Deuda pendiente"]+=42400
    return estado


def finanzas_crear_fondo_emergencia(estado):
    if estado["Fondo emergencia"] == False:
        if estado["Caja disponible"] >= 50000:
            estado["Caja disponible"] -= 50000
        elif estado["Caja disponible"] < 50000:
            estado["Deuda pendiente"] += (50000 - estado["Caja disponible"]) * 1.12
            estado["Caja disponible"] = 0
        estado["Fondo emergencia"] = True
        estado["contador_fondo_emergencia"] = 1

    return estado

def finanzas_no_hacer_nada(estado):
    return estado