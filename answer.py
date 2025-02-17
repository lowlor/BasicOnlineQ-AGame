from tkinter import*
from socket import *
import threading 
root = Tk()
root.geometry("400x200")
root.title("Answer")

score = 0
scoreToWin =0
answerFlag = 0 

def server():
    global scoreToWin,clientSocket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    print(serverName, serverPort)
    clientSocket.connect((serverName,serverPort))
    scoreToWin = clientSocket.recv(1024).decode()
    destroyFrame()
    answerPage()

def serverButtonClick():
    global serverName,serverPort
    try: 
        serverPort = int(portEntry.get())
        serverName =str(ipEntry.get())
        server()
    except Exception as e :
        findPageStatusLabel.config(text="Not found questioner. Please try again.")
    
def destroyFrame():
    for frame in mainFrame.winfo_children():
        frame.destroy()
def findPage():
    global ipEntry,portEntry,findPageStatusLabel
    findPageFrame = Frame(mainFrame)
    findPageFrame.pack()

    ipLabel= Label(findPageFrame,text="Enter IP")
    ipEntry = Entry(findPageFrame)

    portLabel= Label(findPageFrame,text="Enter Port")
    portEntry = Entry(findPageFrame)

    findPageStatusLabel = Label(findPageFrame)

    serverButton = Button(findPageFrame,text="Enter",command=serverButtonClick)

    ipLabel.pack()
    ipEntry.pack()
    portLabel.pack()
    portEntry.pack()
    findPageStatusLabel.pack()
    serverButton.pack()
def receiveQuestion():
    global answerCorrect, question, answerFlag
    statusLabel.config(text="Status : Waiting to questioner to send question.")
    questionLabel.config(text="Question : Waitting for question")
    sentence = clientSocket.recv(1024).decode()
    answerCorrect, question, timeToAnswer = sentence.split('|')
    print("[Received from Server] Received question : "+ question)
    print("[Received from Server] Correct answer : "+ answerCorrect)
    print("[Received from Server] Time to Answer : "+ timeToAnswer)
    questionLabel.config(text="Question : "+question)
    statusLabel.config(text="Status : Answer Now")
    answerButton.config(state=NORMAL)
    answerFlag=0
    countdown(int(timeToAnswer))
def timeRunOut():
    statusLabel.config(text="Status : Time out. Got no score.")
    clientSocket.send("Timed out".encode())
    print("[Sent to Sever] Timed out")
    sentence = clientSocket.recv(1024).decode()
    if(sentence == 'Questioner win'):
        print("[Received from Server] Questioner win")
        destroyFrame()
        losePage()
    else:    
        print("[Received from Server] Questioner not win yet")
        threading.Thread(target=receiveQuestion).start()
def winPage():
    clientSocket.close()
    winPageFrame = Frame(mainFrame)
    winPageFrame.pack()

    winPageLabel = Label(text="You Win")
    winPageLabel.pack()
def losePage():
    clientSocket.close()
    losePageFrame = Frame(mainFrame)
    losePageFrame.pack()

    losePageLabel = Label(text="You Lose")
    losePageLabel.pack()
def answerClick():
    if answerEntry.get() == answerCorrect:
        global score, answerFlag
        score = score + 1
        answerFlag = 1
        answerButton.config(state=DISABLED)
        scoreWithScoreLabel.config(text="Score :" + str(score))
        statusLabel.config(text="Status : Correct Answer. Got +1 score")
        if score >= int(scoreToWin):
            clientSocket.send("Answerer Win".encode())
            print("[Sent to Server] Answerer win")
            destroyFrame()
            winPage()
        else:
            clientSocket.send("Correct".encode())
            print("[Sent to Server] Correct")
            threading.Thread(target=receiveQuestion).start()
    else:
        answerFlag = 1
        answerButton.config(state=DISABLED)
        statusLabel.config(text="Status : Wrong answer. Got no score")
        clientSocket.send("Wrong".encode())
        print("[Sent to Server] Wrong")
        sentence = clientSocket.recv(1024).decode()
        if(sentence == 'Questioner win'):
            print("[Received from Server] Questioner win")
            destroyFrame()
            losePage()
        else:
            print("[Received from Server] Questioner not win yet")
            threading.Thread(target=receiveQuestion).start()
       

def countdown(time, msg='time remain'):
    time -=1
    timerLabel.config(text=f'{msg} ({time}sec)')

    if time != 0 and answerFlag == 0:
        root.after(1000, countdown, time)
    elif time != 0 and answerFlag == 1:
        timerLabel.config(text='Answered stop')
    else:
        answerButton['state'] = 'disabled'
        timeRunOut()

def answerPage():
    global answerButton, timerLabel,statusLabel,answerEntry,scoreWithScoreLabel, questionLabel,scoreToWinLabel
    answerPageFrame = Frame(mainFrame)
    answerPageFrame.pack()

    scoreToWinLabel = Label(answerPageFrame,text="Score to win : "+scoreToWin)
    statusLabel = Label(answerPageFrame,text="Status :")
    answerLabel = Label(answerPageFrame,text="Enter Answer Here")
    questionLabel = Label(answerPageFrame,text="Question : Waiting for question")
    scoreWithScoreLabel = Label(answerPageFrame,text="Score : "+str(score))
    timerLabel = Label(answerPageFrame)

    answerButton = Button(answerPageFrame, text='Answer', command=answerClick,state=DISABLED)
    
    answerEntry = Entry(answerPageFrame,borderwidth=5)

    statusLabel.pack()
    scoreToWinLabel.pack()
    questionLabel.pack()
    scoreWithScoreLabel.pack()
    timerLabel.pack()
    answerLabel.pack()
    answerEntry.pack()
    answerButton.pack()
    threading.Thread(target=receiveQuestion,daemon=True).start()

mainFrame = Frame(root)
mainFrame.pack()

findPage()

root.mainloop()