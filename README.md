# Ticket project

This is a flask webserver with a built in data storage system made to handle suport/contact tickets

### Pictures

**Main page**
![Main page](/images/index.png)
<sup><sub>this is a exaple with two tickets using random contents from postman and one made using the create ticket field</sup></sub>

**Ticket page**
![Ticket page](/images/ticket.png)
<sup><sub>this is a exaple with four tickets using random contents from postman and two made using the message field</sup></sub>

# Usage

### Windows (curently untested)
make sure python is installed (Python 3.14.2 used when making this)

in the parent directory run the following 
```batch
python -m venv .venv
".venv/scripts/activate.bat"
pip install flask
python main.py
```

### Linux
make sure python is installed (Python 3.14.2 used when making this)

in the parent directory run the following 
```shell
python -m venv .venv
source .venv/bin/activate
pip install flask
python main.py
```

if you're using ufw then run the following
```shell
ufw allow 5501/tcp
```

## Website
the website should be on **http://127.0.0.1:5501/**

## file structure

```r
.
├── images
│   ├── index.png                   #Picture of the main page.
│   └── ticket.png                  #Picture of the page for a spesific ticket.
│
├── templates
│   ├── index.html                  #This is the main page.
│   └── ticket.html                 #This is the page for a spesific ticket.
│
├── static
│   ├── fonts/Terminus
│   │   ├── README.md               #Readme for the nerd font. 
│   │   ├── LICENSE.txt             #License for the nerd font. (SIL Open Font License, Version 1.1.)
│   │   └── TerminessNerdFont*.ttf  #True type font file.
│   │
│   └── auth.js                     #File for super basic hased user auth using simlpe sha256 hashing.
│
├── README.md                       #This file :3
├── LICENSE                         #Simple GLWTS license
├── main.py                         #This is the main flask server file
├── data.json                       #Auto generated ticket storage file
└── users.json                      #Auto generated user data storage file
```

## API referance

**GET `/`**\
serves the main page (renderd template)\
Params:
```r
user = str # the user's username
hash = str # the user's hash (SHA-256)
```
body: 
```python
None
```
Returns: templates/index.html 

<br><br>

**GET `/logedOut`**\
forces the user to be loged out\
Params:
```python
None
```
body: 
```python
None
```
Returns: html page that clears the saved username and hash before reloading the page

<br><br>

**GET `/ticket/\<ticket-id>/`**\
serves the ticket page (renderd template)\
Params:
```r
user = str # the user's username
hash = str # the user's hash (SHA-256)
```
body: 
```python
None
```
Returns: templates/ticket.html 

<br><br>

**POST `/ticket/\<ticket-id>/`**\
This changes the ticket status\
Params:
```r
user = str # the user's username
hash = str # the user's hash (SHA-256)
```
body: 
```python
{
  "status":  str # can be "open", "wip" or "closed"
}
```
Returns: Nothing

<br><br>

**POST `/ticket/\<ticket-id>/newMessage/`**\
This adds a comment to the ticket\
Params:
```r
user = str # the user's username
hash = str # the user's hash (SHA-256)
```
body: 
```python
{
  "message":  {
    "user": str,    # the displayed sender name 
    "message": str  # the displayed message
    }
}
```
Returns: Nothing

<br><br>

**POST `/new/ticket/`**\
This adds a comment to the ticket\
Params:
```r
user = str # the user's username
hash = str # the user's hash (SHA-256)
```
body: 
```python
{
    "person": str,  # the displayed sender name
    "email": str,   # the sender's contact email
    "title": str,   # the title of the ticket
    "body": str,    # the text body of the ticket
    "status": str,  # the status opon creation
    "users": list   # list of users added to veiw the ticket
}
```
Returns: Nothing
