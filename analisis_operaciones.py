from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATOS = Path("datos/Online Retail.xlsx")
RESULTADOS = Path("resultados")
RESULTADOS.mkdir(exist_ok=True)

datos = pd.read_excel(DATOS)

# Limpieza inicial
datos = datos.drop_duplicates().copy()
datos["InvoiceNo"] = datos["InvoiceNo"].astype(str)
datos["EsCancelacion"] = datos["InvoiceNo"].str.startswith("C")
datos["Importe"] = datos["Quantity"] * datos["UnitPrice"]
datos["Periodo"] = datos["InvoiceDate"].dt.to_period("M").astype(str)

datos["EsVentaValida"] = (
    (~datos["EsCancelacion"])
    & (datos["Quantity"] > 0)
    & (datos["UnitPrice"] > 0)
)

ventas = datos[datos["EsVentaValida"]].copy()

# KPI
facturacion_total = ventas["Importe"].sum()
pedidos = ventas["InvoiceNo"].nunique()
unidades_vendidas = ventas["Quantity"].sum()
ticket_promedio = ventas.groupby("InvoiceNo")["Importe"].sum().mean()
clientes_activos = ventas["CustomerID"].nunique()

facturas_totales = datos["InvoiceNo"].nunique()
facturas_canceladas = datos.loc[
    datos["EsCancelacion"], "InvoiceNo"
].nunique()

tasa_cancelacion = facturas_canceladas / facturas_totales * 100

print("Facturación total:", round(facturacion_total, 2))
print("Pedidos:", pedidos)
print("Unidades vendidas:", unidades_vendidas)
print("Ticket promedio:", round(ticket_promedio, 2))
print("Clientes activos:", clientes_activos)
print("Tasa de cancelación:", round(tasa_cancelacion, 2), "%")

# Resumen mensual
resumen_mensual = (
    ventas.groupby("Periodo")
    .agg(
        Facturacion=("Importe", "sum"),
        Pedidos=("InvoiceNo", "nunique"),
        Unidades=("Quantity", "sum"),
        Clientes=("CustomerID", "nunique")
    )
    .reset_index()
)

resumen_mensual["TicketPromedio"] = (
    resumen_mensual["Facturacion"] /
    resumen_mensual["Pedidos"]
)

resumen_mensual.to_csv(
    RESULTADOS / "resumen_mensual.csv",
    index=False,
    encoding="utf-8-sig"
)

# Facturación mensual
plt.figure(figsize=(11, 5))
plt.plot(
    resumen_mensual["Periodo"],
    resumen_mensual["Facturacion"],
    marker="o"
)
plt.title("Facturación mensual")
plt.xlabel("Mes")
plt.ylabel("Facturación (£)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(
    RESULTADOS / "01_facturacion_mensual.png",
    dpi=160,
    bbox_inches="tight"
)
plt.close()

# Pedidos mensuales
plt.figure(figsize=(11, 5))
plt.plot(
    resumen_mensual["Periodo"],
    resumen_mensual["Pedidos"],
    marker="o"
)
plt.title("Cantidad de pedidos por mes")
plt.xlabel("Mes")
plt.ylabel("Pedidos")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(
    RESULTADOS / "02_pedidos_mensuales.png",
    dpi=160,
    bbox_inches="tight"
)
plt.close()

# Ticket promedio mensual
plt.figure(figsize=(11, 5))
plt.plot(
    resumen_mensual["Periodo"],
    resumen_mensual["TicketPromedio"],
    marker="o"
)
plt.title("Ticket promedio mensual")
plt.xlabel("Mes")
plt.ylabel("Ticket promedio (£)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(
    RESULTADOS / "03_ticket_promedio_mensual.png",
    dpi=160,
    bbox_inches="tight"
)
plt.close()

# Top 10 países
top_paises = (
    ventas.groupby("Country")["Importe"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))
plt.barh(top_paises.index, top_paises.values)
plt.title("Top 10 países por facturación")
plt.xlabel("Facturación (£)")
plt.ylabel("País")
plt.tight_layout()
plt.savefig(
    RESULTADOS / "04_top10_paises_facturacion.png",
    dpi=160,
    bbox_inches="tight"
)
plt.close()

# Top 10 productos
conceptos_no_producto = {
    "DOTCOM POSTAGE",
    "POSTAGE",
    "Manual",
    "CARRIAGE",
    "BANK CHARGES",
    "AMAZON FEE"
}

ventas_productos = ventas[
    ~ventas["Description"].fillna("").isin(conceptos_no_producto)
]

top_productos = (
    ventas_productos.groupby("Description")["Importe"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(11, 6))
plt.barh(top_productos.index, top_productos.values)
plt.title("Top 10 productos por facturación")
plt.xlabel("Facturación (£)")
plt.ylabel("Producto")
plt.tight_layout()
plt.savefig(
    RESULTADOS / "05_top10_productos_facturacion.png",
    dpi=160,
    bbox_inches="tight"
)
plt.close()

print("Resultados guardados en la carpeta resultados.")
