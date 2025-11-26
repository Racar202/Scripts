import requests
import smtplib
import email
from email.message import EmailMessage

## == MAIL VARIABLES ==##

EMAIL_ACCOUNT = 'john.doe@test.com' 
EMAIL_PASSWORD = 'xxxxx'

smtp_server = 'smtp.server.com' # SMTP server used for sending the email
smtp_port = '465'

subject = 'ELASTIC STACK DISK USAGE' 
recipient = '' # Who will recieve the mail

## ==== ##

response = requests.get('https://IP:9200/_cat/allocation?v', verify=False, auth=('elastic', 'xxxx'))  # Request to the elastic port 

if response.status_code == 200: # If the request is succesfull, removes the word gb just to be able to divide the values
    values = response.text.replace("gb", "").split()
    free_space = ((float(values[11]) / float(values[13])) * 100) # Gets the remaining free space % from dividing disk usage from disk total
    if free_space > 70: # If more than 70% is being used sends an alert along with instructions to free space.

        body = 'Le avisamos que el porcentaje de disco usado de su Elastic Stack, con IP <IP>, es de un: ' + str(round(free_space, 2)) + '%, le quedan ' + str(values[12]) + 'GB libres.\n' \
"""
Si no se soluciona pronto, el sistema podría dejar de funcionar, porfavor siga las siguientes recomendaciones:

- Comprobar que los ciclos de vida de los indices estén funcionando correctamente: Estos deben borrarse cada 30 días.
- Mirar si hay índices innecesarios que se puedan borrar (Que ya tengan varios meses o que no sean importantes).
            
Algunos comandos útiles: 

Mostrar todos los índes y ordenarlos por tamaño: 
    curl -X GET "https://IP:9200/_cat/indices?s=store.size:asc" --insecure -u usuario:contraseña

Borrar índices usando regex (En este caso que borre todos los indices de filebeat del mes de septiembre): 
    curl -X DELETE "https://IP:9200/filebeat-7.17.13-2025.09*" --insecure -u usuario:contraseña

Para más información consultar la documentación oficial.

https://www.elastic.co/docs/solutions/observability/infra-and-hosts/universal-profiling-index-life-cycle-management
https://mkonda007.medium.com/elasticsearch-in-action-uindex-life-cycle-ilm-management-3070bf498b6a

"""

else:
    body = 'Ha habido un error a la hora de comprobar el estado del disco de su Elastic Stack con IP <IP>.\nPorfavor compruebe manualmente su estado.' 


## SEND EMAIl ##

msg = EmailMessage()
msg['From'] = EMAIL_ACCOUNT
msg['To'] = recipient
msg['Subject'] = subject
msg.set_content(body)

with smtplib.SMTP_SSL(smtp_server, 465) as server:
    server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    server.send_message(msg)





