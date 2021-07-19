#version implementing extra conditions

import tkinter,time,random #tkinter library to create GUI, time for animations, random to have different colors

def createGrid(rows,columns,totalHeight,totalWidth): #function to draw the grid
    global board, gridFrame, totalCells #because of tkinters event-driven style global variables have to be used
    #total height and width represent the height and width of the screen

    totalCells = rows*columns
    
    board = [] #where every cell on the grid is stored
    gridFrame = tkinter.Frame(master=secondFrame,bg="gainsboro",pady=10)
    #frame that will hold the grid
    

    ratio = columns/rows #the ratio is found to make boxes look like squares


    if 0.9<=ratio<=1.1: #if the ratio is close to 1,
        #there is no need to change the size of the total grid
        
        singleWidth = totalWidth//columns #gives the width of a single cell
        singleHeight = totalHeight//rows #gives the length of a single cell

    else: #if the sizes are greatly different
        totalWidth = totalWidth*ratio
        #the total width that will be used is made to match the ratio

        if totalWidth > 850: #however, if the new size is greater than the width of the screen
            totalWidth = 850 #it is set to the max width (950)

        singleWidth = totalWidth//columns #the width and lengths are assigned
        singleHeight = totalHeight//rows


    if singleWidth<30: #the width is increased if too small
        singleWidth = 30 #the user can now click the columns more easily


    for column in range(0,columns): # for every column
        board.append([])#add a new list to the board

        number1 = tkinter.Label(gridFrame,text = str(column+1),bg = 'gainsboro')
        number1.grid(row = 0,column = column)
        #number1 is the column number that will present at the top of the grid
        #above each column so the user can identify each column to place a counter
        
        for row in range(1,rows+1): #loop starts from 1 as the first row is the number
            #a blue cell is created with black edges and width and length as created above 
            cell = tkinter.Frame(gridFrame, bg='skyblue', highlightbackground="black",
                        highlightcolor="black", highlightthickness=1,
                        width=singleWidth, height=singleHeight,)
            cell.bind("<Button-1>", clickCounter)

            #the cell is placed within the gridframe with the corresponding row and column
            cell.grid(row=row, column=column)
            board[column].append(cell) #the cell is appended to the column

        number2 = tkinter.Label(gridFrame,text = str(column+1),bg = 'gainsboro')
        number2.grid(row = row+1,column = column)
        #number2 is the same as number1 but is added to the bottom of every column
        
    gridFrame.grid(row =1) #the grid is placed in the window (rather in secondFrame)
    

def startGame(): #function called when the startgame button is pressed 
    global gridFrame,currentPlayer,winCon,end,totalCounters,players,cornerCount #global variables used due to event driven nature of tkinter
    global continueRound,playerWins,currentRound,leaderboardLabel,leaderFrame
    
    end = False
    currentPlayer = 0 #current player is set to 0, the first player
    displayPlayer() #the player is displayed in the main info label
    totalCounters = 0
    
    winCon = getWinCon() #data entered by user is taken
    players = getPlayers()
    cornerCount = getCornerCounter() 
    
    if not continueRound: #if this is not a new round, i.e. completely new game
        playerWins = [0]*players #player wins are all 0
        currentRound = 0 #the current round is 0 
        
        leaderboardLabel.destroy() #destroy the old data about rounds
        leaderFrame.destroy()

        #add new placeholder data for rounds:
        leaderboardLabel = tkinter.Label(master = leaderboardFrame, text = "Round 1",font=('Calibri',23),bg="gainsboro")
        leaderFrame = tkinter.Frame(master=leaderboardFrame,bg = 'gainsboro')
        placeholderLbl = tkinter.Label(master = leaderFrame, text='*This is where the leaderboard will appear*',font=('Calibri',15),bg="gainsboro")

        leaderboardLabel.pack() #the widgets are packed into the frame
        leaderFrame.pack()
        placeholderLbl.pack()

    else: #if this is a new round of an ongoing game
        
        if players>len(playerWins): #if the number of players increased
            for i in range (0,players-len(playerWins)): #add a 0 to player wins for each new player
                playerWins.append(0)
                
        elif players < len(playerWins): #if amount of players decreased
            while len(playerWins) != players:
                del playerWins[-1] #remove player data from the end of the list until enough players
        
    
    gridInfo = gridEntry.get() #the grid sizes entered by the user is received
    gridInfo = gridInfo.strip().split() #sanitised
    
    gridFrame.destroy() #the older grid is destroyed

    #if statement checks if the input entered is not valid
    if len(gridInfo)!=2 or not (gridInfo[0].isdigit() and gridInfo[1].isdigit()) or int(gridInfo[0])<1 or int(gridInfo[1])<1:
        #if not valid:
        gridEntry.delete(0,tkinter.END) #the entry is cleared
        gridEntry.config(fg='red') 
        gridEntry.insert(0,'Invalid grid: using 6 7') #the entry is replaced with text to show that 6 7 is being used
        createGrid(6,7,660,660) #the grid is created using original settings

        
    else: #if grid sizes entered is valid
        createGrid(int(gridInfo[0]),int(gridInfo[1]),660,660) #grid is created using user input

