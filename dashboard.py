#!/usr/bin/env python3
import datetime
import requests

base_url = 'https://api.meraki.com/api/v0'


# Mostrar las organizaciones a las que el api_key tiene acceso
# https://api.meraki.com/api_docs#list-the-organizations-that-the-user-has-privileges-on
def get_user_orgs(api_key):
    get_url = f'{base_url}/organizations'
    headers = {'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'}

    response = requests.get(get_url, headers=headers)
    data = response.json() if response.ok else response.text
    return (response.ok, data)


# Mostrar las redes de la organización
# https://api.meraki.com/api_docs#list-the-networks-in-an-organization
def get_networks(api_key, org_id, configTemplateId=None):
    get_url = f'{base_url}/organizations/{org_id}/networks'
    headers = {'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'}
    if configTemplateId:
        get_url += f'?configTemplateId={configTemplateId}'
    response = requests.get(get_url, headers=headers)
    data = response.json() if response.ok else response.text
    return (response.ok, data)

# Mostrar la configuración de las VPNs Sitio a Sitio de una red
# https://dashboard.meraki.com/api_docs/v0#return-the-site-to-site-vpn-settings-of-a-network
def getNetSiteToSite(api_key, org_id, net_id):
    get_url = f'{base_url}/organizations/{org_id}/networks/{net_id}/siteToSiteVpn'
    headers = {'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'}
    response = requests.get(get_url, headers=headers)
    data = response.json() if response.ok else response.text
    return (response.ok, data)


# Crear una red
# https://api.meraki.com/api_docs#create-a-network
def create_network(api_key, org_id, name, net_type='wireless', tags='', copyFromNetworkId=None, timeZone='America/Los_Angeles'):
    post_url = f'{base_url}/organizations/{org_id}/networks'
    headers = {'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'}
    #convierte los tags de una lista en String ya que el API así lo requiere
    if tags and type(tags) == list:
        tags = ' '.join(tags)
    #Mapear las variables locales a su respectiva llave dentro del diccionario
    vars = locals()
    params = ['name', 'tags', 'timeZone', 'copyFromNetworkId']
    payload = dict((k, vars[k]) for k in params)
    #Agrega una lista al diccionario en la llave 'type' debido a que la función anterior no mapea listas, sólo strings
    payload['type'] = net_type

    response = requests.post(post_url, headers=headers, json=payload)
    data = response.json() if response.ok else response.text
    return (response.ok, data)

# Parpadear LEDs en el dispositivo
# https://api.meraki.com/api_docs#blink-the-leds-on-a-device
def blink_device(api_key, net_id, serial, duration=20, period=160, duty=50):
    post_url = f'{base_url}/networks/{net_id}/devices/{serial}/blinkLeds'
    headers = {'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'}
    #Mapear las variables locales a su respectiva llave dentro del diccionario
    vars = locals()
    params = ['duration', 'period', 'duty']
    payload = dict((k, vars[k]) for k in params)

    response = requests.post(post_url, headers=headers, json=payload)
    data = response.json() if response.ok else response.text
    return (response.ok, data)

# Actualizar los hubs de Auto-VPN de una red
# https://dashboard.meraki.com/api_docs/v0#update-the-site-to-site-vpn-settings-of-a-network
def updateHubsVPN(api_key, org_id, net_id, mode, hubPriId, hubPriFullTunnel='False', hubBkpId='', hubBkpFullTunnel='False'):
    put_url = f'{base_url}/organizations/{org_id}/networks/{net_id}/siteToSiteVpn'
    headers = {'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'}
    #Actualizando sólo los Hubs a los que se conecta el
    payload = {
        "mode":mode,
        "hubs":[
          {
            "hubId": hubPriId,
            "useDefaultRoute": hubPriFullTunnel
          },
          {
            "hubId": hubBkpId,
            "useDefaultRoute": hubBkpFullTunnel
          }
        ]
    }
    response = requests.put(put_url, headers=headers,json=payload)
    data = response.json() if response.ok else response.text
    return (response.ok, data)

# Actualizar la información de una Red
# https://dashboard.meraki.com/api_docs/v0#update-a-network
def updateNetTags(api_key, org_id, net_id, tags):
    put_url = f'{base_url}/organizations/{org_id}/networks/{net_id}'
    headers = {'X-Cisco-Meraki-API-Key': api_key, 'Content-Type': 'application/json'}
    if tags and type(tags) == list:
        tags = ' '.join(tags)
    payload = {'tags':tags}
    response = requests.put(put_url, headers=headers,json=payload)
    data = response.json() if response.ok else response.text
    return (response.ok, data)
