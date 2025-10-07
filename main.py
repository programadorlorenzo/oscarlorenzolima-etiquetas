from reportlab.lib.units import cm
from generador_etiqueta import GeneradorEtiquetas
from excel_manager import ExcelManager
import os
from datetime import datetime

def main():
    """Función principal para generar las etiquetas."""
    # Ruta del archivo Excel (ajustar según corresponda)
    excel_path = "data/productos.xlsx"
    
    # Verificar si el archivo existe
    if not os.path.exists(excel_path):
        print(f"[ERROR] El archivo Excel no existe en {excel_path}")
        print("Por favor, coloque el archivo Excel en la carpeta 'data' o ajuste la ruta.")
        return
    
    # Crear el directorio de salida si no existe
    if not os.path.exists("output"):
        os.makedirs("output")
    
    # Crear manejador de Excel y cargar datos
    excel_manager = ExcelManager(excel_path)
    excel_manager.cargar_excel()
    
    # Generar datos para etiquetas basados en el stock de cada producto
    datos_etiquetas = excel_manager.generar_datos_etiquetas()

    # Helper local para mostrar los datos sin revelar el SKU
    def mask_sku(lista):
        masked = []
        for d in lista:
            copy = dict(d)
            if 'sku' in copy:
                copy['sku'] = '*** oculto ***'
            masked.append(copy)
        return masked

    print(mask_sku(datos_etiquetas))
    
    # Guardar el Excel con los códigos de barras generados
    # Podemos guardar una copia para no modificar el original
    current_time = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    excel_backup = f"data/productos_con_codigos_{current_time}.xlsx"
    excel_manager.guardar_excel(excel_backup)
    
    # También podemos sobrescribir el original si se desea
    excel_manager.guardar_excel()
    
    # Si no hay etiquetas para generar, terminar
    if not datos_etiquetas:
        print("[AVISO] No hay productos con stock para generar etiquetas")
        return
    print(f"[OK] Se generarán {len(datos_etiquetas)} etiquetas basadas en el stock de los productos.")
    print("Cada producto se replicará según su stock disponible.")
    print("El primer producto es:", mask_sku([datos_etiquetas[0]])[0])
    
    # Crear generador de etiquetas con página de 10.02cm de ancho
    generador = GeneradorEtiquetas("output/etiquetas_productos.pdf")
    
    # Generar PDF con etiquetas
    generador.generar_pdf(datos_etiquetas)
    
    print(f"[OK] PDF generado en: output/etiquetas_productos.pdf")

if __name__ == "__main__":
    main()