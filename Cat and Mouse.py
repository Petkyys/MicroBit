MousePosition = [0,0]
CatPosition = [2,2]
GameFinished =  False
KeyBindsAllowed= False
TimePlayed = 0
MouseMoves = 0
CatMoves = 0

Difficulty  = 1   #  Eazy(1) / Medium(2) / Hard(3)
TimeLimit   = 0   #  Time limit (s)  : 0 = No limit
MovesLimit  = 0   #  Cat moves limit : 0 = No limit
MotionDeg   = 40  #  Degrees to register movement

#Mouse Updater modules:
def SetRandomMousePosition():
    global MousePosition, MouseMoves, StartTimer
    RandomPosition = [randint(0, 4),randint(0, 4)]
    if RandomPosition[0] != 2 and RandomPosition[1] != 2:
      led.plot_brightness(RandomPosition[0],RandomPosition[1],40)
      MousePosition[0] = RandomPosition[0]
      MousePosition[1] = RandomPosition[1]
      MouseMoves = 1
    else:
      SetRandomMousePosition()

def MouseUpdatePosition(PositionX,PositionY):
   global MousePosition, MouseMoves
   led.unplot(MousePosition[0],MousePosition[1] )
   led.plot_brightness(PositionX,PositionY,40)
   MousePosition[0] = PositionX
   MousePosition[1] = PositionY
   MouseMoves += 1

def IsCornerBlock(PositionX, PositionY):
   if PositionX == 0 and PositionY == 0:
       return True
   elif PositionX == 0 and PositionY == 4:
       return True
   elif PositionX == 4 and PositionY == 0:
       return True
   elif PositionX == 4 and PositionY == 4:
       return True
   else: 
       return False

def MoveMouse():
    global MousePosition, MouseUpdatePosition, CatPosition, Difficulty
    PossibleYvalue = [-1,1]
    FurthestBlock = [0,0]
    BlockDistance = 0 
    CornerBlock = False
    Test = True
    for i in range(Math.pow(Difficulty, 3)*2):
     basic.pause(10)
     NewMousePosition = [0,0]
     if MousePosition[0] < 4 and MousePosition[0] > 0:
        NewMousePosition[0] = MousePosition[0] + randint(-1, 1)
     elif MousePosition[0] ==4:
         NewMousePosition[0] = randint(3,4)
     elif MousePosition[0] == 0:
        NewMousePosition[0] = randint(1,0)
     if NewMousePosition[0] == MousePosition[0]:
       if MousePosition[1] < 4 and MousePosition[1] > 0:
         NewMousePosition[1] = MousePosition[1] + PossibleYvalue[randint(0, 1)]
       elif MousePosition[1] ==4:
           NewMousePosition[1] = 3
       elif MousePosition[1] ==0:
         NewMousePosition[1] = 1
     else:
      if MousePosition[1] < 4 and MousePosition[1] > 0:
        NewMousePosition[1] = MousePosition[1] + randint(-1, 1)
      elif MousePosition[1] ==4:
        NewMousePosition[1] = randint(3,4)
      elif MousePosition[1] == 0:
        NewMousePosition[1] = randint(1,0)

     if (abs(NewMousePosition[0] - CatPosition[0]) + abs(NewMousePosition[1] - CatPosition[1])) > BlockDistance:
       if Difficulty >= 3 and IsCornerBlock(NewMousePosition[0], NewMousePosition[1]) == True:
           if abs(NewMousePosition[0] - CatPosition[0]) + abs(NewMousePosition[1] - CatPosition[1]) >= 6:
               FurthestBlock[0] = NewMousePosition[0]
               FurthestBlock[1] = NewMousePosition[1]
               print("Corner block allowed")
               BlockDistance = abs(NewMousePosition[0] - CatPosition[0]) + abs(NewMousePosition[1] - CatPosition[1])
               CornerBlock = IsCornerBlock(NewMousePosition[0], NewMousePosition[1])
       else:
         FurthestBlock[0] = NewMousePosition[0]
         FurthestBlock[1] = NewMousePosition[1]
         print("NewFurthestBlock: "+ NewMousePosition[0]+","+ NewMousePosition[1])
         BlockDistance = abs(NewMousePosition[0] - CatPosition[0]) + abs(NewMousePosition[1] - CatPosition[1])
         CornerBlock = IsCornerBlock(NewMousePosition[0], NewMousePosition[1])
         print("Distance: " + BlockDistance)       

     elif abs(NewMousePosition[0] - CatPosition[0]) + abs(NewMousePosition[1] - CatPosition[1]) == BlockDistance and CornerBlock == True:
        if IsCornerBlock(NewMousePosition[0], NewMousePosition[1]) == False:
         FurthestBlock[0] = NewMousePosition[0]
         FurthestBlock[1] = NewMousePosition[1]
         print("Selected another block")
         CornerBlock = False

    if NewMousePosition[0] == CatPosition[0] and NewMousePosition[1] == CatPosition[1]:
       MoveMouse()
    else:
       print("________________")
       MouseUpdatePosition(FurthestBlock[0],FurthestBlock[1])

