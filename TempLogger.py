
import httplib
import urllib
import webbrowser
import json, random, time
#import serial


##################################################################################
# Using OAuth 2.0 for Installed Applications
#
# In this example we are using OAuth and Google APIs
# to create a spreadsheet in Google Drive prepopulated with 10 temperature samples
#
# Temperature data comes fasdfasdfasdfrom a LM35 sensor that is connected to an Arduino board.
# The Arduino board is connected to this script using a Serial communication
##################################################################################

def makeRequest(url, method = 'GET', body='', headers={}):
    partes = url.split('/')
    conn = None
    port = 80
    if partes[0] == "https:":
        conn = httplib.HTTPSConnection(partes[2])
        port = 443
    elif partes[0] == "http:":
        conn = httplib.HTTPConnection(partes[2])
    conn.connect()
    url2 = ''
    index = 3
    while index < len(partes):
        url2 += '/'+partes[index]
        index+=1
    headers['Content-length'] = str(len(body))
    conn.request(method=method, url=url2, body=body, headers=headers)
    resp = conn.getresponse()
    body = resp.read()
    conn.close()
    return (resp, body)

print('#####################################')
print('Getting temperature data from Arduino via Serial connection')
print('#####################################')
#com_port = serial.Serial('/dev/tty.usbmodem1411', 9600)

temperature = ''
while True:
    #temperature = float(com_port.readline())
    temperature = random.random() * 40
    print str(temperature)
    response, edukia = makeRequest(url='http://data.sparkfun.com/input/dZaoR0p6pasmppMl5KRd',method='POST',body="temp="+str(temperature),headers={
        'Phant-Private-Key': 'eEwYG2aKawfW55ow8Gp7',
        'Content-Type': 'application/x-www-form-urlencoded',
        })
    print response.status
    print response.getheader('Location')
    print edukia
    time.sleep(1)


