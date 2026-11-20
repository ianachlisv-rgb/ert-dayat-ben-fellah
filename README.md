# Anomalías de resistividad en Dayat Ben Fellah (Argelia): ¿disolución, fracturas o cavidades?

Análisis de diez perfiles de tomografía de resistividad eléctrica (ERT, arreglo Wenner) en una depresión kárstica cerca de Guerrara (Ghardaïa), para identificar anomalías compatibles con disolución, fracturas o posibles cavidades y decir qué información falta para confirmarlas.

**Autor:** Ian A. Sandoval-Valderrábano, Facultad de Ingeniería, Benemérita Universidad Autónoma de Puebla (BUAP).

## Contenido
- [`paper/ERT_Dayat_Ben_Fellah_IEEE.pdf`](paper/ERT_Dayat_Ben_Fellah_IEEE.pdf): informe en formato IEEE (8 páginas).
- [`paper/overleaf/`](paper/overleaf): fuente LaTeX y figuras.

## Qué se hizo
- Ubicación de los diez perfiles en UTM 31N sobre imagen satelital; pseudosecciones y modelos con escala y unidades.
- Evaluación de la confiabilidad de cada modelo con seis indicadores (el RMS es solo uno).
- 14 anomalías candidatas en los modelos de Res2DInv (BF1 y BF2) con un criterio repetible.
- Inversión propia en Python de los diez perfiles y comparación con Res2DInv: 3 candidatas se reproducen, 5 en parte y 6 no.
- Modelo conceptual y plan de verificación (sondeos, georradar, microgravimetría).

Ninguna anomalía se presenta como cavidad comprobada.

## Código
- [`codigo/pseudosecciones_wenner.py`](codigo/pseudosecciones_wenner.py): lee archivos de datos en formato Res2DInv con arreglo Wenner (nombre, espaciamiento, tipo de arreglo, número de datos, filas x-a-ρa) y dibuja la pseudosección de cada perfil con escala logarítmica. Probado con los diez perfiles de Dayat Ben Fellah (el número de datos leído coincide con el del encabezado en todos).
  ```
  pip install numpy matplotlib
  python codigo/pseudosecciones_wenner.py carpeta_con_datos/ salida/
  ```
  La pseudoprofundidad es z = 0.519·a (Edwards, 1977): sirve para dibujar, no es la profundidad real.

## Qué no incluye
- Los datos de los perfiles y los modelos de Res2DInv son de terceros (literatura) y no se incluyen.
- El código de la inversión propia del informe no está en este repositorio. Una implementación de inversión ERT/IP en Python del mismo autor está en [`ert-ip-kuala-lumpur`](https://github.com/ianachlisv-rgb/ert-ip-kuala-lumpur).

## Licencia
El código está bajo licencia MIT (ver [`LICENSE`](LICENSE)). El texto y las figuras del informe son del autor; los datos originales y los modelos de Res2DInv pertenecen a sus autores. La imagen de fondo de la Fig. 1 es de Google Earth y está atribuida en la figura.
