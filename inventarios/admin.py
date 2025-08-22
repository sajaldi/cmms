from django.contrib import admin
from django.http import HttpResponse
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode import code128
from reportlab.lib.units import inch
from .models import ListaDeImpresion, ItemDeLista



# Register your models here.
##Registrar ListaDeImpresion
from .models import ListaDeImpresion     ,ItemDeLista       

# Función para generar el PDF
# Función para generar el PDF
# Función para generar el PDF
# Función para generar el PDF
def generar_pdf(lista_de_impresion):
    # Tamaño de la etiqueta
    if lista_de_impresion.tamano_etiqueta == 'pequeno':
        tamano = (3 * inch, 1 * inch)  # 3x1 pulgadas
    elif lista_de_impresion.tamano_etiqueta == 'mediano':
        tamano = (3 * inch, 2 * inch)  # 3x2 pulgadas
    else:
        tamano = (3 * inch, 3 * inch)  # 3x3 pulgadas

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{lista_de_impresion.nombre}_etiquetas.pdf"'

    c = canvas.Canvas(response, pagesize=tamano)
    width, height = tamano

    for item in lista_de_impresion.items.all():
        for _ in range(item.cantidad):
            # --- Código de barras ---
            barcode = code128.Code128(item.nombre, barHeight=0.8 * inch, barWidth=1.0)
            barcode_width = barcode.width
            x_pos = (width - barcode_width) / 2
            y_pos = height - 60
            barcode.drawOn(c, x_pos, y_pos)

            # --- Recuadro blanco para el nombre dentro del código de barras ---
            c.setFillColorRGB(1, 1, 1)  # Blanco
            text_width = c.stringWidth(item.nombre, "Helvetica-Bold", 14)
            text_x = (width - text_width) / 2
            text_y = y_pos + 0.15 * inch  # Ajustar verticalmente dentro del barcode
            padding_x = 2
            padding_y = 2
            c.rect(text_x - padding_x, text_y - padding_y, text_width + padding_x*2, 14 + padding_y*2, fill=1, stroke=0)

            # --- Nombre centrado dentro del recuadro ---
            c.setFillColorRGB(0, 0, 0)  # Negro
            c.setFont("Helvetica-Bold", 14)
            c.drawCentredString(width / 2, text_y, item.nombre)

            # --- Campo adicional más pequeño centrado abajo ---
            if item.campo_adicional:
                c.setFont("Helvetica", 9)
                c.drawCentredString(width / 2, 15, item.campo_adicional)

            c.showPage()

    c.save()
    return response


def generar_etiquetas(modeladmin, request, queryset):
    for lista in queryset:
        response = generar_pdf(lista)
        return response

generar_etiquetas.short_description = "Generar etiquetas en PDF"



class ItemDeListaInline(admin.TabularInline):  # o puedes usar StackedInline si prefieres un diseño diferente
    model = ItemDeLista
    extra = 1  # Número de formularios vacíos pa

###inline ItemDeLista


@admin.register(ListaDeImpresion)
class ListaDeImpresionAdmin(admin.ModelAdmin):
    inlines = [ItemDeListaInline]
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)  
    actions = [generar_etiquetas]