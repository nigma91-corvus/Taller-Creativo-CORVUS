import streamlit as st
import pandas as pd
from datetime import datetime, date
import os
import base64
import urllib.parse
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

# ==========================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(
    page_title="Corvus | Taller Creativo",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PASSWORD_ADMIN = "corvus123"
CATALOGO_FILE = "catalogo.csv"
HISTORIAL_FILE = "historial_ventas.csv"
GALERIA_DIR = "galeria_muestras"

if not os.path.exists(GALERIA_DIR):
    os.makedirs(GALERIA_DIR)

# Encontrar logo
def obtener_ruta_logo():
    for ext in ["logo.png", "logo.jpg", "logo.jpeg"]:
        if os.path.exists(ext):
            return ext
    return None

RUTA_LOGO = obtener_ruta_logo()

def get_base64_image(image_path):
    if image_path and os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return None

LOGO_BASE64 = get_base64_image(RUTA_LOGO)

# ==========================================
# CATÁLOGO EXTENDIDO Y CATEGORÍAS OFICIALES
# ==========================================
GENEROS_PREFIX = {
    "Promocionales": "PRO",
    "Credenciales y Plásticos": "CRE",
    "DTF": "DTF",
    "Impresión Digital": "DIG",
    "Acabados y Efectos 3D": "ACA",
    "Gran Formato y Banners": "GF",
    "Offset y Papelería": "OFF",
    "Sublimación": "SUB",
    "Corte y Grabado Láser": "LAS",
    "Corte de Vinil": "VIN-C",
    "Viniles por Metro": "VIN-M",
    "Otros": "OTR"
}