def checkGrid(event): #when keyboard focus is taken away from the gridEntry
    
    info = gridEntry.get() #the info in the grid entry is taken
    info = info.strip().split() #sanitised
    mainInfoLabel.config(fg='red') #the info label color is changed to red
    
    if len(info)!=2 or not (info[0].isdigit() and info[1].isdigit()) or int(info[0])<1 or int(info[1])<1:
        #if invalid: appropiate text is shown
        mainInfoLabel['text'] = "Invalid Grid: Enter 2 positive integers."
    elif int(info[0])>25 or int(info[1])>25:
        #if the grid size is too big, the user is cautioned
        mainInfoLabel['text'] = "Caution, grid size may lead to bad experience."
    else:#valid grid size entered is shown
        mainInfoLabel['text'] = "Valid grid size entered."
        
def updateAnimations(): #function called whenever a radio button is clicked
    global animations #the global value is changed as tkinter is event driven
    
    if animationChoice.get() == 1: #if checkbox is clicked
        animations = True
    else:
        animations = False
    
def performAnimation(column,index): #function used to show animations
    global drop #the global value is changed as tkinter is event driven

    #drop is used to see if the next player can drop a counter
    drop = False #next player cant drop a counter as this one is being dropped
    
    for i in range(0,index):#loops from the top of the grid to the index that will be filled
        
        board[column][i].configure(background=colors[currentPlayer])
        #color of cell is changed to counter color
        time.sleep(0.1) #wait 0.1 second 
        window.update()#update the GUI window
        
        board[column][i].configure(background='skyblue')#color is changed back

    drop = True #the next player can now drop a counter since the animation is over
        
def placeCounter(column): #function used to place counter given a column
    global currentPlayer, board, animations,end,totalCounters,currentRound,playerWins
    
    if not end: #if the game didnt finish, the user is allowed to enter a new counter
        if board[column-1][0]['bg'] != 'skyblue':
            mainInfoLabel['text'] = "That column is full!"
            
        else:
            for i in range (len(board[0])-1,-1,-1):
            #loops through the bottom of the column to the top
                
                if board[column-1][i]['bg'] == 'skyblue':#if it is empty(blue)

                    if animations == True:
                        performAnimation(column-1,i)

                    board[column-1][i].configure(background=colors[currentPlayer])#color is changed
                    totalCounters +=1

                    
                    largest = longestLine(column-1,i,[colors[currentPlayer]]) #finds the longest line of same color
                    
                    if largest>=winCon: # if this exceeds the winning condition
                        winner = currentPlayer #winner is set
                        mainInfoLabel['text'] = 'Player '+str(winner+1)+' is the winner!'
                        end = True
                        currentRound += 1
                        playerWins[winner] +=1
                        
                        finishedRound(playerWins)

                        
                    elif totalCounters == totalCells: #if the total counters fill up the whole board
                        winner = None #there is a tie
                        end = True
                        mainInfoLabel['text'] = 'There is a draw!'
                        mainInfoLabel.config(fg='black')
                        currentRound +=1
            
                        finishedRound(playerWins)
                        
                        
                    else: #else its the next players turn
                        currentPlayer = (currentPlayer+1)%players#next players turn
                        displayPlayer()#display info of new player
                        
                    break #the column is dropped so we can leave the loop
                

                
def displayPlayer(): #function used to display the current players turn
    mainInfoLabel.config(fg=colors[currentPlayer])#the color is changed to the current player
    mainInfoLabel['text'] = 'Player '+str(currentPlayer+1)+"'s turn. (Click any column or type on the right)"#the text is changed

