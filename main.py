import json
from flask import Flask, render_template, request, redirect, Response, stream_with_context



app = Flask(__name__)

class temp:
    data= {}



def LCG(prevNumber):
    A=9
    C=5
    M=2**32
    return (A*prevNumber+C)%M

def testLCG(numb=10):
    tmp=1
    for i in range(numb):
        tmp=LCG(tmp)
        print("hex:"+Numb2HexStr(tmp))
        print("numb:"+str(Hex2Numb(Numb2HexStr(tmp))))

def Numb2HexStr(numb):
    hexNumb = hex(numb)
    #print(len(hexNumb))
    return(hexNumb + ("0"*(10-len(hexNumb))))

def Hex2Numb(Hex):
    print((int(Hex, 0)))
    return (int(Hex, 0))


def nextTicketId(data):
    print(data)
    print(len(data))
    if len(data) == 0:
        return Numb2HexStr(1)
    last=list(data)[-1]
    print(last)
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
    data = temp.data
    print(data)
    #data = json.dumps(data)
    #print(data)
    return render_template('index.html', data=data)

@app.route('/ticket/<path:path>')
def ticket(path):
    data = temp.data[path]
    print(data)
    #data = json.dumps(data)
    #print(data)
    return render_template('ticket.html', data=data)


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
    app.run(host='0.0.0.0', port=5501, debug=True)