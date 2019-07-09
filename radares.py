import mysql.connector, requests
from time import sleep
from notify_run import Notify
from bs4 import BeautifulSoup


def main():
    noty = notifier()

    sleep(30)

    while True:
        getRadares(["A1"])
        # sendNotification(noty, getRadares(getRadaresToSearch()))
        print "done"
        sleep(60)

def db(operation):

    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="root",
      database="radares"
    )

    cursor = mydb.cursor()

    result = None
    
    if "SELECT" in operation:
        cursor.execute(operation)
        result = cursor.fetchall()
    elif "INSERT" in operation:
        cursor.execute(operation)
        mydb.commit()


    return result


def notifier():

    noty = Notify()

    if len(db("SELECT * FROM sessions")) == 0:
        register = noty.register()
        print register
        db("INSERT INTO sessions (token) VALUES ('" + register.endpoint.split("/")[-1] + "')")

    noty.send("Server up!!")
    print "Server up!!"

    return noty


def sendNotification(noty, message):
    noty.send(message)
    print "Sended notification: " + message


def getRadaresToSearch():
    return map(lambda x: str(x[0]), db("SELECT * FROM search"))

def getRadares(radares):

    toAlert = "RADARES ENCONTRADOS!\n"


    for i in range(0,5):
        req = requests.get("https://temporeal.radaresdeportugal.pt/extras/paginator.php?page=" + str(i))
        page = BeautifulSoup(req.content, 'html.parser')

        for elem in page.find_all('p', attrs={'class':'lead'}):
            warning = elem.text

            pubid = warning.parent.parent["class"][2]

            for word in warning.split(" "):
                if word in radares:
                    message = warning.replace("[marcado no Mapa da app RADARES de Portugal]","").replace("[app RADARES de Portugal]", "").strip("\n")
                    toAlert += message + "\n"
                    print "Radar found: " + message

    return toAlert



main()