def enterCounter(event):#function called when the user presses enter
    if not end and drop:
        column = columnEntry.get().strip() #text from entry is taken
        columnEntry.delete(0,tkinter.END) #entry is cleared

        #accepts only non-negative integers
        if column.isdigit(): #checks if the string is an integer
            column = int(column) #cast to integer
            if 0<column<=len(board): #checks if it is a valid column
                placeCounter(column)

            else:
                mainInfoLabel['text'] = "Thats not a column!"
            
        else:
            mainInfoLabel['text'] = "Enter a positive integer."


def clickCounter(event): #when a cell is clicked, this function is called
    if drop:
        cell = event.widget #the cell that was clicked is received
        column = cellColumn(board,cell)+1 #the column its in is identified

        placeCounter(column) #counter is placed in that column
    
    
def cellColumn(board, cell): #function used to find the column index of a cell in a 2d list
    for i, x in enumerate(board): #loops through the 2d list
        if cell in x:#if the cell is in the column
            return i #column index is returned
    
def checkWinCon(event): #checks if entered data is valid
    global winCon
    info = winEntry.get() 
    info = info.strip() #sanitised

    if info.isdigit() and int(info)>0: #checks if integer: appropriate message shown
        winCon = int(info)
        mainInfoLabel['text'] = "Valid win condition entered."
    else:
        mainInfoLabel['text'] = "Invalid Win Condition: Enter an integer."


def getWinCon(): #function used to find the win conditon i.e. how many in a row
    info = winEntry.get()
    info = info.strip() #sanitised

    if info.isdigit() and int(info)>0:
        return int(info) #returns the input if vlaid
    else:
        winEntry.config(fg='red')
        winEntry.delete(0,tkinter.END) #the prewwritten text in the entry is deleted
        winEntry.insert(0,'Invalid win condition: using 4') #the entry is replaced with text to show that 4 is being used
        return 4 #if invalid uses 4


def longestLine(index1,index2,colors):  #function used to find the longest line of a color
    xlength,ylength,new1,new2 = 0,0,index1,index2

    corners = [board[0][0],board[0][len(board[0])-1],board[len(board)-1][0],board[len(board)-1][len(board[0])-1]]
    
    
    #check total x direction:
    
    while new1<len(board)and board[new1][new2]['bg'] in colors:
    #with every iteration, moves towards the right of the counter
    #until a different color is found or the board limit is reached
        if board[new1][new2] not in corners:
            xlength += 1 #the horizontal length is increased 
        else:
            xlength+= cornerCount
            
        new1 += 1 #the next index will be checked
            
        
    new1 = index1 -1   #the index is reset back

    #similarly, checks the left side of the counter
    while new1>=0 and board[new1][new2]['bg'] in colors:
        if board[new1][new2] not in corners: #if the cell isnt in a corner
            xlength += 1
        else:
            xlength+= cornerCount #if it is, add the corner value on instead
        new1 -= 1
    new1 = index1

    #check total y direction:
    #checks above and below the counter to find the total vertical length
    while new2<len(board[0]) and board[new1][new2]['bg'] in colors:
        if board[new1][new2] not in corners: #same as above
            ylength += 1
        else:
            ylength += cornerCount
        new2 += 1
    new2 = index2-1

    while new2>=0 and board[new1][new2]['bg'] in colors:
        if board[new1][new2] not in corners:
            ylength += 1
        else:
            ylength += cornerCount
        new2 -= 1
    new2 = index2

    #checking diagonals:
    diag1,diag2 = 0,0

    #checks both diagonals going a square diagonally each time
    while new1<len(board)and new2<len(board[0]) and board[new1][new2]['bg'] in colors:
        if board[new1][new2] not in corners:
            diag1 += 1
        else:
            diag1 += cornerCount
        new1 += 1
        new2+= 1
    new1,new2 = index1-1,index2-1

    while new1>=0 and new2>=0 and board[new1][new2]['bg'] in colors:
        if board[new1][new2] not in corners: #same as above
            diag1 += 1
        else:
            diag1 += cornerCount
            
        new1 -= 1
        new2-= 1

    new1,new2 = index1,index2
    #print('diag1',diag1)

    while new1>=0 and new2<len(board[0]) and board[new1][new2]['bg'] in colors:
        if board[new1][new2] not in corners:
            diag2 += 1
        else:
            diag2+=cornerCount
        new1 -= 1
        new2+= 1

    new1,new2 = index1+1,index2-1
    
    while new1<len(board) and new2>=0 and board[new1][new2]['bg'] in colors:
        if board[new1][new2] not in corners:
            diag2 += 1
        else:
            diag2 += cornerCount
        new1 += 1
        new2-= 1
    new1,new2 = index1,index2
    #print('diag2',diag2,'\n')
        
    return max(xlength,ylength,diag1,diag2) #returns the longest line formed

