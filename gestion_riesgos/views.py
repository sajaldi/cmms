# gestion_riesgos/views.py

from django.shortcuts import render
from .models import Riesgo, Probabilidad, Impacto

def matriz_riesgos_view(request):
    """
    Prepara y renderiza la matriz de riesgos.
    Toda la lógica de cálculo se realiza aquí para mantener la plantilla simple.
    """
    # 1. Obtener los datos base de la base de datos
    probabilidades = Probabilidad.objects.order_by('-valor') # Mayor a menor para el eje Y
    impactos = Impacto.objects.order_by('valor')      # Menor a mayor para el eje X
    riesgos_abiertos = Riesgo.objects.filter(estado='abierto')

    # 2. Organizar los riesgos en un diccionario para un acceso rápido y eficiente
    # La clave es una tupla (id_probabilidad, id_impacto)
    riesgos_dict = {}
    for riesgo in riesgos_abiertos:
        if riesgo.probabilidad and riesgo.impacto:
            clave = (riesgo.probabilidad.id, riesgo.impacto.id)
            if clave not in riesgos_dict:
                riesgos_dict[clave] = []
            riesgos_dict[clave].append(riesgo)

    # 3. Construir la estructura de datos final para la plantilla
    # Será una lista de filas, donde cada fila tiene su data de celdas pre-calculada
    matriz_data = []
    for p in probabilidades:
        fila_actual = {'probabilidad': p, 'celdas': []}
        for i in impactos:
            # Calcular el nivel de riesgo para la celda actual
            nivel_riesgo = p.valor * i.valor

            # Determinar la clase CSS para el color basado en el nivel de riesgo
            if nivel_riesgo <= 4:
                color_clase = "nivel-bajo"
            elif nivel_riesgo <= 9:
                color_clase = "nivel-moderado"
            elif nivel_riesgo <= 15:
                color_clase = "nivel-alto"
            else:
                color_clase = "nivel-extremo"

            # Obtener la lista de riesgos que corresponden a esta celda del diccionario
            riesgos_en_celda = riesgos_dict.get((p.id, i.id), [])

            # Agregar toda la información de la celda a la fila
            fila_actual['celdas'].append({
                'riesgos': riesgos_en_celda,
                'color_clase': color_clase,
            })
        
        # Agregar la fila completa a la matriz
        matriz_data.append(fila_actual)

    # 4. Definir el contexto y renderizar la plantilla
    context = {
        'impactos': impactos,
        'matriz_data': matriz_data,
    }
    return render(request, 'gestion_riesgos/matriz_riesgos.html', context)