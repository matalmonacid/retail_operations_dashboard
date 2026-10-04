# Guía rápida de Power BI

## Archivo de entrada

Importar:

`datos/retail_operaciones_powerbi.csv`

## Tipos de datos recomendados

- Factura: texto
- CodigoProducto: texto
- Descripcion: texto
- Cantidad: número entero
- FechaHora: fecha/hora
- Fecha: fecha
- Año: número entero
- NumeroMes: número entero
- Mes: texto
- Periodo: texto
- PrecioUnitario: número decimal
- Cliente: texto
- Pais: texto
- Importe: número decimal
- EsCancelacion: verdadero/falso
- EsVentaValida: verdadero/falso

Si Power BI interpreta mal los decimales de `PrecioUnitario` o `Importe`, usar:

**Cambiar tipo → Usar configuración regional → Número decimal → Inglés (Reino Unido)**

## KPI

Crear las medidas incluidas en `medidas_dax.txt`.

Tarjetas recomendadas:

- Facturación Total
- Pedidos
- Unidades Vendidas
- Ticket Promedio
- Clientes Activos
- Tasa de Cancelación

## Gráficos

### Facturación mensual

- Visual: gráfico de líneas
- Eje X: Periodo
- Eje Y: Facturación Total
- Orden: Periodo ascendente

### Pedidos mensuales

- Visual: gráfico de líneas
- Eje X: Periodo
- Eje Y: Pedidos
- Orden: Periodo ascendente

### Top 10 países por facturación

- Visual: gráfico de barras agrupadas
- Eje Y: Pais
- Eje X: Facturación Total
- Filtro: Top N = 10 por Facturación Total
- Orden: descendente

### Top 10 productos por facturación

- Visual: gráfico de barras agrupadas
- Eje Y: Descripcion
- Eje X: Facturación Total
- Filtro: Top N = 10 por Facturación Total
- Orden: descendente

Para analizar productos físicos, se recomienda excluir conceptos como:
`DOTCOM POSTAGE`, `POSTAGE`, `Manual`, `CARRIAGE`, `BANK CHARGES` y `AMAZON FEE`.

## Nota de interpretación

Diciembre de 2011 es un período incompleto: el dataset contiene datos solamente hasta el 9 de diciembre de 2011.
