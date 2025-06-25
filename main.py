from reportlab.lib.units import cm
from generador_etiqueta import GeneradorEtiquetas

# Función principal
def main():
    """Función principal para generar las etiquetas."""
    # Crear generador de etiquetas con página de 10.02cm de ancho
    generador = GeneradorEtiquetas("output/etiquetas_multiple.pdf", custom_width=10.02*cm)
    
    # Generar datos de ejemplo (múltiplos de 3 para páginas completas)
    datos_etiquetas = generador.generar_mockup_datos(51)  # 17 páginas con 3 etiquetas cada una
    
    # Generar PDF con etiquetas
    generador.generar_pdf(datos_etiquetas)


if __name__ == "__main__":
    main()