#Cat Updater modules:
def CatUpdatePosition(PositionX, PositionY):
  global CatPosition, CatMoves, MoveMouse
  led.unplot(CatPosition[0],CatPosition[1])
  led.plot_brightness(PositionX,PositionY,255)
  CatPosition[0] = PositionX
  CatPosition[1] = PositionY
  CatMoves += 1
  basic.pause(900)
  if GameStatus() == "Continue":
     MoveMouse()

def CatSpawn():
 basic.pause(1000)
 global MousePosition, CatPosition
 while True:
   NewCatPosition = [randint(0, 4),randint(0, 4)]
   if abs(NewCatPosition[0] - MousePosition[0]) >= 2 and abs(NewCatPosition[1] - MousePosition[1]) >= 2:
       if NewCatPosition[0] != 2 and NewCatPosition[1] != 2:
         led.plot(NewCatPosition[0], NewCatPosition[1])
         CatPosition[0] = NewCatPosition[0]
         CatPosition[1] = NewCatPosition[1]
         music.play_melody("A", 350)
         break

# Base Game modules:
def GameStatusWinner():
    global GameFinished, CatPosition, CatMoves, KeyBindsAllowed
    GameFinished = True
    led.unplot(CatPosition[0],CatPosition[1])
    basic.pause(100)
    basic.show_string("WINNER!",130)
    basic.show_number(CatMoves)
    KeyBindsAllowed = True

def GameStatusLoser():
    global GameFinished,CatPosition, MousePosition, CatMoves, KeyBindsAllowed
    GameFinished = True
    led.unplot(CatPosition[0],CatPosition[1])
    led.unplot(MousePosition[0],MousePosition[1])
    basic.pause(100)
    basic.show_string("GAME OVER",130)
    basic.show_number(CatMoves)
    KeyBindsAllowed = True

def StartTimer():
  global TimeLimit, TimePlayed, GameFinished
  if TimeLimit != 0:
     while (TimeLimit > TimePlayed):
         basic.pause(1000)
         TimePlayed += 1
         if TimePlayed == TimeLimit and GameFinished == False:
             GameStatusLoser()
             break

def GameStatus():
  global MousePosition, CatPosition, CatMoves, MovesLimit, TimeLimit, TimePlayed
  if MousePosition[0] == CatPosition[0] and MousePosition[1] == CatPosition[1]:
     GameStatusWinner()
     return "Winner"
  elif CatMoves >= MovesLimit and MovesLimit != 0:
     GameStatusLoser()
     return "Loser"
  else:
     return "Continue"

def RestartGame():
    global GameFinished, SetRandomMousePosition, CatSpawn, CatMoves, MouseMoves, CatPosition, TimePlayed, KeyBindsAllowed
    if GameFinished and KeyBindsAllowed:
       led.unplot(CatPosition[0], CatPosition[1])
       CatMoves = 0
       MouseMoves = 0
       basic.show_string("")
       SetRandomMousePosition()
       CatSpawn()
       TimePlayed = 0
       GameFinished = False
       KeyBindsAllowed = False
       StartTimer()

def ShowScore():
    global CatMoves, KeyBindsAllowed, GameFinished
    if KeyBindsAllowed and GameFinished:
        basic.show_number(CatMoves)

def BaseRotation():
    global MouseMoves, CatMoves, CatPosition, GameFinished, MotionDeg
    if MouseMoves > CatMoves and GameFinished == False:
      if input.rotation(Rotation.PITCH) > MotionDeg and CatPosition[1] < 4:
         CatUpdatePosition(CatPosition[0], CatPosition[1]+1)
      elif input.rotation(Rotation.PITCH) < (MotionDeg*-1) and CatPosition[1] > 0:
         CatUpdatePosition(CatPosition[0], CatPosition[1]-1)
      elif input.rotation(Rotation.ROLL) < (MotionDeg*-1) and CatPosition[0] > 0:
         CatUpdatePosition(CatPosition[0]-1, CatPosition[1])
      elif input.rotation(Rotation.ROLL) > MotionDeg and CatPosition[0] < 4:
         CatUpdatePosition(CatPosition[0]+1, CatPosition[1])

SetRandomMousePosition()
CatSpawn()
basic.forever(BaseRotation)
StartTimer()
input.on_button_pressed(Button.A, ShowScore)
input.on_button_pressed(Button.B, RestartGame)
