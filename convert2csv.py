import time
import sys

def writeOutput(result, path="submission"):
    with open(path+".csv", 'w') as f:
        for i in result:
            f.write(i+"\n")
    f.close()

def play(symbol,strLocation,board,output):
    if strLocation == "PASS":
        return
    strGap = "*, ,*,"
    location = strLocation.split(",")
    i = int(location[0])
    j = int(location[1])
    replaceBoard = board[i].split(",")
    replaceBoard[j] = symbol
    board[i] = ','.join(replaceBoard)
    output[0] += strGap + board[0]
    output[1] += strGap + board[1]
    output[2] += strGap + board[2]
    output[3] += strGap + board[3]
    output[4] += strGap + board[4]

    return

def start_game(gameLines):
    str0 = gameLines.pop(0)
    parsePlay = gameLines.pop(0)
    symbol = parsePlay.split(" ")
    str1 = "X - " + symbol[0]
    str2 = "0 - " +symbol[1]
    board = [" , , , , ,"," , , , , ,"," , , , , ,"," , , , , ,"," , , , , ,"]
    gameTrace = ["","","","",""]
    error = " "
    i = 0
    Black = "X"
    White = "O"
    while i < len(gameLines):
        if gameLines[i] =='Black makes move...':
            i+=1
            if gameLines[i] == "ERROR: Your program interrupted":
                error = "ERROR : TIME OUT,"
                break
            play(Black, gameLines[i], board, gameTrace)
        elif gameLines[i] =='White makes move...':
            i += 1
            if gameLines[i] == "ERROR: Your program interrupted":
                error = "ERROR : TIME OUT,"
                break
            play(White,gameLines[i], board, gameTrace)
        else :
            break
        i+=1
    output= []
    output.append(str0+",")
    output.append(str1+",")
    output.append(str2+",")
    if error == " ":
        part = gameLines[i+2].split(" ")
        output.append(part[0][6:-1]+" "+part[1][:-1]+",")
    else :
        output.append(gameLines[i + 3] + ","+error)
    output.append(" ,"+gameTrace[0]+",*,END")
    output.append(" ,"+gameTrace[1]+",*,END")
    output.append(" ,"+gameTrace[2]+",*,END")
    output.append(" ,"+gameTrace[3]+",*,END")
    output.append(" ," + gameTrace[4]+",*,END")
    print(output)
    return output

def main(path):
    lineCount = -1
    ouput = []
    gameCount = 0
    gameLines = []
    with open(path, 'r') as f:
        print("Reading file..")
        for line in f:
            lineCount += 1
            if (lineCount < 10 or len(line) < 2):
                continue;
            for i in range(len("=====")):
                if line[i] != "=":
                    break;
            if i == 4:
                # print(line[5:-6])
                gameLines.append(line[5:-6])
            elif line[0] != "=" and line.find("PDT") == -1 and line[0] != "C" and  line[0] != "S" :
                gameLines.append(line[:-1])
    lineCount = 0
    # print(gameLines)
    # print(len(gameLines))
    while lineCount < len(gameLines):
        if gameLines[lineCount].split(" ")[0] == "Round" :
            gameEnd = lineCount+1
            while gameLines[gameEnd].find("win") == -1 and gameLines[gameEnd].find("lose") == -1 :
                gameEnd+=1
            gameOut = start_game(gameLines[lineCount:gameEnd+1])
            ouput.extend(gameOut)
            lineCount=gameEnd
        lineCount+=1
    writeOutput(ouput,path.split(".")[0])
    print("Closing file..")
    f.close()


if __name__ == '__main__':
    start_time = time.time()
    # print("Start time :",start_time)
    path = sys.argv[1]
    main(path)
    print("COMPLETED")
    print("Duration:", time.time() - start_time)