def clearEntry(event): #function used to empty the entry which calls this
    widget = event.widget

    widget.delete(0,tkinter.END) #the placeholder text in the entry is deleted
    widget.config(fg='black') #the color is changed to black
    
def checkPlayers(event):#function that checks whether entered data is valid
    info = playersEntry.get()
    info = info.strip() #sanitised

    if info.isdigit() and 0<int(info)<386: #checks if valid must be between 0 and 386 
        mainInfoLabel['text'] = "Valid player count entered."
    else:
        mainInfoLabel['text'] = "Invalid Players: Enter an integer between 1 and 385."

def getPlayers(): #function that returns the number of players
    info = playersEntry.get()
    info = info.strip() #sanitised

    if info.isdigit() and 0<int(info)<386:
        return int(info)
    else:
        playersEntry.config(fg='red')
        playersEntry.delete(0,tkinter.END) #the prewwritten text in the entry is deleted
        playersEntry.insert(0,'Invalid players: using 2') #the entry is replaced with text to show that 4 is being used
        return 2 #if invalid uses 2

def checkCornerCounter(event): #function that checks if the text entered by user is correct
    global cornerCount #corner count can change during game
    info = cornerCounterEntry.get()
    info = info.strip()

    if info.isdigit() and int(info) >= 0: #checks if data is valid - corner counters can be 0
        cornerCount = int(info)
        mainInfoLabel['text'] = "Valid corner counter value entered."
    else:
        mainInfoLabel['text'] = "Invalid Corner Count: Enter an integer."


def getCornerCounter(): #inputs and validates the value for the counter entered by the user
    info = cornerCounterEntry.get()#the data is input
    info = info.strip()

    if info.isdigit() and int(info) >= 0: #if it is an integer bigger than 0
        return int(info) #the value is accepted
    
    else: #1 is used instead and the user is told it is invalid
        cornerCounterEntry.config(fg='red')
        cornerCounterEntry.delete(0,tkinter.END) #the prewwritten text in the entry is deleted
        cornerCounterEntry.insert(0,'Invalid corner count: using 1') #the entry is replaced with text to show that 4 is being used
        return 1 #if invalid uses 1

def buildLeaderboard(wins): #function that builds the leaderboard on the right hand side of the screen
    global leaderFrame,leaderboardLabel
    leaderFrame.destroy() #the old leaderboard data is destroyed
    leaderboardLabel.destroy()
    
    #new leaderboard frames are created
    leaderboardLabel = tkinter.Label(master = leaderboardFrame, text = "Round "+ str(currentRound),font=('Calibri',20),bg="gainsboro")
    leaderFrame = tkinter.Frame(master=leaderboardFrame,bg="gainsboro",pady=10)

    players = [[wins[i],i,colors[i]] for i in range (0,len(wins))] #the players data contains [wins,index,color] for each player
    players.sort(reverse = True) #the list is sorted in descending order

    displayed = 5    
    if len(players)>displayed: #if more than x players, display x players - only the top x players are displayed
        players = players[:displayed-1] #this value must be 1 less than the value in the if statement

    for i in players: #for each player
        line = tkinter.Label(leaderFrame, bg='gainsboro',fg = i[2],pady = 5,font = ('Calibri',20),text= 'Player '+str(i[1]+1)+': '+str(i[0]))
        line.pack() #create a new label for the player and display it
        
        
    leaderboardLabel.pack() #pack the new frames
    leaderFrame.pack()

def finishedRound(wins): #once a round is finished, this round is called
    global rounds, nextRoundButton

    buildLeaderboard(wins) #build the leaderboard after the round
    
    #create a button that will start a new round when pressed
    nextRoundButton = tkinter.Button(master=leaderboardFrame,padx=20,pady=10,highlightbackground='lightyellow',
                            text = "Play Next Round!", command = nextRound, height = 2,width = 15)
    
    nextRoundButton.pack() #pack this button below the leaderboard
    
def nextRound(): #this function will be called whenever a new round will be played
    global continueRound
    
    nextRoundButton.destroy() #the next round button is destroyed
    continueRound = True #continue round is set to true
    startGame() #the game starts