def cargar_catalogo():
    if os.path.exists(CATALOGO_FILE):
        df = pd.read_csv(CATALOGO_FILE)
        cat_dict = {}
        for _, row in df.iterrows():
            cat_dict[row["nombre"]] = {
                "cod": str(row["cod"]),
                "rango1": float(row["rango1"]),
                "rango2": float(row["rango2"]),
                "rango3": float(row["rango3"]),
                "rango4": float(row["rango4"]),
                "tipo": str(row["tipo"]),
                "cat": str(row["cat"])
            }
        return cat_dict
    else:
        # Base con 4 Escalas de Precios: (1-6, 7-50, 51-100, 101+)
        base = {
            # Promocionales
            "Taza 11oz Blanca (Lisa)": {"cod": "PRO-01", "rango1": 85.0, "rango2": 55.0, "rango3": 45.0, "rango4": 38.0, "tipo": "pieza", "cat": "Promocionales"},
            "Taza Fondo Color 11oz": {"cod": "PRO-02", "rango1": 95.0, "rango2": 65.0, "rango3": 55.0, "rango4": 48.0, "tipo": "pieza", "cat": "Promocionales"},
            "Taza Térmica / Mágica": {"cod": "PRO-03", "rango1": 120.0, "rango2": 85.0, "rango3": 75.0, "rango4": 68.0, "tipo": "pieza", "cat": "Promocionales"},
            "Taza Metálica Color": {"cod": "PRO-04", "rango1": 120.0, "rango2": 85.0, "rango3": 75.0, "rango4": 68.0, "tipo": "pieza", "cat": "Promocionales"},
            "Gorra Trucker (Lisa)": {"cod": "PRO-05", "rango1": 65.0, "rango2": 50.0, "rango3": 42.0, "rango4": 35.0, "tipo": "pieza", "cat": "Promocionales"},
            "Playera Liso Algodón (Cuello Redondo)": {"cod": "PRO-06", "rango1": 110.0, "rango2": 95.0, "rango3": 85.0, "rango4": 78.0, "tipo": "pieza", "cat": "Promocionales"},
            "Playera Tipo Polo": {"cod": "PRO-07", "rango1": 160.0, "rango2": 140.0, "rango3": 130.0, "rango4": 120.0, "tipo": "pieza", "cat": "Promocionales"},
            "Sudadera con Capucha (Lisa)": {"cod": "PRO-08", "rango1": 290.0, "rango2": 260.0, "rango3": 240.0, "rango4": 220.0, "tipo": "pieza", "cat": "Promocionales"},
            "Rompecabezas Sublimación": {"cod": "PRO-09", "rango1": 80.0, "rango2": 60.0, "rango3": 50.0, "rango4": 45.0, "tipo": "pieza", "cat": "Promocionales"},
            "Mouse Pad": {"cod": "PRO-10", "rango1": 75.0, "rango2": 55.0, "rango3": 45.0, "rango4": 38.0, "tipo": "pieza", "cat": "Promocionales"},
            "Fotoboton 5.5cm": {"cod": "PRO-11", "rango1": 15.0, "rango2": 10.0, "rango3": 8.0, "rango4": 6.5, "tipo": "pieza", "cat": "Promocionales"},
            "Fotoboton 7.5cm": {"cod": "PRO-12", "rango1": 18.0, "rango2": 12.0, "rango3": 9.0, "rango4": 7.5, "tipo": "pieza", "cat": "Promocionales"},
            "Termo Aluminio / Deportivo": {"cod": "PRO-13", "rango1": 140.0, "rango2": 110.0, "rango3": 95.0, "rango4": 85.0, "tipo": "pieza", "cat": "Promocionales"},

            # Credenciales y Plásticos
            "Credencial PVC Paquete / Pieza": {"cod": "CRE-01", "rango1": 45.0, "rango2": 25.0, "rango3": 18.0, "rango4": 12.0, "tipo": "pieza", "cat": "Credenciales y Plásticos"},
            "Credencial Sublimada Color Oro": {"cod": "CRE-02", "rango1": 55.0, "rango2": 35.0, "rango3": 28.0, "rango4": 22.0, "tipo": "pieza", "cat": "Credenciales y Plásticos"},
            "Credencial Sublimada Color Plata": {"cod": "CRE-03", "rango1": 55.0, "rango2": 35.0, "rango3": 28.0, "rango4": 22.0, "tipo": "pieza", "cat": "Credenciales y Plásticos"},
            "Cinta / Lanyard Porta-gafete": {"cod": "CRE-04", "rango1": 35.0, "rango2": 25.0, "rango3": 20.0, "rango4": 15.0, "tipo": "pieza", "cat": "Credenciales y Plásticos"},

            # DTF
            "DTF Textil 58x100 cm (Metro Lineal)": {"cod": "DTF-01", "rango1": 320.0, "rango2": 280.0, "rango3": 250.0, "rango4": 220.0, "tipo": "m_lineal", "cat": "DTF"},
            "DTF UV 58x100 cm (Metro Lineal)": {"cod": "DTF-02", "rango1": 700.0, "rango2": 650.0, "rango3": 600.0, "rango4": 550.0, "tipo": "m_lineal", "cat": "DTF"},
            "DTF UV Metro (28 cm)": {"cod": "DTF-03", "rango1": 420.0, "rango2": 380.0, "rango3": 340.0, "rango4": 300.0, "tipo": "m_lineal", "cat": "DTF"},
            "DTF UV Carta (21x27 cm)": {"cod": "DTF-04", "rango1": 220.0, "rango2": 190.0, "rango3": 170.0, "rango4": 150.0, "tipo": "pieza", "cat": "DTF"},
            "DTF UV Tabloide (27x43 cm)": {"cod": "DTF-05", "rango1": 260.0, "rango2": 230.0, "rango3": 200.0, "rango4": 180.0, "tipo": "pieza", "cat": "DTF"},

            # Impresión Digital (Tabloides y Papeles)
            "Tabloide Couché 150g (Solo Frente)": {"cod": "DIG-01", "rango1": 10.0, "rango2": 7.0, "rango3": 6.0, "rango4": 5.0, "tipo": "pieza", "cat": "Impresión Digital"},
            "Tabloide Couché 300g (Solo Frente)": {"cod": "DIG-02", "rango1": 16.0, "rango2": 13.0, "rango3": 11.0, "rango4": 9.5, "tipo": "pieza", "cat": "Impresión Digital"},
            "Tabloide Couché 300g (Frente y Vuelta)": {"cod": "DIG-03", "rango1": 22.0, "rango2": 18.0, "rango3": 15.0, "rango4": 13.0, "tipo": "pieza", "cat": "Impresión Digital"},
            "Tabloide Adhesivo UPM": {"cod": "DIG-04", "rango1": 15.0, "rango2": 11.0, "rango3": 9.5, "rango4": 8.0, "tipo": "pieza", "cat": "Impresión Digital"},
            "Tabloide Adhesivo Dorado / Plateado": {"cod": "DIG-05", "rango1": 25.0, "rango2": 20.0, "rango3": 17.0, "rango4": 15.0, "tipo": "pieza", "cat": "Impresión Digital"},
            "Tabloide Adhesivo Holográfico": {"cod": "DIG-06", "rango1": 30.0, "rango2": 25.0, "rango3": 22.0, "rango4": 20.0, "tipo": "pieza", "cat": "Impresión Digital"},
            "Tabloide Polipropileno Blanco / Transparente": {"cod": "DIG-07", "rango1": 30.0, "rango2": 25.0, "rango3": 22.0, "rango4": 20.0, "tipo": "pieza", "cat": "Impresión Digital"},
            "Tabloide Cartulina Opalina 350g": {"cod": "DIG-08", "rango1": 18.0, "rango2": 15.0, "rango3": 13.0, "rango4": 11.0, "tipo": "pieza", "cat": "Impresión Digital"},

            # Gran Formato y Banners
            "Lona Front 13 oz (m²)": {"cod": "GF-01", "rango1": 60.0, "rango2": 45.0, "rango3": 38.0, "rango4": 32.0, "tipo": "m2", "cat": "Gran Formato y Banners"},
            "Lona Backlite (m²)": {"cod": "GF-02", "rango1": 120.0, "rango2": 100.0, "rango3": 90.0, "rango4": 80.0, "tipo": "m2", "cat": "Gran Formato y Banners"},
            "Lona Mesh (m²)": {"cod": "GF-03", "rango1": 200.0, "rango2": 170.0, "rango3": 150.0, "rango4": 135.0, "tipo": "m2", "cat": "Gran Formato y Banners"},
            "Vinil Brillante / Mate (m²)": {"cod": "GF-04", "rango1": 110.0, "rango2": 85.0, "rango3": 75.0, "rango4": 65.0, "tipo": "m2", "cat": "Gran Formato y Banners"},
            "Vinil Microperforado (m²)": {"cod": "GF-05", "rango1": 180.0, "rango2": 150.0, "rango3": 135.0, "rango4": 120.0, "tipo": "m2", "cat": "Gran Formato y Banners"},
            "Banner 60x160 cm (Estructura + Lona)": {"cod": "GF-06", "rango1": 250.0, "rango2": 220.0, "rango3": 200.0, "rango4": 180.0, "tipo": "pieza", "cat": "Gran Formato y Banners"},

            # Offset y Papelería
            "Millar Tarjetas Couché 4x1": {"cod": "OFF-01", "rango1": 150.0, "rango2": 120.0, "rango3": 110.0, "rango4": 95.0, "tipo": "pieza", "cat": "Offset y Papelería"},
            "Millar Volantes 1/4 Carta 4x1": {"cod": "OFF-02", "rango1": 200.0, "rango2": 160.0, "rango3": 140.0, "rango4": 125.0, "tipo": "pieza", "cat": "Offset y Papelería"},

            # Sublimación
            "Pliego Papel para Sublimar": {"cod": "SUB-01", "rango1": 45.0, "rango2": 38.0, "rango3": 32.0, "rango4": 28.0, "tipo": "pieza", "cat": "Sublimación"},
            "Hoja Carta Papel Sublimación": {"cod": "SUB-02", "rango1": 15.0, "rango2": 12.0, "rango3": 9.0, "rango4": 7.0, "tipo": "pieza", "cat": "Sublimación"},

            # Corte y Grabado Láser
            "Corte Láser MDF 3mm (Servicio/Minuto)": {"cod": "LAS-01", "rango1": 20.0, "rango2": 16.0, "rango3": 14.0, "rango4": 12.0, "tipo": "pieza", "cat": "Corte y Grabado Láser"},
            "Corte Láser Acrílico (Servicio/Minuto)": {"cod": "LAS-02", "rango1": 25.0, "rango2": 22.0, "rango3": 18.0, "rango4": 15.0, "tipo": "pieza", "cat": "Corte y Grabado Láser"},

            # Viniles por Metro
            "Vinil Textil Básico (Metro Lineal)": {"cod": "VIN-M01", "rango1": 150.0, "rango2": 130.0, "rango3": 115.0, "rango4": 100.0, "tipo": "m_lineal", "cat": "Viniles por Metro"},
            "Vinil Textil Detalle (Metro Lineal)": {"cod": "VIN-M02", "rango1": 190.0, "rango2": 165.0, "rango3": 150.0, "rango4": 135.0, "tipo": "m_lineal", "cat": "Viniles por Metro"},

            # Otros
            "Servicio de Planchado / Aplicación": {"cod": "OTR-01", "rango1": 40.0, "rango2": 30.0, "rango3": 25.0, "rango4": 20.0, "tipo": "pieza", "cat": "Otros"}
        }
        guardar_catalogo_dict(base)
        return base

