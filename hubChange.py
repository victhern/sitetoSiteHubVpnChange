import csv
import json
from json.decoder import JSONDecodeError
import os
import random
import time
import datetime
import sys

from progress.bar import ShadyBar
from progress.spinner import PieSpinner

from dashboard import *


# Helper function to get siteToSiteVpn
def getNetName(net_id, networks):
    net_ids = [network['id'] for network in networks]
    for i in networks:
        if net_id in net_ids:
            net_name = networks[net_ids.index(net_id)].get("name")
    return (net_name)

def pausa():
    print()
    pause = input('Continuar? (S/N)')
    if pause == 'S':
        print('Continuando')
    elif pause == 's':
        print('Continuando')
    else:
        sys.exit()

def cleanScreen():
    # Clear Screen for windows
    if os.name == 'nt':
        os.system('cls')

    # Clear Screenfor mac and linux(here, os.name is 'posix')
    else:
        os.system('clear')
    print()
    print()
    print('                               ##       ##  #########  ########       ##     ##    ##  ######')
    print('                               ####   ####  ###        ##     ##    ##  ##   ##   ##     ##  ')
    print('                               ## ## ## ##  ##         ##     ##   ##    ##  ##  ##      ##  ')
    print('                               ##  ##   ##  #######    ######      ########  #####       ##  ')
    print('                               ##       ##  ##         ##    ##    ##    ##  ##  ##      ##  ')
    print('                               ##       ##  ###        ##     ##   ##    ##  ##   ##     ##  ')
    print('                               ##       ##  #########  ##      ##  ##    ##  ##    ##  ######')
    print()
    print('                                        Desarrollo de API para Farmacias del Ahorro             ')
    print('                                  Por Victor Hernandez CSE Cisco Meraki victhern@cisco.com         ')
    print()
    print()

def fileVersioning(fileToKeep):
    str1 = fileToKeep
    try:
        x = 0
        for i in range(10):
            x += str1.count(str(i))
            ini = len(str1)-x-4
            fin = len(str1)-4
            str2 = str1[ini:fin]
        y = int(str2)
        y += 1
        newStr = "_old"+str(y)
        if y == 1:
            oldStr = "_old"
        else:
            oldStr = "_old"+str(y-1)
            fileToKeep = fileToKeep.replace(oldStr, newStr)
    except:
        y = 1
        newStr = "_old"+str(y)
        fileToKeep = fileToKeep.replace("_old", newStr)
    return(fileToKeep)

