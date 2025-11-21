def calcular_estado_inicial():
    """
    Inicializa el diccionario `estado` con los indicadores clave de la empresa,
    incluyendo todos los flags y contadores que luego se referencian en
    calcular_estado_final().
    """
    empleados = 4
    costo_emp = 2000
    precio_venta = 4.5
    return {
        # Indicadores financieros y operativos
        "Caja disponible":                   50000,
        "Precio Venta": precio_venta,# agregado por mi
        "Inventario":                        0,
        "Pedidos por atender":               0,
        "Unidades vendidas":                 0,
        "Insumos disponibles":               100,
        "Cantidad de empleados":             empleados,
        "Costo por empleado":                costo_emp,
        "Sueldos por pagar":                 empleados * costo_emp,
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
        #contador de las cartas del caos

        # contadores agregados por mi
        "mejora_proceso":0,
        "duracion_demanda": 0,
        "competidores_nuevos": 0,
        "duracion_ecommerce": 0,
        "contador_fondo_emergencia": 0,
        "Ventas": 0,  # vinculado al estado final
        "Subida de sueldo":0,
        "bloqueador_clima":0,
        "Registro_de_cambios":{}# usare esto de aca para revertir efectos de las acciones
        "Registro_de_deudas(duracion)":{'a':0,'b':0,'c':0,'d':0}, # relacionado al credito de proveedores
        "Registro_de_deudas(cantidad)": {'a': 0, 'b': 0, 'c': 0, 'd': 0},
        "indice_deudas":0
    }

def calcular_estado_final(estado):
# funcion agregada por mi para multi deudas
    for s, d in estado["Registro_de_deudas(duracion)"].items():
       if d != 0:
          estado["Registro_de_deudas(duracion)"][s] -= 1
    #1-------------------
    while estado["Inventario"]>0 :
        if estado["Pedidos por atender"]>0:
           estado["Pedidos por atender"]-=1
           estado["Unidades vendidas"]+=1
           estado["Caja disponible"] += estado["Precio Venta"]
        elif estado["Pedidos por atender"]==0:
            break
        estado["Inventario"] -= 1
    if estado["Pedidos por atender"]>0:
        estado["Reputacion del mercado"]="Nivel"+" "+ str(int(estado["Reputacion del mercado"][-1])-1)
    """
    Aplica las formulas de calculo al final de cada turno (mes) en el siguiente orden:

    1) Venta automatica
       - El precio de venta se debe cargar de la función calcular_estado_inicial()
       - Vender hasta ‘Pedidos por atender’, descontar de ‘Inventario’
       - Sumar ingresos a ‘Caja disponible’
       - Incrementar ‘Unidades vendidas’
       - Descontar Pedidos por atender’
       - Si no se atiende el total de la demanda, la 'Reputacion del mercado' se reduce un nivel """
#2----------------------------------------------------
    estado["Pedidos por atender"]=1000*int(estado["Reputacion del mercado"][-1])
    if estado["BrandingActivo"]==True:
        estado["Demanda"]=estado["Demanda"]*1.1
    if estado["EcommerceActivo"]==True:
        estado["Demanda"]=estado["Demanda"]+5000
    if estado["DemandaExtraTemporal"]==True:
        if estado["DuracionRestante->Temporal"]==2:
            estado["Demanda"]=estado["Demanda"]+300000
            estado["DuracionRestante->Temporal"]-=1
        elif estado["DuracionRestante->Temporal"]==1:
            estado["Demanda"]=estado["Demanda"]+150000
            estado["DuracionRestante->Temporal"]-=1
    """
    2) Actualizacion de pedidos por atender
       - Calcular la demanda del proximo mes a partir de:
         • ‘Reputacion del mercado’
         • Flags permanentes (p. ej. ‘BrandingActivo’, ‘EcommerceActivo’)
         • Incrementos temporales (‘DemandaExtraTemporal’)
       - Almacenar en ‘Pedidos por atender’
       - Fórmula para calcular pedidos nuevos es: 1,000 x (nivel de reputación)
       - Recuerde que el Branding activo aumenta la demanda en 10%
       - Recuerde que tener un e-commerce aumenta la demanda en 5,000 unidades al mes
    (no hay xd)   - Recurde que la campaña promocional aumenta la demanda en 4,000 unidades al mes
       - Recuerde que el cobranding con una marca o influencer popular ocasiona:
        • Una demanda temporal de 300,000 solo por el primer mes (luego desaparece)
        • Una demanda temporal de 150,000 solo por el segundo mes  (luego desaparece)
    """