def guardar_catalogo_dict(cat_dict):
    data = []
    for nombre, info in cat_dict.items():
        data.append({
            "cod": info["cod"],
            "nombre": nombre,
            "rango1": info["rango1"],
            "rango2": info["rango2"],
            "rango3": info["rango3"],
            "rango4": info["rango4"],
            "tipo": info["tipo"],
            "cat": info["cat"]
        })
    df = pd.DataFrame(data)
    df.to_csv(CATALOGO_FILE, index=False)

def obtener_siguiente_codigo(genero_nombre):
    prefijo = GENEROS_PREFIX.get(genero_nombre, "GEN")
    cat_dict = cargar_catalogo()
    codigos_existentes = []
    for info in cat_dict.values():
        if info["cat"] == genero_nombre and info["cod"].startswith(prefijo + "-"):
            try:
                num = int(info["cod"].split("-")[1])
                codigos_existentes.append(num)
            except ValueError:
                pass
    siguiente_num = max(codigos_existentes) + 1 if codigos_existentes else 1
    return f"{prefijo}-{siguiente_num:02d}"

def calcular_precio_escala(info_producto, cantidad):
    if cantidad <= 6:
        return info_producto["rango1"], "1-6 pzs"
    elif cantidad <= 50:
        return info_producto["rango2"], "7-50 pzs"
    elif cantidad <= 100:
        return info_producto["rango3"], "51-100 pzs"
    else:
        return info_producto["rango4"], "101+ pzs"

CATALOGO_PRODUCTOS = cargar_catalogo()

