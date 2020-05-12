![Site to Site VPN Hub Change Demo]
# Demo of Meraki Dashboard API Site to Site Hub Change

Este archivo realiza cambios para las redes especificadas en un archivo .csv (Sites.CSV) para ser actualizadas al hub indicado y para ello se requiere obtener una lista de las redes configuradas en el Dashboard la cual se almacena en disco como NetSummary.csv y extrae la lista de Hubs existente para seleccionar el Hub destino.


Existen 3 funciones:

1) Listar Redes y Hubs en archivo csv. 
 La primer opción crea el arvhivo NetSummary.csv con la integración de la red y el contenido de la VPN sitio a sitio de cada red, así como un archivo HubList.csv que contiene la información únicamente de los Hubs.

 Esta opción también permite actualizar las etiquetas (Tags) a las redes para diferenciar sitios entre Spokes, Hubs y NoVPN adicionalmente permite agregar las etiquetas específicas a los Hubs diferenciando entre Principal y  Secundario mediante la búsqueda del texto BCKUP en el nombre.

 Los archivos a entregar y presentan las actualizaciones.

2) Cambiar VPNs de Hub
 Esta opción permite ser ejecutada desde el principio si es que ya existe un archivo que contenga a los Hubs (buscando por defect el archivo HubList.csv y que requiere de un archivo (Sites.csv) donde se encuentren los sitios enlistados a moverse al hub destino.

 La lista de sitios (Sites.csv por defecto) es evaluada para filtrar cualquier sitio que no contenga un appliance, que ya se encuentra configurado con el Hub en primario  o que se haya incluido un sitio que es hub en la lista. Esta lista actualizada se guarda con el nombre original y se hace una copia del original agregando "_old" al archivo respaldado.

 Adicionalmente se actualizan las etiquetas para identificar las sucursales que están referenciadas al Hub Primario o Backup mediante las etiquetas VPN@Primario y VPN@Backup de manera mutuamente excluyente.

3) Salir
 Opción que como su nombre lo dice permite terminar el programa y salir de la ejecución del mismo.


### Mejoras propuestas

1. Leer archivo con credenciales utilizando el ConfigParser o importando el archivo con terminación .py
2. Enlistar los Hubs y seleccionarlos por número, como en las organizaciones, en lugar de agregar el ID de cada Hub
3. Pedir el hub origen y seleccionar los sitios a moverse al otro Hub deseado tomando el archivo NetSummary.csv como entrada y filtrando los sitios en la columna hubPriName