#3-------------------------------------
    if estado ["Caja disponible"] >= estado["Sueldos por pagar"]:
           estado["Caja disponible"]-=estado["Sueldos por pagar"]
    elif estado["Caja disponible"] < estado["Sueldos por pagar"]:
           estado["Deuda pendiente"]=(estado["Sueldos por pagar"]-estado["Caja disponible"])*1.12
           estado["Caja disponible"]=0
    """
    3) Pago de la nomina del mes actual
       - Tomar ‘Sueldos por pagar’
       - Si ‘Caja disponible’ ≥ ‘Sueldos por pagar’:
           • Restar de ‘Caja disponible’
         Sino:
           • Calcula cuanto es lo que falta pagar (‘Sueldos por pagar’ – ‘Caja disponible’)
           • Generar deuda con el 12% de interes total.
           • Poner ‘Caja disponible’ = 0
    """
#4----------------------------------------------
#esta ya escrito en la parte inicial
    """
       4) Generacion de la nomina del proximo mes
       - Calcular ‘Sueldos por pagar’ en base a la cantidad de empleados
           • No se toma en cuenta a los empleados temporales porque a ellos ya se les pago al contratarlos.
     """
#5-------------------------------------------------
#me falta programar las cartas
    """""
       5) Anular multas, accidentes, y demas cartas del caos
       - Esto dependera de la carta del caos que haya salido, y de los flags que tengas activos.
    """

#6-----------------------------------------------------
#no entiendo como usar
    """
    6) Produccion en automatico
       - Si ‘TurnosProduccionExtra’ > 0:
         • Se produce en automatico la misma cantidad del turno anterior (sin gastar insumos).
         • No debes disminuir ‘TurnosProduccionExtra’ porque dicho valor se reduce en el punto 7)
    """
#7------------------------------------------------------
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
#    if estado["Pedidos"]==0:

    """
    8) Perdida de inventario:
       - Los meses que no se produce nada, el 10% de insumos caduca.
       - Si la produccion de este mes uso menos inventario que el 10% disponible,
         entonces, el excedente caduca (hasta completar el 10% que vence).
       - Puedes apoyarte de las variables "InventarioMesAnterior" e "Inventario"
    """
    # 1) Venta automatica
    estado["Inventario"]            = estado["Inventario"]
    estado["Unidades vendidas"]     = estado["Unidades vendidas"]
    estado["Caja disponible"]       = estado["Caja disponible"]

    # 2) Actualizacion de pedidos por atender
    estado["Pedidos por atender"]   = estado["Pedidos por atender"]
    estado["Reputacion del mercado"] = estado["Reputacion del mercado"]

    # 3) Pago de la nomina del mes actual
    estado["Sueldos por pagar"]     = estado["Sueldos por pagar"]
    estado["Caja disponible"]       = estado["Caja disponible"]

    # 4) Generacion de la nomina del proximo mes
    estado["Sueldos por pagar"]     = estado["Sueldos por pagar"]

    # 5) Anular multas, accidentes, y demas cartas del caos
    estado["Prohibir Produccion"]   = estado["Prohibir Produccion"]

    # 6) Produccion en automatico
    estado["Inventario"]            = estado["Inventario"]

    # 7) Actualizacion de flags temporales y decremento de contadores
    estado["TurnosProduccionExtra"] = estado["TurnosProduccionExtra"]

    # 8) Perdida de inventario:
    estado["Inventario"]            = estado["Inventario"]
    return estado
