### NECESSARY:

The Microservice is implemented by using sockets as a communication pipeline.
In order for the server and client to communicate with each other, there are some necessary imports.
Please include the following at the top of the client file.

```commandline
import socket
import base64
from PIL import Image
```

### A) Clear instructions for how to programmatically REQUEST data from microservice. Include example call.

**Important**: You will need to start the server before starting the client. 

Once the server is running, it will wait for the client to send data to it and 
once it receives what it was waiting for it will process it and send back the 
encoded image of the chart. So basically, to request data, you first have to 
send data - the data you send being a string of numbers separated by spaces.

Here is how to request data from the microservice:

Specify the HOST and the PORT.

```python
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
```
After that, you must make a socket instance and pass the necessary parameters, 
then connect to the server.
```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
```

To send your data to the server, you will convert the string to bytes (specifying the
encoding as utf-8) and use the sendall method (where s is that socket instance we created).
```python
def send_to_server(scores_string):
    s.sendall(bytes(scores_string, 'utf-8'))
```

Here is an example of how you might pass in the scores_string.
```python
send_to_server(f"{addition_correct} {subtraction_correct} {multiplication_correct} {incorrect}")
```
where 'incorrect' is the number of questions they answered incorrectly.

####Full example call:
```python
import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def send_to_server(scores_string):
    s.sendall(bytes(scores_string, 'utf-8'))
    ...

example_scores = "2 6 8 3"
send_to_server(example_scores)
```

The server will be expecting the string to be set up with the numbers in exactly that order.

### B) Clear instructions for how to programmatically RECEIVE data from microservice.

To receive data from the server, you can use a while loop and use the ``s.recv()`` method.
The data you will receive will look like a bunch of letters and numbers if you attempt to
print it. That's because it is an image encoded into base64.
```python
    data = b''
    print("Connected to Server, getting data...")
    while True:
        try:
            s.settimeout(0.5)
            data += s.recv(1024)
        except socket.error:
            break
    ...
```
Once the data has been received, you can turn it back into a human-readable image.
To do this, write it to a png file.
Then save it to a variable using PIL's ``Image.open()`` method.
To display the image to the user, you can use ``.show()``
``` python
    ...
    imgdata = base64.b64decode(data)
    filename = 'my_image.png'
    with open(filename, 'wb') as f:
        f.write(imgdata)
    my_image = Image.open(filename)
    my_image.show()
```

#### Full Example:
```python
import socket
import base64
from PIL import Image


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def send_to_server(scores_string):
    s.sendall(bytes(scores_string, 'utf-8'))
    data = b''
    print("Connected to Server, getting data...")
    while True:
        try:
            s.settimeout(0.5)
            data += s.recv(1024)
        except socket.error:
            break
    imgdata = base64.b64decode(data)
    filename = 'my_image.png'
    with open(filename, 'wb') as f:
        f.write(imgdata)
    my_image = Image.open(filename)
    my_image.show()

######## end of function ###########

...
...
...
# Put this at the end of PlayGame(), just before optionsScreen()
send_to_server(f"{addition_correct} {subtraction_correct} {multiplication_correct} {incorrect}")

```

### C) UML sequence diagram showing how requesting and receiving data works.

![image](https://github.com/AriZeto/microservice/assets/98569819/d5926b0d-ce4e-471c-8090-a4b7b0453c42)


