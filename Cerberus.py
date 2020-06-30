import xml.etree.ElementTree as ET
import json
import os
from colorama import init, Style,  Back,  Fore
init()
tree = ET.parse('cerberus_teste.xml')
root = tree.getroot()


print("|",'\x1b[6;47;42m' + "--------------------------------CheckList Cerberus--------------------------------" + '\x1b[0m',"|")

#Loop to find the XML first row(XML)
for x in root.findall("./*"):
    #Get the server names and remove "_" from the beggining of it
    if x is not None:
        servidor = (x.tag)
        servidor = ''.join(c for c in servidor if c not in '(){}<>_,')
        
    #Access the comandosdb row
    comandosdb = x.find('_comandosdb')
    if comandosdb is not None:
        #Finds the acumulated command value
        comandos_armazenados = comandosdb.find('_comandosarmazenados').attrib
        if comandos_armazenados == {'_comandosarmazenados': '-'}:
            print("Status: ", Back.RED+ "Desconectado? - VERIFICAR"+Style.RESET_ALL,"|")
        else:
            print("Status: ", Back.GREEN+ "Conectado"+Style.RESET_ALL,"|")
            comandos_lista =  json.dumps(comandos_armazenados).split(":")
            comandos_numeros = int(''.join(c for c in comandos_lista[1] if c not in '("){.}<>_,'))
            if comandos_numeros != 0:
                print("COMANDOS ARMAZENADOS:", Back.RED, comandos_numeros, Style.RESET_ALL,"|")

#Access the process row
    processo = x.find('_processo')
    if processo is not None:
        processo_child = processo.find('_workingset').attrib
        processo_lista = json.dumps(processo_child).replace('"}','').replace('"', '').split(":")
        workinset_sem_pontos= ''.join(c for c in processo_lista[1] if c not in '("){.}<>_,')
        workinget_numeros  = int(workinset_sem_pontos)
        if workinget_numeros >= 1580142592:
            print ("Workingset: ", Back.RED, workinget_numeros, Style.RESET_ALL,"|",  "\n")

#Access the StatusBasic row     
    statusbasic = x.find('_statusbasic')
    if statusbasic is not None:
        #Search for errors and errorhour
        warning_child = statusbasic.find('_warningmsg').attrib
        warninghora_child = statusbasic.find('_warninghora').attrib
        if warninghora_child != {'_warninghora': ''}:
            warninghora_lista = json.dumps(warninghora_child).replace('{"_warninghora":', '').replace('}', '').split("':")
            warning_lista = json.dumps(warning_child).replace('{"_warningmsg": ', '').replace('}', '')
            print ("Ultimo warning ocorrido:\n", Back.WHITE, Fore.BLACK+warning_lista+Style.RESET_ALL,"|"),
            print ("Hora do warning:", warninghora_lista[0], "\n")
            
        #Search for dberros and hour
        statusbasic_child = statusbasic.find('_erromsg').attrib
        statushora_child = statusbasic.find('_errohora').attrib
        if statushora_child != {'_errohora': ''}:            
            statusbasic_lista = json.dumps(statusbasic_child).replace('{"_erromsg": ', '').replace('}', '')
            print ("Ultimo erro ocorrido:\n", Back.WHITE, Fore.BLACK+ statusbasic_lista+Style.RESET_ALL,"|")
        if statusbasic_child != {'_erromsg': ''}:
            statushora_lista = json.dumps(statushora_child).replace('{"_errohora":', '').replace('}', '').split("':")
            print ("Hora do erro:", statushora_lista[0])

            
        print("_____________________________________________________________________________________________",  "\n")
        
        
os.system("pause")
    