def main():

    args = sys.argv

    cleanScreen()

    SiSubrayada = "\u0332".join("Si ")
    NoSubrayada = "\u0332".join("No ")
    api_key = None
    org_id = None
    user_name = None

    if 'test' in args:
        # api_key = '15e8d3c9a4e8b44241800fcb92065883b01e8409'
        # org_id = '578350'
        # user_name = 'VicMac'
        print('                                   **********       --- Test Mode ---       **********')
    # Obtener nombre y TAGs personalizados
    print()
    print()
    if user_name == None:
        print('                                  **********       Bienvenido  Mi Señor       **********')
        print()
        print()
        user_name = input('Mi Señor, deseo conocerlo mejor, por favor introduzca su(s) nombre(s): ')
        print()
        print(f'De acuerdo Mi Señor {user_name}' )# Obtener API Key y validar acceso a la organizacion
    else:
        print(f'                           **********       Bienvenido de vuelta Mi Señor {user_name}      **********')
        print()
        print()
        print()
    if api_key == None:
        while True:
            print()
            api_key = input(f'Mi Señor {user_name}, Introduzca su API key, por favor: ')
            (ok, orgs) = get_user_orgs(api_key)
            if ok:
                break
            else:
                print(f'Disculpe Mi Señor {user_name} no puedo proceder, el API key es incorrecto o creado recientemente, en cuyo caso le solicito reintentar de nuevo en otro momento')
    else:
        while True:
            print()
            (ok, orgs) = get_user_orgs(api_key)
            if ok:
                break
            else:
                print(f'Disculpe Mi Señor {user_name} no puedo proceder, el API key es incorrecto o creado recientemente, en cuyo caso le solicito reintentar de nuevo en otro momento')
                print()
                api_key = input(f'Mi Señor {user_name}, Introduzca su API key, por favor: ')

    # Obteniendo el ID de la organizacion
    org_ids = []
    if org_id == None:
        print('Se muestran las organizaciones a las que puede acceder, Mi Señor, se muestran los IDs & nombres, respectivamente:')
        i = 0
        for org in orgs:
            org_id = org["id"]
            org_ids.append(str(org_id))
            print(f'{i}) {org_id:18}\t{org["name"]}')
            i+=1
        print()
        while True:
            org_id = input('Introduzca el ID de la Org en que desea trabajar - Mi Señor: ')
            if org_id.isnumeric():
                i=int(org_id)
                if i<len(orgs):
                    org_id = orgs[i].get("id")
            elif ")" in org_id:
                org_id = org_id.strip()
                org_id = org_id[0:org_id.find(")")]
                i=int(org_id)
                org_id = orgs[i].get("id")

            if org_id in org_ids:
                break
            else:
                print('Disculpe Mi Señor no encuentro esa Org, por favor intente de nuevo!')
    cleanScreen()
    for org in orgs:
        if org_id == org["id"]:
            org_name = org["name"]
            print()
            print(' @@@@@ La org seleccionada es @@@@@')
            print(f' ********    {org_name}    ******** ')
    print()
    # Obteniendo las redes a utilizar para las actividades

    print(' @@@ Leyendo redes del Dashboard @@@ ')
    print()
    (ok, data) = get_networks(api_key,org_id)
    if not ok:
        sys.exit(data)
    else:
        networks = data
        print(f' ### {len(networks)} redes enccontradas en el Dashboard ###')

    # Menú de Opciones
    while True:
        if 'test' not in args:
            mytime = datetime.datetime.now()
            try:
                ask = input(f'¿Deseas actualizar la fecha {timestamp} para una nuevo proceso? (Si /{NoSubrayada})')
                ask.lower()
                if 's' in ask:
                    timestamp = mytime.strftime('%Y%m%d_%H%M')
                print(f' ### Se añadirá la fecha y hora {timestamp} para cada archivo creado en esta sesión ###')
            except:
                timestamp = mytime.strftime('%Y%m%d_%H%M')
                print(f' ### Se añadirá la fecha y hora {timestamp} para cada archivo creado en esta sesión ###')

        print()
        print(f'Mi Señor {user_name}, Indique lo que desea hacer:')
        print()
        print('1) Listar Redes y Hubs en archivo csv')
        print('2) Cambiar VPNs de Hub')
        print('3) Salir')
        print()
        stop = input('Su respuesta:')
        stop = stop.lower()
        stop = stop.replace(' ', '')

        if 'listar' in stop:
            stop = '1'
        elif 'cambiar' in stop:
            stop = '2'
        elif 'salir' in stop:
            stop = '3'

        # 1) Listar Redes y Hubs
        # 2) Cambiar VPNs de Hub
        # 3) Salir
        if stop == '1':
        #Para crear el listado de redes es necesario leer las redes y agregar la información de las VPNs

        #### Crear tabla de redes en .csv
            newHeader = list(networks[0].keys())
            for i in range(1, len(networks)):
                x = len(networks[i-1].keys())
                y = len(networks[i].keys())
                if y-x == 1:
                    newHeader = list(networks[i].keys())
            newHeader.append('mode')               #Json Attribute is mode
            newHeader.append('hubPriId')           #Json Attribute is in hubs[hubId]
            newHeader.append('hubPriName')           #Json Attribute is in hubs[hubId]
            newHeader.append('hubPriFullTunnel')   #Json Attribute is in hubs[useDefaultRoute]
            newHeader.append('hubBkpId')           #Json Attribute is in hubs[hubId]
            newHeader.append('hubBkpName')           #Json Attribute is in hubs[hubId]
            newHeader.append('hubBkpFullTunnel')   #Json Attribute is in hubs[useDefaultRoute]
            newHeader.append('hubBk2Id')           #Json Attribute is in hubs[hubId]
            newHeader.append('hubBk2Name')           #Json Attribute is in hubs[hubId]
            newHeader.append('hubBk2FullTunnel')   #Json Attribute is in hubs[useDefaultRoute]
            countOfNets = len(networks)

            if 'test' in args:
                testNetMax = 50 # Máximo de redes a procesar en modo prueba
                filename = './NetSummary.csv'
                hubFileName = './HubList.csv'
                if countOfNets > testNetMax:
                    print(f'  @@@ Para el Modo Prueba sólo se realizan máximo {testNetMax} redes @@@')
                    continuar = input(f' ¿Desea procesar el total de redes {countOfNets}? (Si /{NoSubrayada})')
                    continuar = continuar.lower()
                    if continuar != 's':
                        countOfNets = testNetMax
                print()
                print()

            else:
                filename = './'+org_name+'_NetSummary_'+timestamp+'.csv'
                hubFileName = './'+org_name+'_HubList_'+timestamp+'.csv'
            setTag = input(f'  ¿Desea actualizar los tags de cada red para indicar si son "Hubs", "Spokes" o "noVPN"? ({SiSubrayada}/No )')
            setTag.lower()
            if 'n' in setTag:
                setTag = 'n'
            else:
                setTag = 's'

            outputFile = open(filename, 'w', newline='\n', encoding='utf-8-sig')
            output = csv.writer(outputFile)

            newHeader = list(dict.fromkeys(newHeader))

            output.writerow(newHeader) #headers
            hubFile = open(hubFileName, 'w', newline='\n', encoding='utf-8-sig')
            hubWriter = csv.writer(hubFile)
            hubheader =['id','name','mode', 'dcType', 'tags']
            hubWriter.writerow(hubheader)
            hubs = dict()
            rowHubs = {'id' : "", 'name' : "", 'mode' : "", 'dcType' : "", 'tags' : ""}
            hubTag = "Hub"
            spokeTag = "Spoke"
            noVPNTag = "noVPN"
            hub_tags = []
            hubtable = [{}]
            templateId = ''
            row = {}
            bar=ShadyBar('Procesando información de VPNs', max=countOfNets, suffix = 'quedan %(remaining)d de %(max)d avance del %(percent).1f%%, se estima terminar en %(eta)ds')
            if 'test' in args:
                j = 0
            for net in networks:
                net_id = net.get("id")
                if "configTemplateId" in newHeader:
                    templateId = '' if net.get("configTemplateId") is None else net.get("configTemplateId")
                    net.update({"configTemplateId" : templateId})
                if "appliance" in net.get("productTypes"):
                    (ok, netVPN) = getNetSiteToSite(api_key,org_id,net_id)
                    if not ok:
                        sys.exit(netVPN)
                    else:
                        netcfg = netVPN
                    mode = netcfg.get("mode")
                    #Crear tabla de hubs
                    if mode != 'none':
                        net['mode'] = mode
                        if mode == "hub":
                            net_name = hub_name = net.get("name")
                            net_name = hub_name.lower()
                            if "bckup" in net_name:
                                hub_dcType = "Secundario"
                            else:
                                hub_dcType = "Principal"

                            if 's' in setTag:
                                str1 = net["tags"].strip()
                                hub_tags = str1.split()
                                if not hubTag in hub_tags:
                                    hub_tags.append(hubTag)
                                if spokeTag in hub_tags:
                                    hub_tags.remove(spokeTag)
                                if noVPNTag in hub_tags:
                                    hub_tags.remove(noVPNTag)
                                if "Principal" in hub_tags:
                                    hub_tags.remove("Principal")
                                if "Secundario" in hub_tags:
                                    hub_tags.remove("Secundario")
                                hub_tags.append(hub_dcType)

                                net['tags'] = ' '.join(hub_tags)
                                ### Actualizar Tags de Hub
                                (ok,network)=updateNetTags(api_key,org_id,net_id,hub_tags)
                                if not ok:
                                    sys.exit(network)
                            rowHubs = {
                                'id': net_id,
                                'name': hub_name,
                                'mode': mode,
                                'dcType': hub_dcType,
                                'tags': ' '.join(hub_tags)
                            }
                            hubtable.append(rowHubs)
                            hubWriter.writerow(rowHubs.values())
                        elif mode == "spoke":
                            if 's' in setTag:
                                str1 = net["tags"].strip()
                                net_tags = str1.split()
                                if not spokeTag in net_tags:
                                    net_tags.append(spokeTag)
                                elif hubTag in net_tags:
                                    net_tags.remove(hubTag)
                                elif noVPNTag in net_tags:
                                    net_tags.remove(noVPNTag)

                                net['tags'] = ' '.join(net_tags)
                                ### Actualizar Tags de Red
                                (ok,network)=updateNetTags(api_key,org_id,net_id,net_tags)
                                if not ok:
                                    sys.exit(network)
                        hubs=netcfg['hubs']
                        if len(hubs) > 2:
                            net['hubBk2Id'] = hubs[2].get("hubId")
                            net['hubBk2Name'] = getNetName(hubs[2].get("hubId"),networks)
                            net['hubBk2FullTunnel'] = hubs[2].get("useDefaultRoute")
                        if len(hubs) > 1:
                            net['hubBkpId'] = hubs[1].get("hubId")
                            net['hubBkpName'] = getNetName(hubs[1].get("hubId"),networks)
                            net['hubBkpFullTunnel'] = hubs[1].get("useDefaultRoute")
                        if len(hubs) > 0:
                            net['hubPriId'] = hubs[0].get("hubId")
                            net['hubPriName'] = getNetName(hubs[0].get("hubId"),networks)
                            net['hubPriFullTunnel'] = hubs[0].get("useDefaultRoute")
                    else:
                        if 's' in setTag:
                            str1 = net["tags"].strip()
                            net_tags = str1.split()
                            if not noVPNTag in net_tags:
                                net_tags.append(noVPNTag)
                            elif spokeTag in net_tags:
                                net_tags.remove(spokeTag)
                            elif hubTag in net_tags:
                                net_tags.remove(hubTag)
                            net['tags'] = ' '.join(net_tags)
                            ### Actualizar Tags de Red
                            (ok,network)=updateNetTags(api_key,org_id,net_id,net_tags)
                            if not ok:
                                sys.exit(network)

                        net['mode'] = ''
                        net['hubPriId'] = ''
                        net['hubPriFullTunnel'] = ''
                        net['hubBkpId'] = ''
                        net['hubBkpFullTunnel'] = ''
                        net['hubBk2Id'] = ''
                        net['hubBk2FullTunnel'] = ''

                for i in range(len(newHeader)):
                    row[newHeader[i]] = net.get(newHeader[i])
                output.writerow(row.values())

                time.sleep(0.005)# Only 5 requests per second
                bar.next()
                if 'test' in args:  #Limit repetition to 200 devices
                    if j >= countOfNets - 1:
                        break
                    else:
                        j += 1
            bar.finish()
            outputFile.close()
            hubFile.close()
            cleanScreen()
            print(f'Mi Señor, el proceso de información de VPNs tomó {bar.elapsed}s en terminar')
            print()
            print('Abajo la lista de Hubs obtenida')
            print('\tID de Red\t\tNombre de Red\t\t\tEtiquetas\t\tTipo de DC')
            if not hubtable[0]:
             hubtable.pop(0)
            for hub in hubtable:
                print(f'\t{hub["id"]:20}\t{hub["name"]:25}\t{hub["tags"]:20}\t{hub["dcType"]}')
            print()
            print(f'Mi Señor {user_name} recuerde revisar su trabajo en los archivos \n{filename}\n{hubFileName}')


        # 1) Listar Redes y Hubs
        # 2) Cambiar VPNs de Hub
        # 3) Salir
        if stop == '2':
            if 'test' in args:
                hubFileName = 'HubList.csv'
                print()
                print(f'   Mi Señor {user_name} se utilizará la información en {hubFileName} para procesar los hubs')
                file1 = "NetSummary.csv"
                file2 = "Sites.csv"
                print()
                print(f'@@@ Realizando copia de archivo {file1} a {file2} para pruebas @@@')
                os.system("cp "+file1+" "+file2)

            else:
                fileNames = os.listdir(os.getcwd())
                for name in fileNames:
                    print(name)
                hubFileName = 'HubList.csv'
                hubFileNameU = "\u0332".join(hubFileName)
                response = input(f' Mi Señor, por favor indique el archivo que contiene los Hubs actualizados ({hubFileNameU} por defecto): ')
                fileName = response
                if response != "":
                    hubFileName = response

                hubFileName = './'+hubFileName

            hubHeader =['id','name','mode', 'dcType', 'tags']
            rowHubs = {'id' : "", 'name' : "", 'mode' : "", 'dcType' : "", 'tags' : ""}

            hub_ids = []

            cleanScreen()
            try:
                if not hubtable[0]:
                    hubtable.pop(0)
                print('@@@ Leyendo desde memoria en hubtable @@@')

            except (UnboundLocalError, NameError):
                print(f' @@@ Leyendo desde archivo {hubFileName} @@@')
                hubtable = []
                with open(hubFileName,  newline='\n', encoding='utf-8-sig') as hubFileRd:
                    hubReader = csv.DictReader(hubFileRd, fieldnames=(hubHeader), delimiter=',', quotechar='"')
                    hubHeader = next(hubReader)
                    for hub in hubReader:
                        hub_id = hub['id']
                        net_name = hub_name = hub['name']
                        mode = hub['mode']
                        hub_tags = hub['tags']
                        hub_dcType = hub['dcType']
                        rowHubs = {
                            'id': hub_id,
                            'name': hub_name,
                            'mode': mode,
                            'dcType': hub_dcType,
                            'tags': hub_tags
                        }
                        hubtable.append(rowHubs)
                hubFileRd.close()
                if not hubtable:
                    cleanScreen()
                    print()
                    print()
                    print(f' ¡¡¡¡####                                 ERROR                                 ####!!!!')
                    print(f' ¡¡¡¡####            {hubFileName} es un valor de archivo incorrecto            ####!!!!')
                    print(f' ¡¡¡¡####                                                                       ####!!!!')
                    print(f' ¡¡¡¡####  Para analizar la red y crear el archivo desde la org del Dashboard   ####!!!!')
                    print(f' ¡¡¡¡####                     Por Favor utilice la opción 1                     ####!!!!')
                    print(f' ¡¡¡¡####                                                                       ####!!!!')
                    print()
                    time.sleep(5)
                    continue

            #Mostrar la lista de hubs de manera lineal
            print('\tID de Red\t\tNombre de Red\t\t\tEtiquetas\t\tTipo de DC')
            if not hubtable[0]:
             hubtable.pop(0)
            for hub in hubtable:
                hub_ids.append(hub["id"])
                print(f'\t{hub["id"]:20}\t{hub["name"]:25}\t{hub["tags"]:20}\t{hub["dcType"]}')
            print()
            while True:
                hub_id = input(f'\t\tMi Señor {user_name}, Por favor introduza el ID del Hub al que desea apuntar sus sucursales: ')
                if hub_id in hub_ids:
                    break
                else:
                    print()
                    print('Disculpe Mi Señor no encuentro ese Hub, por favor intente de nuevo!')
                    hub_id = ""

            hub_name = getNetName(hub_id, hubtable)
            cleanScreen()
            print()
            print(f'    Me queda claro, se ha seleccionado "{hub_name}" como el objetivo')
            print()

            #Leer el archivo de ingreso de Redes
            correcto = "n"
            sites = []
            site_ids = []
            siteHeaders = []

            while True:
                fileNames = os.listdir(os.getcwd())
                for name in fileNames:
                    print(name)
                myFileName = ""
                oldFile = ""
                response = input(f' Mi Señor, por favor indique el archivo para el movimiento de DC (Sites.csv por defecto): ')
                myFileName = response
                response = response.lower()
                if response == "si" or response == "s" or response == "":
                    oldFile = "Sites_old.csv"
                    myFileName = "Sites.csv"
                elif ".csv" in myFileName and myFileName in fileNames:
                        oldFile = myFileName.replace(".", "_old.")
                else:
                        cleanScreen()
                        print()
                        print()
                        print(f' ¡¡¡¡####                                 ERROR                                 ####!!!!')
                        print(f' ¡¡¡¡####             {myFileName} es un valor de archivo incorrecto            ####!!!!')
                        print(f' ¡¡¡¡####                       Por Favor intente de nuevo                      ####!!!!')
                        print(f' ¡¡¡¡####                                                                       ####!!!!')
                        print()
                        continue

                while oldFile in fileNames:
                    oldFile = fileVersioning(oldFile)

                cleanScreen()
                correcto = input(f' Mi Señor, ¿Desea usar {myFileName} y respaldarlo en {oldFile}? (Si /{NoSubrayada})  ')
                correcto = correcto.lower()
                if "s" not in correcto:
                    continue
                else:
                    break

            print(f'@@@ Realizando respaldo de archivo {myFileName} a {oldFile} @@@')
            os.system("cp "+myFileName+" "+oldFile)

            #Leer información del archivo
            print()
            print(f' @@@ Leyendo desde archivo {myFileName} @@@')
            sitetable = []
            rowUpd = []
            with open("./"+myFileName,  newline='\n', encoding='utf-8-sig') as sitesFileRd:
                siteReader = csv.DictReader(sitesFileRd)
                #Construir Diccionario Tabla sitetable
                sitetable = [row for row in siteReader]
            sitesFileRd.close()

            try:
                siteHeaders = sitetable[0].keys()
            except:
                cleanScreen()
                print()
                print(f' ¡¡¡¡####                                 ERROR                                 ####!!!!')
                print(f' ¡¡¡¡####                   El archivo {myFileName} está vacío                  ####!!!!')
                print(f' ¡¡¡¡####                       Por Favor intente de nuevo                      ####!!!!')
                print(f' ¡¡¡¡####                                                                       ####!!!!')
                print()
                print(json.dumps(sitetable,indent=4))
                time.sleep(5)
                continue

            templList=[]
            if len(siteHeaders) < 19:
                print()
                print(f' ¡¡¡¡####                                 ERROR                                 ####!!!!')
                print(f' ¡¡¡¡####     El archivo {myFileName} no contiene la información  necesaria     ####!!!!')
                print(f' ¡¡¡¡####                       Por Favor intente de nuevo                      ####!!!!')
                print(f' ¡¡¡¡####                                                                       ####!!!!')
                print()
                continue
            elif "configTemplateId" in siteHeaders:
                print()
                print(f' ¡¡¡¡####                              PRECAUCIÓN                               ####!!!!')
                print(f' ¡¡¡¡####    Esta versión no actualiza plantillas, sólo redes independientes!   ####!!!!')
                print(f' ¡¡¡¡####                                                                       ####!!!!')


            ## Listando la información del archivo cargado en sitetable
            print()
            correcto = input(f' Mi Señor, ¿Desea mover el Hub Primario al Backup? ({SiSubrayada}/No ): ')
            correcto = correcto.lower()
            newSiteTable = []
            cleanScreen()
            print()
            print(f'  Mi Señor {user_name}, favor de validar la lista de redes a mover ')
            print()
            print("\u0332".join('\tID de Red\t\tNombre de Red\t\tHub Primario Actual\t-->\tHub Primario Deseado'))

            for site in sitetable:
                #Crear lista de ids a ejecutar
                site_id = site.get("id")
                site_name = site.get("name")
                site_tags = site.get("tags")
                site_templ = site.get("configTemplateId")
                site_mode = site.get("mode")
                site_priId = site.get("hubPriId")
                site_priName = site.get("hubPriName")
                site_priFul = site.get("hubPriFullTunnel")
                site_bkpId = site.get("hubBkpId")
                site_bkpName = site.get("hubBkpName")
                site_bkpFul = site.get("hubBkpFullTunnel")
                site['mode'] = site_mode
                site['hubPriId'] = hub_id
                site['hubPriName'] = hub_name
                site['hubPriFullTunnel'] = site_priFul
                if not site_templ and site_mode == "spoke" and site_priName != hub_name:
                    if "s" in correcto or "" in correcto:
                        site['hubBkpId'] = site_priId
                        site['hubBkpName'] = site_priName
                        site['hubBkpFullTunnel'] = site_priFul
                    ### Agregar el Tag "VPN@Backup" o "VPN@Primario"
                    str2 = hub_name.lower()
                    if "bckup" in str2:
                        siteTag = "VPN@Backup"
                    else:
                        siteTag = "VPN@Primario"
                    str1 = site['tags'].strip()
                    new_tags = str1.split()
                    if "VPN@Primario" in new_tags:
                        new_tags.remove("VPN@Primario")
                    if "VPN@Backup" in new_tags:
                        new_tags.remove("VPN@Backup")
                    new_tags.append(siteTag)
                    site['tags'] = ' '.join(new_tags)
                    newSiteTable.append(site) #generar tabla newSiteTable
                    print(f'{site_id:18}\t{site_name:25}\t{site_priName:20}\t-->\t{hub_name}')
                    site_ids.append(str(site_id)) # Registrar sólo los sitios que requieren cambio

                elif site_mode == "hub":
                    print(f'{site_id:18}\t{site_name:25}\t{site_priName:20}\t-->\tSin Cambio, ya es Hub')
                elif site_priName == hub_name:
                    print(f'{site_id:18}\t{site_name:25}\t{site_priName:20}\t==\t{hub_name} Sin Cambio')
                else:
                    print(f'{site_id:18}\t{site_name:25}\t{site_priName:20}\t-->\tSin Cambio {site_templ}')

            correcto = input(f' Mi Señor, ¿Desea Proceder con el movimiento? (Si /{NoSubrayada}): ')
            correcto.lower()
            if "s" not in correcto:
                continue
            # Abriendo archivo para guardan cambios
            sitesFileWr = open(myFileName, 'w', newline='\n', encoding='utf-8-sig')
            sitesWriter = csv.writer(sitesFileWr)
            sitesWriter.writerow(siteHeaders)
            print()

            bar=ShadyBar(f'Moviendo Hubs a {hub_name}', max=len(newSiteTable), suffix = 'quedan %(remaining)d de %(max)d avance del %(percent).1f%%, se estima terminar en %(eta)ds')
            for site in newSiteTable:
                siteId = site.get('id')
                siteTags = site.get('tags')
                siteMode = site.get('mode')
                sitePriId = site.get('hubPriId')
                sitePriFul = site.get('hubPriFullTunnel')
                siteBkpId = site.get('hubBkpId')
                siteBkpFul = site.get('hubBkpFullTunnel')

                ### Actualizar Tags de Hub
                (ok,network)=updateNetTags(api_key,org_id,siteId,siteTags)
                time.sleep(.05)

                #Actualizar la nueva información
                sitesWriter.writerow(site.values())

                ### Actualizar VPNs en Dashboard
                (ok, data)=updateHubsVPN(api_key,org_id,siteId,siteMode,sitePriId,sitePriFul,siteBkpId,siteBkpFul)
                time.sleep(.05)

                bar.next()
            bar.finish()
            sitesFileWr.close()

            print()
            print(f' ¡¡¡¡####                              Finalizado                               ####!!!!')
            print(f' ¡¡¡¡####           Mi Señor, la actualización tomó {bar.elapsed}s en terminar           ####!!!!')
            print(f' ¡¡¡¡####                Recuerde revisar los cambios en Dashboard              ####!!!!')
            print(f' ¡¡¡¡####           y en la actualización del archivo {myFileName}          ####!!!!')
            print()


         # 1) Listar Redes y Hubs
         # 2) Cambiar VPNs de Hub
         # 3) Salir
        if stop == '3':
            cleanScreen()
            print()
            print(f' ¡¡¡¡####           Mi Señor {user_name}, Muchas Gracias por llamarme recuerde que estoy a su servicio           ####!!!!')
            print()
            print()
            sys.exit()

    # Run the main function when opened

if __name__ == '__main__':
    main()
