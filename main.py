import json
from flask import Flask, render_template, request, redirect, Response, stream_with_context, request_finished
#from OpenSSL import SSL
#context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
#context.use_privatekey_file('server.key')
#context.use_certificate_file('server.crt')   


app = Flask(__name__)

class temp:
    data= {}
    users= {}



def LCG(prevNumber):
    A=9
    C=5
    M=2**32
    return (A*prevNumber+C)%M

def testLCG(numb=10):
    tmp=1
    for i in range(numb):
        tmp=LCG(tmp)
        #print("hex:"+Numb2HexStr(tmp))
        #print("numb:"+str(Hex2Numb(Numb2HexStr(tmp))))

def Numb2HexStr(numb):
    hexNumb = hex(numb)
    #print(len(hexNumb))
    return(hexNumb + ("0"*(10-len(hexNumb))))

def Hex2Numb(Hex):
    #print((int(Hex, 0)))
    return (int(Hex, 0))


def nextTicketId(data):
    #print(data)
    #print(len(data))
    if len(data) == 0:
        return Numb2HexStr(1)
    last=list(data)[-1]
    #print(last)
    lastNumb = Hex2Numb(last)
    return Numb2HexStr(LCG(lastNumb))


def writeData(data, fileName):
    with open(fileName, 'w',  encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def readData(fileName, fallbackData={}):
    try:
        with open(fileName, 'r',  encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"File: {fileName} not found creating empty")
        writeData(fallbackData, fileName)
    except Exception as err:
        print(f'read failed reson: {str(err.with_traceback)}')
        return None




def newTicket(ticket):
    data = temp.data
    id = nextTicketId(data)
    data[id] = ticket
    temp.data = data
    writeData(data, "data.json")





@app.route('/')
def index():
    user=request.args.get('user')
    hash=request.args.get('hash')
    #print(request.args)
    userDict = temp.users
    if user != None:
        temp.data = readData("data.json")
        temp.users = readData("users.json")
        try:
            if userDict[user]["hash"] == hash:
                print("auth ok")
            else:
                print("auth failed")
                return redirect('/logedOut')
        except:
            userDict[user] = {"hash": hash, "admin": False}
            writeData(userDict, "users.json")
            temp.users = readData("users.json")
            print("user does not exist")
            return redirect('/')
        tmpdata = temp.data
        #print(tmpdata)
        #data = json.dumps(data)
        #print(data)
        data = {}
        if userDict[user]["admin"]:
            data = tmpdata
        else:
            for i in tmpdata:
                j = tmpdata[i]
                for k in j["users"]:
                    if user == k:
                        data[i] = j
    else:
        data={}
    return render_template('index.html', data=data)


@app.route('/logedOut')
def logedOut():
    site = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    </head>
    <body>
    <script>
        localStorage.clear()
        window.location.href = (window.location.href.split("?")[0].split("logedOut")[0])
    </script>
    </body>
    """
    return site

@app.route('/ticket/<path:path>', methods=['GET'])
def ticket(path):
    user=request.args.get('user')
    hash=request.args.get('hash')
    #print(request.args)
    userDict = temp.users
    isAdmin=False
    if user != None:
        temp.data = readData("data.json")
        temp.users = readData("users.json")
        try:
            if userDict[user]["hash"] == hash:
                print("auth ok")
            else:
                print("auth failed")
                return redirect('/logedOut')
        except:
            userDict[user] = {"hash": hash, "admin": False}
            writeData(userDict, "users.json")
            temp.users = readData("users.json")
            print("user does not exist")
            return redirect('/')
        tmpdata = temp.data[path]
        #print(tmpdata)
        #data = json.dumps(data)
        #print(data)
        data = {}
        if userDict[user]["admin"]:
            data = tmpdata
            isAdmin = True
        else:
            if user in tmpdata["users"]:
                data = tmpdata
    else:
        data={}
    #data = temp.data[path]
    #print(data)
    #data = json.dumps(data)
    print(data)
    return render_template('ticket.html', data=data, isAdmin=isAdmin)

@app.route('/ticket/<path:path>', methods=['POST'])
def changeTicket(path):
    user=request.args.get('user')
    hash=request.args.get('hash')
    #print(request.json)
    status= request.json["status"]
    #print(request.args)
    userDict = temp.users
    isAdmin=False
    if user != None:
        temp.data = readData("data.json")
        temp.users = readData("users.json")
        try:
            if userDict[user]["hash"] == hash:
                print("auth ok")
            else:
                print("auth failed")
        except:
            userDict[user] = {"hash": hash, "admin": False}
            writeData(userDict, "users.json")
            temp.users = readData("users.json")
            print("user does not exist")
        tmpdata = temp.data[path]
        #print(tmpdata)
        #data = json.dumps(data)
        #print(data)
        data = {}
        if userDict[user]["admin"]:
            data = tmpdata
            #print(f"data is{data}")
            #print(f"data is type: {type(data)}")
            data["status"] = status
            #print(f"data is now{data}")
            temp.data[path] = data
            writeData(temp.data, "data.json")
            isAdmin = True
        else:
            if user in tmpdata["users"]:
                data = tmpdata
    else:
        data={}
    return redirect('/')


@app.route('/ticket/<path:path>/newMessage', methods=['POST'])
def newMessage(path):
    user=request.args.get('user')
    hash=request.args.get('hash')
    #print(request.json)
    body = request.json
    message= body["message"]
    #print(request.args)
    userDict = temp.users
    isAdmin=False
    if user != None:
        data = {}
        try:
            if userDict[user]["hash"] == hash:
                print("auth ok")
            else:
                print("auth failed")
        except:
            print("user does not exist")
            return request_finished
        tmpdata = temp.data[path]
        if userDict[user]["admin"]:
            data = tmpdata
            #print(f"data is{data}")
            #print(f"data is type: {type(data)}")
            data["comments"].append(message)
            #print(f"data is now{data}")
            temp.data[path] = data
            writeData(temp.data, "data.json")
            isAdmin = True
        else:
            if user in tmpdata["users"]:
                data = tmpdata
                data["comments"].append(message)
    else:
        data={}
    return redirect('/')


@app.route('/new/ticket', methods=['POST'])
def GenerateNewTicket(callback=None):
    data = request.json
    print(f"data is type: {type(data)}")
    newTicket(data)
    return redirect('/')










if __name__ == '__main__':
    #testLCG()
    #temp.data = readData("data.json")
    #newTicket("test")
    temp.data = readData("data.json")
    temp.users = readData("users.json")
    app.run(host='0.0.0.0', port=5501, debug=True, ssl_context=('.cert/server.crt', '.cert/server.key'))