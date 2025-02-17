from tkinter import*
from socket import *
import threading
root = Tk()
root.geometry("400x300")
root.title('Question')

score = 0 
questionButtonClicked = 0
answerButtonClicked = 0
timeButtonClicked =0
scoreToWin =0

def serverOpen():
    global connectionSocket, serverSocket
    serverPort = 5050
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)
    print("server ready to connect")
    print("Waiting for Client to connect")
    waitingPage()
def winPage():
    connectionSocket.close()
    winPageFrame = Frame(mainFrame)
    winPageFrame.pack()

    winPageLabel = Label(text="You Win")
    winPageLabel.pack()
def acceptConnect():
    global connectionSocket,waitingLabel    
    connectionSocket, addr = serverSocket.accept()
    waitingLabel.config(text="answerer is in. Ready")
    connectionSocket.send(str(scoreToWin).encode())
    destroyFrame()
    questionPage()
def winButtonClick():
    global scoreToWin
    try:
        scoreToWin = int(winEntry.get())
        destroyFrame()
        serverOpen()
    except Exception as e:
        winStatusLabel.config(text="Type in Number")

def winNumberPage():
    global winStatusLabel,winEntry
    winNumberPageFrame = Frame(mainFrame)
    winNumberPageFrame.pack()

    winLabel = Label(winNumberPageFrame,text="How many score to win")
    winEntry = Entry(winNumberPageFrame)
    winButton = Button(winNumberPageFrame,text="Enter",command=winButtonClick)
    winStatusLabel = Label(winNumberPageFrame)

    winLabel.pack()
    winEntry.pack()
    winButton.pack()
    winStatusLabel.pack()

def waitingPage():
    global serverSocket,winStatusLabel,connectionSocket,waitingLabel,waitingPageFrame,winEntry
    waitingPageFrame = Frame(mainFrame)
    waitingPageFrame.pack()

    ipAddr = gethostbyname(gethostname())
    informationLabel = Label(waitingPageFrame,text="Your Ip is "+ ipAddr)
    portLabel = Label(waitingPageFrame,text="Your port number to let answerer connect is 5050")
    waitingLabel = Label(waitingPageFrame,text="Waiting to Answer to connect")
    
    informationLabel.pack()
    portLabel.pack()
    waitingLabel.pack()
    


    root.update()
    threading.Thread(target=acceptConnect,daemon=True).start()
    

  
def destroyFrame():
    for frame in mainFrame.winfo_children():
        frame.destroy()
def resetFlag():
    global questionButtonClicked, answerButtonClicked
    questionButtonClicked=0
    answerButtonClicked=0
def setButtonFreeze():
    enterButton.config(state=DISABLED)
def setButtonActive():
    enterButton.config(state=NORMAL)

def buttonClick():
    try:
        if answerEntry.get() == '' or questionEntry.get() =='' or timeEntry.get()=='':
            statusLabel.config(text="Status : Fill all Entry")
        elif int(timeEntry.get()) < 20 :
            statusLabel.config(text="Status : Time need to more than or equal to 20")
        else:
            resetFlag()
            sendToAnswerer()
            statusLabel.config(text="Status : sent to answerer. Waitting to answer")
            setButtonFreeze()
            threading.Thread(target=receiveClientStatus).start()
    except Exception as e:
        statusLabel.config(text="Status : Please enter properly")
def sendToAnswerer():
    sentenceToSend = answerEntry.get()+'|'+questionEntry.get()+'|'+timeEntry.get()
    print("[Sent to Client] " + sentenceToSend)
    connectionSocket.send(sentenceToSend.encode())
def receiveClientStatus():
    global score
    sentence = connectionSocket.recv(1024).decode()
    if sentence == 'Wrong':
        score += 1
        print("[Received from Client] Wrong")
        if score >= scoreToWin:
            connectionSocket.send("Questioner win".encode())
            print("[Sent to Client] Questioner win")
            destroyFrame()
            winPage()
        else:
            statusLabel.config(text="Status : Answerer is incorrect. you got point.")
            scoreWithScoreLabel.config(text="Score : "+str(score))
            connectionSocket.send("Questioner not win yet".encode())
            print("[Sent to Client] Questioner not win yet")
            setButtonActive()
    elif sentence == 'Timed out':
        score += 1
        print("[Received from Client] Timed out")
        if score >= scoreToWin:
            connectionSocket.send("Questioner win".encode())
            print("[Sent to Client] Questioner win")
            destroyFrame()
            winPage()
        else:
            statusLabel.config(text="Status : Answerer ran out of time. you got point.")
            scoreWithScoreLabel.config(text="Score : "+str(score))
            connectionSocket.send("Questioner not win yet".encode())
            print("[Sent to Client] Questioner not win yet")
            setButtonActive()
    elif sentence == "Answerer Win":
        print("[Received from Client] Answerer Win")
        destroyFrame()
        losePage()
    else:
        statusLabel.config(text="Status : Answerer is correct. you got no point.")
        scoreWithScoreLabel.config(text="Score : "+str(score))
        print("[Received from Client] Correct")
        setButtonActive()
        
def losePage():
    connectionSocket.close()
    losePageFrame = Frame(mainFrame)
    losePageFrame.pack()

    losePageLabel = Label(text="You Lose")
    losePageLabel.pack()

def questionPage():
    global statusLabel,scoreWithScoreLabel,answerEntry,questionEntry,enterButton,timeEntry
    
    questionPageFrame = Frame(mainFrame)
    questionPageFrame.pack()
    statusLabel = Label(questionPageFrame,text="Status : Waiting to send question")
    answerLabel = Label(questionPageFrame,text="Enter Answer Here")
    questionLabel = Label(questionPageFrame,text="Enter Question Here")
    scoreWithScoreLabel = Label(questionPageFrame,text="Score : "+str(score))
    timeLabel = Label(questionPageFrame,text="Enter Time Here")
    
    enterButton = Button(questionPageFrame, text='Enter', command=buttonClick)
  
    answerEntry = Entry(questionPageFrame,borderwidth=5)
    questionEntry = Entry(questionPageFrame,borderwidth=5)
    timeEntry = Entry(questionPageFrame,borderwidth=5)
    
    
    statusLabel.pack()
    scoreWithScoreLabel.pack()
    questionLabel.pack()
    questionEntry.pack()
    answerLabel.pack()
    answerEntry.pack()
    timeLabel.pack()
    timeEntry.pack()
    enterButton.pack()

mainFrame = Frame(root)
mainFrame.pack()
winNumberPage()

root.mainloop()