def buttonStart(): #this function will be called whenever a totally new game will start
    global continueRound
    try:
        nextRoundButton.destroy() #destroy the button (there might not be one so try is used)
    except:
        pass
    continueRound = False #set to false since this is not a new round
    startGame() #start the game
    
window = tkinter.Tk() #window is create
window.title("Connectron") #the title is connectron
window.columnconfigure(0,minsize = 200)#this adds space between the left hand side and the right hand side of the GUI
window.configure(bg='lightyellow') #sets background color to the color gainsboro

#colors for each player
extraColors = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace','linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff','navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender','lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray','light slate gray', 'gray', 'light grey', 'midnight blue', 'cornflower blue', 'dark slate blue','slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue','dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue','light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise','cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark olive green','dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green','lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green','forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow','light yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown','indian red','sandy brown','dark salmon', 'salmon', 'light salmon', 'orange','coral', 'light coral', 'tomato', 'orange red','hot pink','pink','pale violet red', 'maroon', 'medium violet red', 'violet red','medium orchid', 'dark orchid', 'dark violet', 'blue violet','medium purple','thistle', 'snow2', 'snow3','snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2','AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2','PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4','LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3','cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4','LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3','MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3','SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4','DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2','SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3','SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3','LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4','LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2','PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3','CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3','cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4','aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3','DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2','PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4','green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4','OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2','DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4','LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4','LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4','gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4','DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4','RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2','IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1','burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1','tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2','firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2','salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2','orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4','coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2','OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4','HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4','LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1','PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2','maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4','magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1','plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3','MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4','purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2','MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4','gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28', 'gray99']
eightColors = ['dark green','deep pink','dark orange','purple','saddle brown','navy','light green','gray35']
#up to 385 colors
random.shuffle(eightColors)#the 8 colors after the orignal red and yellow are shuffled
random.shuffle(extraColors)#the extra colors are shuffled to provide a more unique experience for multiple players
tenColors = ['red','yellow']+eightColors

colors = tenColors + extraColors
#the colors of each user will be shown as above

#first frame is left side, second Frame is main grid and third frame is right side of the gui
firstFrame = tkinter.Frame(master=window,bg="gainsboro",pady=10,padx=20)
secondFrame = tkinter.Frame(master = window, bg ="gainsboro",pady=15,padx=15,width = 900, height = 800)
thirdFrame = tkinter.Frame(master=window,bg="gainsboro",pady=10,padx=20)

#this label is just above the grid, showing whose player it is and other information
mainInfoLabel = tkinter.Label(secondFrame,bg='gainsboro',text='Welcome to Connectron!',height=1,fg='red',font=("Calibri",26))
mainInfoLabel.grid(row=0) #the label is packed into the frame


#global variables used to control flow
drop = True
animations = False
end = False
totalCounters = 0 #total number of counters placed, used to identify a draw

#Starting values of the game
winCon = 4
players = 2
cornerCount = 1
currentRound = 0
playerWins = [0]*players
continueRound = False

currentPlayer = 0
createGrid(6,7,660,660) #the starting board is a 6 by 7 grid which is created
window.bind('<Return>',enterCounter)



##left hand side of the grid
#Grid info
gridInfoFrame = tkinter.Frame(master=firstFrame,bg="gainsboro",pady=10) #the frame that contains the grid stuff

gridLabel = tkinter.Label(master = gridInfoFrame, text = "Enter grid size (row,column):",bg="gainsboro")#grid label
gridEntry = tkinter.Entry(master = gridInfoFrame, width = 20,bg="light yellow") #grid entry
gridEntry.insert(0,'example: 6 7') #contains the placerholder to give an idea to user
gridEntry.config(fg='grey')

gridLabel.pack() #the widhgets are packed into the frame
gridEntry.pack()

gridInfoFrame.pack() #the frame is placed 

gridEntry.bind("<FocusIn> ", clearEntry) #when the user presses the entry, it is cleared
gridEntry.bind("<FocusOut> ",checkGrid) #when the user presses out of the entry, an appropiarte message is shown


#enter win conditon
winFrame = tkinter.Frame(master=firstFrame,bg="gainsboro",pady=10) #the frame that contains the grid stuff

winLabel = tkinter.Label(master = winFrame, text = "Enter length needed to win:",bg="gainsboro")#grid label
winEntry = tkinter.Entry(master = winFrame, width = 20,bg="light yellow") #grid entry
winEntry.insert(0,'example: 4') #contains the placerholder to give an idea to user
winEntry.config(fg='grey')

