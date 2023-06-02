''' Integrantes do grupo: 
    ALEKSANDRO BRUNO GOUVEA 
    ALISON GUILHERME BABINSKI 
    LAIS MULLER ALISKI 
    THIAGO JOSINALDO DOS SANTOS SOUZA 
'''

import datetime
import pyrebase
import os.path
import os
import stat
import smtplib
import random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

firebaseConfig = {
    "apiKey": "AIzaSyDBpVEphafYSpeenpqKrP9KVVYKbFG11Kk",
    "authDomain": "puc---seguranca-da-informacao.firebaseapp.com",
    "projectId": "puc---seguranca-da-informacao",
    "databaseURL": "https://" + "puc---seguranca-da-informacao" + ".firebaseio.com",
    "storageBucket": "puc---seguranca-da-informacao.appspot.com",
    "messagingSenderId": "210447136441",
    "appId": "1:210447136441:web:d395b34a2d129235fe8d68",
    "measurementId": "G-890FK1MHR7"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

server = "smtp.gmail.com"
port = 587
username = "alebgou@gmail.com"
passwordSMTP = "xrncfwwpjqfcrqdx"

ok = True

while ok:
    print("1 - Cadastrar Usuário")
    print("2 - Verificar Email")
    print("3 - Autenticar Usuário")

    opcao = input("Selecione uma das opções:")

    if opcao == "1":
        user = input("Digite seu e-mail: ")
        password = input("Digite sua senha, com pelo menos 6 caracteres: ")
        status = auth.create_user_with_email_and_password(user, password)
        print("Email cadastrado: ",user)

    elif opcao == "2":
        user = input("Digite seu e-mail: ")
        password = input("Digite sua senha, com pelo menos 6 caracteres: ")
        # status = auth.create_user_with_email_and_password(user,password)
        status = auth.sign_in_with_email_and_password(user, password)
        idToken = status["idToken"]
        auth.send_email_verification(idToken)
        print("Email de verificação enviado: ", user)

    elif opcao == "3":
        user = input("Digite seu e-mail: ")
        password = input("Digite sua senha, com pelo menos 6 caracteres: ")
        status = auth.sign_in_with_email_and_password(user, password)
        now = datetime.datetime.now()
        dataehora = now.strftime("%d/%m/%Y, %H:%M:%S")
        idToken = status["idToken"]
        info = auth.get_account_info(idToken)
        users = info["users"]
        verifyEmail = users[0]["emailVerified"]

        if verifyEmail:
            print("Segundo Fator de Autenticao")
            codigo = random.randint(1000,9999)
            mail_body = "Código de validação: %d "%codigo

            mensagem = MIMEMultipart()
            mensagem['From'] = username
            mensagem['To'] = user
            mensagem['Subject'] = "Código E-mail"
            mensagem.attach(MIMEText(mail_body, 'plain'))

            connection = smtplib.SMTP(server, port)
            connection.starttls()
            connection.login(username, passwordSMTP)
            connection.send_message(mensagem)
            connection.quit()

            codigoEmail = int(input("Entre com o código que foi enviado por e-mail: "))

            if codigo == codigoEmail:
                print("Usuário Autenticado!!!")
                ok = False

            else:
                print("Código Inválido!!")

        else:
            print("Email não verificado!")



print("Último acesso do usuário ", user, " em: ", dataehora)

file_exists = os.path.exists('acesso.txt')
print()
# Verifica se existe o arquivo emails.txt
if file_exists is False:
    # Se sim, cria ele e adiciona o email adicionado e a data/hora
    with open('acesso.txt', 'w') as arquivo:
        # Modifica a permissão do arquivo para leitura, escrita e execução
        os.chmod("acesso.txt", stat.S_IRWXU)
        arquivo.write(str(user) + ' - ' + dataehora + '\n')
        #fecha aquivo
        arquivo.close()
        # Modifica o arquivo apenas para leitura
        os.chmod("acesso.txt", stat.S_IRUSR)
else:
    # Se nao, apenas adiciona informações nele e depois fecha
    with open('acesso.txt', 'a') as arquivo:
        # Modifica a permissão do arquivo para leitura, escrita e execução
        os.chmod("acesso.txt", stat.S_IRWXU)
        # print("Arquivo já existe, logo adicionar informações nele")
        arquivo.write(str(user) + ' - ' + dataehora + '\n')
        # fecha aquivo
        arquivo.close()
        # Modifica o arquivo apenas para leitura
        os.chmod("acesso.txt", stat.S_IRUSR)