# ==========================================
# ESTILOS CSS - POS DINÁMICO CORVUS
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap');

    [data-testid="collapsedControl"] { display: none; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp {
        background-color: #0A0A0A !important;
        color: #FFFFFF !important;
        font-family: 'Montserrat', sans-serif !important;
    }

    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #0A0A0A;
        border-bottom: 2px solid #C9A33F;
        z-index: 99999;
        padding: 12px 30px;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .header-spacer {
        margin-top: 105px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: flex-start;
        margin-bottom: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1A1A1A !important;
        border: 1px solid #866E2E !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #C9A33F !important;
        color: #0A0A0A !important;
        font-weight: 800 !important;
    }

    h1, h2, h3, h4 {
        color: #C9A33F !important;
        font-weight: 800 !important;
        letter-spacing: 1px;
    }

    .ticket-container {
        background-color: #141414;
        border: 2px solid #C9A33F;
        border-radius: 10px;
        padding: 18px;
        box-shadow: 0 4px 15px rgba(201, 163, 63, 0.15);
    }

    div[data-baseweb="select"] > div, input {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 1px solid #C9A33F !important;
        border-radius: 6px !important;
    }
    ul[data-baseweb="menu"] {
        background-color: #1A1A1A !important;
    }
    li[data-baseweb="option"] {
        color: #FFFFFF !important;
    }
    li[data-baseweb="option"]:hover {
        background-color: #C9A33F !important;
        color: #0A0A0A !important;
    }

    .stButton>button {
        background-color: #C9A33F !important;
        color: #0A0A0A !important;
        font-weight: 800 !important;
        border-radius: 6px !important;
        border: none !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #E2B74A !important;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

if 'carrito' not in st.session_state:
    st.session_state.carrito = []

# ==========================================
# GENERADOR DE PDF REMISIÓN
# ==========================================
def generar_pdf_remision(datos_orden, carrito):
    folio = datos_orden["folio"]
    filename = f"Remision_{folio}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    
    # Header Banner
    c.setFillColor(colors.HexColor("#0A0A0A"))
    c.rect(0, 680, 612, 120, fill=True)
    
    if RUTA_LOGO and os.path.exists(RUTA_LOGO):
        try:
            c.drawImage(RUTA_LOGO, 30, 685, width=95, height=95, preserveAspectRatio=True, mask='auto')
            x_off = 135
        except:
            x_off = 40
    else:
        x_off = 40
        
    c.setFillColor(colors.HexColor("#C9A33F"))
    c.setFont("Helvetica-Bold", 20)
    c.drawString(x_off, 755, "CORVUS TALLER CREATIVO")
    c.setFont("Helvetica", 10)
    c.drawString(x_off, 735, f"NOTA DE REMISIÓN | FOLIO: #{folio}")
    c.drawString(x_off, 715, f"Recepción: {datos_orden['f_recepcion']} | Entrega: {datos_orden['f_entrega']}")
    
    # Datos Cliente
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(40, 660, f"Cliente: {datos_orden['cliente']}")
    c.drawString(320, 660, f"Teléfono: {datos_orden['telefono']}")
    c.drawString(40, 645, f"Dirección: {datos_orden['direccion']}")
    c.drawString(320, 645, f"Tipo de Pago: {datos_orden['tipo_pago']}")
    
    # Tabla
    y = 615
    c.setFillColor(colors.HexColor("#0A0A0A"))
    c.rect(40, y-5, 532, 18, fill=True)
    c.setFillColor(colors.HexColor("#C9A33F"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(45, y, "Código")
    c.drawString(105, y, "Descripción")
    c.drawString(300, y, "Detalle")
    c.drawString(420, y, "P. Unit")
    c.drawString(500, y, "Subtotal")
    
    y -= 20
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 8.5)
    for item in carrito:
        c.drawString(45, y, str(item['Código']))
        c.drawString(105, y, str(item['Producto'])[:30])
        c.drawString(300, y, str(item['Detalle'])[:22])
        c.drawString(420, y, f"${item['P. Unit']:.2f}")
        c.drawString(500, y, f"${item['Subtotal']:.2f}")
        y -= 15
        
    c.line(40, y, 572, y)
    
    # Totales
    y -= 25
    c.setFont("Helvetica-Bold", 10)
    c.drawString(350, y, f"Total de Orden: ${datos_orden['total']:.2f} MXN")
    
    if datos_orden['anticipo'] > 0:
        y -= 15
        c.drawString(350, y, f"Anticipo Recibido: ${datos_orden['anticipo']:.2f} MXN")
        y -= 15
        c.setFillColor(colors.HexColor("#A80000"))
        c.drawString(350, y, f"SALDO PENDIENTE: ${datos_orden['saldo']:.2f} MXN")

    # Cláusula
    y_leyenda = 105
    c.setStrokeColor(colors.HexColor("#866E2E"))
    c.setFillColor(colors.HexColor("#FAF8F5"))
    c.rect(40, y_leyenda - 10, 532, 50, fill=True, stroke=True)
    
    c.setFillColor(colors.HexColor("#0A0A0A"))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(50, y_leyenda + 28, "TÉRMINOS DE SERVICIO Y GARANTÍA CORVUS:")
    c.setFont("Helvetica", 7.5)
    
    if datos_orden.get("archivo_cliente", False):
        c.drawString(50, y_leyenda + 15, "* Archivos proporcionados por el cliente: Corvus no se responsabiliza por ortografía, baja resolución o color de origen.")
    else:
        c.drawString(50, y_leyenda + 15, "* Diseño desarrollado por Corvus Taller Creativo y autorizado formalmente por el cliente.")
        
    c.drawString(50, y_leyenda + 3, "* La entrega está sujeta a anticipos e insumos. En prendas externas existe una tolerancia de merma del 2%.")

    # Firma
    c.setFillColor(colors.black)
    c.line(40, 40, 220, 40)
    c.setFont("Helvetica", 8)
    c.drawString(65, 28, "Firma de Conformidad Cliente")

    c.save()
    return filename

# ==========================================
# ENCABEZADO DESTACADO DE LA APLICACIÓN
# ==========================================
if LOGO_BASE64:
    logo_html = f'<img src="data:image/png;base64,{LOGO_BASE64}" style="max-height: 70px; width: auto; border-radius: 6px;">'
else:
    logo_html = '<span style="font-size: 2.5rem;">👑</span>'

st.markdown(f"""
    <div class="fixed-header">
        <div style="display: flex; align-items: center; gap: 20px;">
            <div>{logo_html}</div>
            <div>
                <h1 style="margin: 0; color: #C9A33F; font-size: 1.8rem; line-height: 1;">CORVUS</h1>
                <p style="margin: 0; color: #FFFFFF; font-size: 0.8rem; letter-spacing: 4px; font-weight: 600;">TALLER CREATIVO</p>
            </div>
        </div>
    </div>
    <div class="header-spacer"></div>
""", unsafe_allow_html=True)

# NAVEGACIÓN
tab1, tab2, tab3, tab4 = st.tabs(["🛒 PUNTO DE VENTA (POS)", "🖼️ GALERÍA DE MUESTRAS", "➕ NUEVO PRODUCTO / CATÁLOGO", "📊 HISTORIAL DE VENTAS"])

# ------------------------------------------
# TAB 1: PUNTO DE VENTA DINÁMICO (POS 2 COLUMNAS)
# ------------------------------------------
with tab1:
    col_izq, col_der = st.columns([1.2, 1])

    with col_izq:
        st.markdown("### 🔍 SELECCIÓN Y CONFIGURACIÓN")
        
        # BUSCADOR RÁPIDO
        busqueda_txt = st.text_input("🔎 Buscador rápido por palabra clave (ej. 'taza', 'pvc', 'láser'):", "")
        
        cats = list(GENEROS_PREFIX.keys())
        cat_activa = st.selectbox("Familia / Categoría Oficial:", cats)
        
        if busqueda_txt.strip():
            prods_cat = [p for p, info in CATALOGO_PRODUCTOS.items() if busqueda_txt.lower() in p.lower()]
        else:
            prods_cat = [p for p, info in CATALOGO_PRODUCTOS.items() if info["cat"] == cat_activa]
        
        if prods_cat:
            prod_sel = st.selectbox("Producto o Servicio:", prods_cat)
            info_p = CATALOGO_PRODUCTOS[prod_sel]
            cod_p = info_p["cod"]
            tipo_p = info_p["tipo"]

            # CONTROLES SEGÚN TIPO Y CÁLCULO POR ESCALA
            if "Playera" in prod_sel or "Sudadera" in prod_sel or "Gorra" in prod_sel:
                st.markdown("#### 👕 **DETALLE INDIVIDUAL DE PRENDA**")
                col_c1, col_c2, col_c3 = st.columns(3)
                with col_c1:
                    corte_p = st.selectbox("Corte:", ["Caballero", "Dama", "Infantil", "Unisex"])
                with col_c2:
                    talla_p = st.selectbox("Talla:", ["CH", "M", "G", "XG", "2XG", "Talla 2", "Talla 4", "Talla 6", "Talla 8", "Talla 10", "Talla 12"])
                with col_c3:
                    color_p = st.text_input("Color:", "Negro")
                cant_pz = st.number_input("Cantidad de prendas iguales:", min_value=1, value=1, step=1)
                
                det_final = f"Corte: {corte_p} | Talla: {talla_p} | Color: {color_p}"
                cant_unidades = float(cant_pz)

            elif tipo_p == "m2":
                col_m1, col_m2 = st.columns(2)
                with col_m1: ancho = st.number_input("Ancho (m):", min_value=0.1, value=1.0, step=0.1)
                with col_m2: alto = st.number_input("Alto (m):", min_value=0.1, value=1.0, step=0.1)
                cant_unidades = ancho * alto
                det_final = f"{ancho:.2f}m x {alto:.2f}m ({cant_unidades:.2f} m²)"

            elif tipo_p == "m_lineal":
                cant_m = st.number_input("Metros Lineales (ej. 0.5m, 1.2m):", min_value=0.1, value=1.0, step=0.1)
                cant_unidades = float(cant_m)
                det_final = f"{cant_unidades:.2f} Metro(s) Lineales"

            else:
                cant_pz = st.number_input("Cantidad:", min_value=1, value=1, step=1)
                cant_unidades = float(cant_pz)
                det_final = f"{cant_unidades:.0f} pieza(s)/servicio(s)"

            precio_base_escala, etiqueta_escala = calcular_precio_escala(info_p, cant_unidades)
            st.caption(f"📌 Código: **{cod_p}** | Tarifa Escala (**{etiqueta_escala}**): **${precio_base_escala:.2f} MXN** por {tipo_p}")

            # PRORRATEO DE DISEÑO
            incluye_diseno = st.checkbox("🎨 Incluir Cobro de Arte/Diseño Prorrateado")
            costo_diseno_extra = 0.0
            if incluye_diseno:
                tarifa_diseno = st.number_input("Monto Total del Diseño ($ MXN):", min_value=0.0, value=50.0, step=10.0)
                if cant_unidades > 0:
                    costo_diseno_extra = tarifa_diseno / cant_unidades

            precio_unitario_final = precio_base_escala + costo_diseno_extra
            subtotal_item = cant_unidades * precio_unitario_final

            if st.button("➕ AGREGAR ITEM AL TICKET EN VIVO"):
                st.session_state.carrito.append({
                    "Código": cod_p,
                    "Producto": prod_sel,
                    "Detalle": det_final,
                    "P. Unit": precio_unitario_final,
                    "Subtotal": subtotal_item
                })
                st.toast(f"¡{prod_sel} agregado al ticket!")

        st.divider()
        with st.expander("✨ Agregar Servicio Especial / Trabajo a Medida"):
            nom_custom = st.text_input("Descripción del Servicio Especial:", "Corte Láser Custom / Maquila")
            precio_custom = st.number_input("Precio Unitario Final ($ MXN):", min_value=1.0, value=100.0, step=10.0)
            cant_custom = st.number_input("Cantidad / Unidades:", min_value=1.0, value=1.0, step=1.0)
            if st.button("➕ AGREGAR TRABAJO ESPECIAL"):
                st.session_state.carrito.append({
                    "Código": "CUSTOM",
                    "Producto": nom_custom,
                    "Detalle": f"{cant_custom:.0f} servicio(s)",
                    "P. Unit": precio_custom,
                    "Subtotal": cant_custom * precio_custom
                })
                st.toast("Trabajo especial agregado.")

    with col_der:
        st.markdown("""<div class="ticket-container">""", unsafe_allow_html=True)
        st.markdown("### 📄 TICKET / REMISIÓN EN TIEMPO REAL")
        
        if len(st.session_state.carrito) > 0:
            df_ticket = pd.DataFrame(st.session_state.carrito)
            st.dataframe(df_ticket[["Código", "Producto", "P. Unit", "Subtotal"]], use_container_width=True)
            
            if st.button("🗑️ Vaciar Ticket"):
                st.session_state.carrito = []
                st.rerun()

            st.write("---")
            st.markdown("#### **DATOS DE LOGÍSTICA**")
            cli_nombre = st.text_input("Cliente:", "Público General")
            cli_tel = st.text_input("Teléfono (para WhatsApp):", "")
            cli_dir = st.text_input("Dirección:", "Recoge en Taller")
            tipo_pago = st.selectbox("Forma de Pago:", ["Efectivo", "Transferencia", "Tarjeta Débito/Crédito", "Mercado Pago"])
            f_recep = datetime.now().strftime("%Y-%m-%d %H:%M")
            f_entrega = st.date_input("Fecha Promesa de Entrega:", date.today()).strftime("%Y-%m-%d")

            archivo_cli = st.checkbox("⚠️ Insumos / Archivos del Cliente", value=True)

            subtotal_orden = sum(i["Subtotal"] for i in st.session_state.carrito)
            anticipo_ingresado = st.number_input("Anticipo Recibido ($ MXN):", min_value=0.0, value=0.0, step=50.0)
            saldo_debido = max(0.0, subtotal_orden - anticipo_ingresado)

            st.markdown(f"""
                <div style="background-color: #1A1A1A; border: 1px solid #C9A33F; padding: 12px; border-radius: 8px; margin-top: 10px;">
                    <p style="margin: 0; font-size: 1.1rem; color: #FFFFFF;">TOTAL: <b>${subtotal_orden:.2f} MXN</b></p>
                    <p style="margin: 0; font-size: 1rem; color: #C9A33F;">ANTICIPO: <b>${anticipo_ingresado:.2f} MXN</b></p>
                    <p style="margin: 0; font-size: 1.1rem; color: #FF4B4B;">PENDIENTE: <b>${saldo_debido:.2f} MXN</b></p>
                </div>
            """, unsafe_allow_html=True)

            folio_orden = datetime.now().strftime("%Y%m%d%H%M")

            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("📄 GENERAR PDF"):
                    datos_o = {
                        "folio": folio_orden, "cliente": cli_nombre, "telefono": cli_tel, "direccion": cli_dir,
                        "f_recepcion": f_recep, "f_entrega": f_entrega, "tipo_pago": tipo_pago,
                        "total": subtotal_orden, "anticipo": anticipo_ingresado, "saldo": saldo_debido, "archivo_cliente": archivo_cli
                    }
                    registro = {
                        "Folio": folio_orden, "Fecha Recepcion": f_recep, "Fecha Entrega": f_entrega, "Cliente": cli_nombre,
                        "Telefono": cli_tel, "Tipo Pago": tipo_pago, "Total": subtotal_orden, "Anticipo": anticipo_ingresado,
                        "Saldo Pendiente": saldo_debido, "Archivo Cliente": "SÍ" if archivo_cli else "NO",
                        "Productos": ", ".join([f"[{i['Código']}] {i['Producto']} ({i['Detalle']})" for i in st.session_state.carrito])
                    }
                    df_h = pd.DataFrame([registro])
                    if os.path.exists(HISTORIAL_FILE):
                        df_h.to_csv(HISTORIAL_FILE, mode='a', header=False, index=False)
                    else:
                        df_h.to_csv(HISTORIAL_FILE, index=False)

                    pdf_file = generar_pdf_remision(datos_o, st.session_state.carrito)
                    with open(pdf_file, "rb") as f_pdf:
                        st.download_button(label="⬇️ DESCARGAR PDF", data=f_pdf, file_name=pdf_file, mime="application/pdf")

            with col_btn2:
                # GENERAR ENLACE DE WHATSAPP
                msg_wa = f"👑 *CORVUS | TALLER CREATIVO*\n"
                msg_wa += f"📄 *COTIZACIÓN FOLIO #{folio_orden}*\n"
                msg_wa += f"👤 *Cliente:* {cli_nombre}\n"
                msg_wa += f"----------------------------------\n"
                msg_wa += f"📦 *DETALLE DE TU PEDIDO:*\n"
                for item in st.session_state.carrito:
                    msg_wa += f"• {item['Producto']} ({item['Detalle']}) -> ${item['Subtotal']:.2f}\n"
                msg_wa += f"----------------------------------\n"
                msg_wa += f"💰 *TOTAL:* ${subtotal_orden:.2f} MXN\n"
                msg_wa += f"💳 *ANTICIPO:* ${anticipo_ingresado:.2f} MXN\n"
                msg_wa += f"🟡 *SALDO PENDIENTE:* ${saldo_debido:.2f} MXN\n\n"
                msg_wa += f"¡Quedamos a tus órdenes para iniciar la producción!"

                encoded_msg = urllib.parse.quote(msg_wa)
                wa_url = f"https://api.whatsapp.com/send?phone={cli_tel.strip().replace('+', '').replace(' ', '')}&text={encoded_msg}" if cli_tel else f"https://api.whatsapp.com/send?text={encoded_msg}"
                st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366 !important; color:white; font-weight:800; padding:8px 16px; border-radius:6px; border:none; cursor:pointer;">📲 ENVIAR POR WHATSAPP</button></a>', unsafe_allow_html=True)

        else:
            st.info("El ticket está vacío. Selecciona un producto a la izquierda y presiona 'Agregar'.")
        
        st.markdown("""</div>""", unsafe_allow_html=True)

# ------------------------------------------
# TAB 2: GALERÍA GENERAL DE MUESTRAS
# ------------------------------------------
with tab2:
    st.markdown("### 🖼️ GALERÍA DE MUESTRAS Y TRABAJOS TERMINADOS")
    
    col_g1, col_g2 = st.columns([1, 2])
    with col_g1:
        st.markdown("#### **Subir Nueva Fotografía de Trabajo**")
        cat_foto = st.selectbox("Categoría de la Muestra:", list(GENEROS_PREFIX.keys()), key="cat_foto_key")
        nom_muestra = st.text_input("Título / Descripción Corta:", "Muestra Grabado Láser MDF")
        foto_archivo = st.file_uploader("Tomar Foto o Cargar Imagen:", type=["png", "jpg", "jpeg"])
        
        if st.button("💾 GUARDAR EN GALERÍA"):
            if foto_archivo and nom_muestra:
                f_name = f"{GENEROS_PREFIX[cat_foto]}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
                r_dest = os.path.join(GALERIA_DIR, f_name)
                img = Image.open(foto_archivo)
                img.convert("RGB").save(r_dest)
                st.success("¡Imagen guardada en la Galería General!")
                st.rerun()

    col_der_galeria = col_g2
    with col_der_galeria:
        st.markdown("#### **Muestrario para Clientes en Mostrador**")
        cat_filtro = st.selectbox("Filtrar Muestras por Categoría:", ["TODAS"] + list(GENEROS_PREFIX.keys()))
        
        fotos_existentes = [f for f in os.listdir(GALERIA_DIR) if f.endswith(('.jpg', '.png', '.jpeg'))]
        if cat_filtro != "TODAS":
            pref = GENEROS_PREFIX[cat_filtro] + "_"
            fotos_existentes = [f for f in fotos_existentes if f.startswith(pref)]

        if fotos_existentes:
            cols_grid = st.columns(3)
            for idx, f_item in enumerate(fotos_existentes):
                path_f = os.path.join(GALERIA_DIR, f_item)
                with cols_grid[idx % 3]:
                    st.image(path_f, use_container_width=True, caption=f_item.split(".")[0])
        else:
            st.info("No hay muestras registradas en esta categoría.")

# ------------------------------------------
# TAB 3: GESTIÓN DE CATÁLOGO Y EDICIÓN MASIVA
# ------------------------------------------
with tab3:
    st.markdown("### ➕ ADMINISTRACIÓN Y EDICIÓN MASIVA DEL CATÁLOGO")
    pass_cat = st.text_input("Contraseña Admin:", type="password", key="pass_cat_key")
    
    if pass_cat == PASSWORD_ADMIN:
        st.success("Acceso Concedido")
        
        st.markdown("#### **1. Alta de Nuevo Producto**")
        gen_nuevo = st.selectbox("Categoría Oficial:", list(GENEROS_PREFIX.keys()))
        cod_sugerido = obtener_siguiente_codigo(gen_nuevo)
        st.info(f"💡 Código Autogenerado: **{cod_sugerido}**")
        
        nom_nuevo = st.text_input("Nombre del Producto / Insumo:")
        tipo_nuevo = st.selectbox("Unidad de Cobro:", ["pieza", "m2", "m_lineal"])
        
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        with col_r1: p_r1 = st.number_input("Precio 1-6 pzs:", min_value=0.1, value=50.0)
        with col_r2: p_r2 = st.number_input("Precio 7-50 pzs:", min_value=0.1, value=45.0)
        with col_r3: p_r3 = st.number_input("Precio 51-100 pzs:", min_value=0.1, value=40.0)
        with col_r4: p_r4 = st.number_input("Precio 101+ pzs:", min_value=0.1, value=35.0)

        if st.button("💾 GUARDAR NUEVO PRODUCTO"):
            if nom_nuevo:
                CATALOGO_PRODUCTOS[nom_nuevo] = {
                    "cod": cod_sugerido, "rango1": p_r1, "rango2": p_r2, "rango3": p_r3, "rango4": p_r4,
                    "tipo": tipo_nuevo, "cat": gen_nuevo
                }
                guardar_catalogo_dict(CATALOGO_PRODUCTOS)
                st.success(f"¡Producto '{nom_nuevo}' registrado!")
                st.rerun()

        st.divider()
        st.markdown("#### **2. Edición Masiva de Precios por Escalas**")
        df_cat_edit = pd.DataFrame([
            {
                "Código": v["cod"], "Producto": k, "Categoría": v["cat"], "Tipo": v["tipo"],
                "1-6 pzs ($)": v["rango1"], "7-50 pzs ($)": v["rango2"],
                "51-100 pzs ($)": v["rango3"], "101+ pzs ($)": v["rango4"]
            }
            for k, v in CATALOGO_PRODUCTOS.items()
        ])
        
        cat_modificado = st.data_editor(df_cat_edit, use_container_width=True, num_rows="dynamic")
        
        if st.button("💾 GUARDAR CAMBIOS MASIVOS EN EL CATÁLOGO"):
            dict_act = {}
            for _, r in cat_modificado.iterrows():
                dict_act[r["Producto"]] = {
                    "cod": r["Código"], "rango1": float(r["1-6 pzs ($)"]), "rango2": float(r["7-50 pzs ($)"]),
                    "rango3": float(r["51-100 pzs ($)"]), "rango4": float(r["101+ pzs ($)"]),
                    "tipo": r["Tipo"], "cat": r["Categoría"]
                }
            guardar_catalogo_dict(dict_act)
            st.success("¡Catálogo Actualizado!")
            st.rerun()

# ------------------------------------------
# TAB 4: HISTORIAL Y PANEL FINANCIERO
# ------------------------------------------
with tab4:
    st.markdown("### 📊 HISTORIAL DE VENTAS Y SALDOS")
    pass_hist = st.text_input("Contraseña Admin Finanzas:", type="password", key="pass_hist_key")
    
    if pass_hist == PASSWORD_ADMIN:
        st.success("Acceso Concedido")
        if os.path.exists(HISTORIAL_FILE):
            try:
                df_h_ver = pd.read_csv(HISTORIAL_FILE, on_bad_lines='skip')
                st.dataframe(df_h_ver, use_container_width=True)
                
                col_k1, col_k2 = st.columns(2)
                with col_k1:
                    if "Total" in df_h_ver.columns:
                        st.metric("VENTAS TOTALES ACUMULADAS:", f"${df_h_ver['Total'].sum():.2f} MXN")
                with col_k2:
                    if "Saldo Pendiente" in df_h_ver.columns:
                        st.metric("SALDOS POR COBRAR EN ENTREGAS:", f"${df_h_ver['Saldo Pendiente'].sum():.2f} MXN")
            except Exception as e:
                st.error("Elimina el archivo 'historial_ventas.csv' de la carpeta para actualizar la tabla.")
        else:
            st.info("No hay historial registrado.")