winLabel.pack() #the widhgets are packed into the frame
winEntry.pack()

winFrame.pack() #the frame is placed 

winEntry.bind("<FocusIn> ", clearEntry) #when the user presses the entry, it is cleared
winEntry.bind("<FocusOut> ",checkWinCon) #when the user presses out of the entry, an appropiarte message is shown

#enter players
playersFrame = tkinter.Frame(master=firstFrame,bg="gainsboro",pady=10) #the frame that contains the grid stuff

playersLabel = tkinter.Label(master = playersFrame, text = "Enter number of players:",bg="gainsboro")#grid label
playersEntry = tkinter.Entry(master = playersFrame, width = 20,bg="light yellow") #grid entry
playersEntry.insert(0,'example: 2') #contains the placerholder to give an idea to user
playersEntry.config(fg='grey')

playersLabel.pack() #the widhgets are packed into the frame
playersEntry.pack()

playersFrame.pack() #the frame is placed 

playersEntry.bind("<FocusIn> ", clearEntry) #when the user presses the entry, it is cleared
playersEntry.bind("<FocusOut> ",checkPlayers) #when the user presses out of the entry, an appropiarte message is shown

#enter corner counter points

cornerCounterFrame = tkinter.Frame(master=firstFrame,bg="gainsboro",pady=10) #the frame that contains the grid stuff

cornerCounterLabel = tkinter.Label(master = cornerCounterFrame, text = "Enter Corner Values:",bg="gainsboro")#grid label
cornerCounterEntry = tkinter.Entry(master = cornerCounterFrame, width = 20,bg="light yellow") #grid entry
cornerCounterEntry.insert(0,'example: 2') #contains the placerholder to give an idea to user
cornerCounterEntry.config(fg='grey')

cornerCounterLabel.pack() #the widgets are packed into the frame
cornerCounterEntry.pack()
cornerCounterFrame.pack() #the frame is placed 

cornerCounterEntry.bind("<FocusIn> ", clearEntry) #when the user presses the entry, it is cleared
cornerCounterEntry.bind("<FocusOut> ",checkCornerCounter) #when the user presses out of the entry, an appropiarte message is shown


#animation  button
animationChoice = tkinter.IntVar()

animCheckbox = tkinter.Checkbutton(master=firstFrame,command = updateAnimations,variable=animationChoice, onvalue=1, offvalue=0,
                                   text= "Counter drop animations",bg = 'gainsboro',pady=15)
animCheckbox.pack()

#start game
startButton = tkinter.Button(master=firstFrame,padx=20,pady=10,highlightbackground='lightyellow',
                            text = "Start a New Game!", command = buttonStart, height = 2,width = 15)
startButton.pack()

startButton.bind("<1>", lambda event: startButton.focus_set())

##right hand side:

#entry that will be used to enter a counter - in development
columnFrame = tkinter.Frame(master=thirdFrame,bg="gainsboro") #frame that contains the column entry

columnLabel = tkinter.Label(master=columnFrame,bg="gainsboro",text="Type a column number and press enter:",font=('Calibri',15))
columnEntry = tkinter.Entry(master = columnFrame, width = 20,bg="light yellow")

#column label and entry are packed
columnLabel.pack(pady=5) #pad y so there is some space between them
columnEntry.pack()

columnFrame.pack()

#leaderboard

leaderboardFrame = tkinter.Frame(master=thirdFrame,bg="gainsboro",pady=15) #the frame that contains the grid stuff

leaderboardLabel = tkinter.Label(master = leaderboardFrame, text = "Round 1",font=('Calibri',23),bg="gainsboro")
leaderFrame = tkinter.Frame(master=leaderboardFrame,bg = 'gainsboro')
placeholderLbl = tkinter.Label(master = leaderFrame, text='*This is where the leaderboard will appear*',font=('Calibri',15),bg="gainsboro")
#place holder label only appears at the start of a game

leaderboardLabel.pack() #the widgets are packed into the frame
leaderFrame.pack()

leaderboardFrame.pack() #the frame is placed
placeholderLbl.pack()


#the main frames are packed
firstFrame.grid(row = 0, column = 0, sticky = "nsew")
secondFrame.grid(row=0, column = 1, sticky = "ns")
thirdFrame.grid(column=2,row=0,sticky = 'nsew')

window.mainloop()