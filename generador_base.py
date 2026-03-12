from PIL import Image, ImageDraw, ImageFont, ImageOps
import io

# --- RUTAS DE ARCHIVOS LOCALES ---
# Asegúrate de que 'perfil.jpg' y 'arial.ttf' estén en la misma carpeta
FUENTE_PATH = "arial.ttf" 

# --- PARÁMETROS DEL CARNET ---
ANCHO_CARNET = 400
ALTO_CARNET = 600


def generar_carnet(nombre, cargo, empleado_id, color_marca, foto_bytes=None):
    # --- PROCESO DE GENERACIÓN DEL CARNET ---

    # 1. Crear el lienzo base del carnet
    carnet = Image.new('RGB', (ANCHO_CARNET, ALTO_CARNET), color='white')
    draw = ImageDraw.Draw(carnet)

    # 2. Cargar Fuentes (con manejo de errores para entorno local)
    try:
        font_nombre = ImageFont.truetype(FUENTE_PATH, 35)
        font_cargo = ImageFont.truetype(FUENTE_PATH, 20)
        font_id = ImageFont.truetype(FUENTE_PATH, 16)
        font_footer = ImageFont.truetype(FUENTE_PATH, 12)
    except IOError:
        # Si la fuente no se encuentra, usamos una por defecto (sin control de tamaño)
        font_nombre = ImageFont.load_default()
        font_cargo = ImageFont.load_default()
        font_id = ImageFont.load_default()
        font_footer = ImageFont.load_default()
        print("Advertencia: No se pudo cargar la fuente .ttf. Usando fuente por defecto.")

    # 3. Dibujar Banner Superior
    draw.rectangle([0, 0, ANCHO_CARNET, 180], fill=color_marca)

    # 4. Procesar y Pegar Foto de Perfil (Recorte Circular)
    try:
        foto_original = Image.open(foto_bytes)
        
        # Ajustar foto al tamaño del cuadro (180x180)
        foto_perfil = ImageOps.fit(foto_original, (180, 180), centering=(0.5, 0.5))
        
        # Crear máscara para el círculo (Todo blanco = visible)
        mask = Image.new('L', (180, 180), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 180, 180), fill=255) # Elipse blanca en fondo negro
        
        # Pegar la foto con la máscara circular
        # Coordenadas (x,y) donde se pegará la esquina superior izquierda de la foto
        carnet.paste(foto_perfil, (110, 90), mask) # Centrado para un ancho de 400
    except FileNotFoundError:
        print(f"Error: No se encontró la imagen de perfil en {foto_bytes}. Se dibujará un placeholder.")
        # Dibujar un círculo gris como placeholder si no hay foto
        draw.ellipse((110, 90, 110+180, 90+180), fill="#cccccc", outline="#666666", width=2)
        draw.text((150, 170), "SIN FOTO", fill="#333333", font=font_id)


    # 5. Inserción de Textos
    # Nombre (Centrado horizontalmente)
    draw.text((ANCHO_CARNET/2, 310), nombre.upper(), font=font_nombre, fill="black", anchor="mm")

    # Cargo (Centrado horizontalmente)
    draw.text((ANCHO_CARNET/2, 350), cargo, font=font_cargo, fill="#555555", anchor="mm")

    # Línea divisoria
    draw.line([120, 380, 280, 380], fill=color_marca, width=3)

    # ID del Empleado
    draw.text((ANCHO_CARNET/2, 410), f"ID: {empleado_id}", font=font_id, fill="black", anchor="mm")

    # 6. Footer del Carnet
    draw.rectangle([0, ALTO_CARNET - 60, ANCHO_CARNET, ALTO_CARNET], fill="#f8f9fa")
    draw.text((ANCHO_CARNET/2, ALTO_CARNET - 30), "PROPIEDAD PRIVADA - USO INTERNO", font=font_footer, fill="#adb5bd", anchor="mm")

    buffer = io.BytesIO()
    carnet.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

if __name__ == "__main__":
    # --- CONFIGURACIÓN DE DATOS ESTÁTICOS ---
    NOMBRE_EMPLEADO = "JUAN PERÉZ"
    CARGO_EMPLEADO = "Director de Marketing"
    ID_EMPLEADO = "EMP-7890"
    COLOR_MARCA = "#007bff"  # Azul corporativo
    IMAGEN_PERFIL_PATH = "perfil.jpg" 

    try:
        with open(IMAGEN_PERFIL_PATH, "rb") as f:
            foto = io.BytesIO(f.read())
    except FileNotFoundError:
        print(f"Advertencia: No se encontró '{IMAGEN_PERFIL_PATH}'. Se usará placeholder.")
        foto = None
    
    buffer = generar_carnet(NOMBRE_EMPLEADO, CARGO_EMPLEADO, ID_EMPLEADO, COLOR_MARCA, foto)

    # --- GUARDAR EL RESULTADO (para verificación local) ---
    # Guarda la imagen en la misma carpeta que el script
    nombre_archivo_salida = f"carnet_{NOMBRE_EMPLEADO.replace(' ', '_')}.png"
    with open(nombre_archivo_salida, "wb") as f:
        f.write(buffer.read())
    print(f"Carnet generado y guardado como: {nombre_archivo_salida}")

