Stage = 1
Num1 = 0
Num2 = 0
Operation = 0
IsFinished = False
OperationArray = ["+", "-", "*", "/",">","<"]

# SIMPLE CALCULATOR
#  Button A: reduce the value
#  Button B: add the value / repeat result
#  Button AB: confirm the number / restart

def UpdateDisplayNumber(Number):
 basic.show_number(Number, 50)

def Result(Number):
 basic.clear_screen()
 music.play_melody("C", 500)
 basic.show_number(Number, 100)

def Count():
 global IsFinished
 if Operation == 0:
  Result(Num1 + Num2)
 elif Operation == 1:
  Result(Num1 - Num2)
 elif Operation == 2:
  Result(Num1 * Num2)
 elif Operation == 3:
  Result(Num1 / Num2)
 elif Operation == 4:
  Result(max(Num1,Num2))
 elif Operation == 5:
  Result(min(Num1,Num2))
 IsFinished = True

def UpdateOperation():
 basic.show_string(OperationArray[Operation], 0)

def on_button_pressed_a():
    global Num1, Operation, Num2
    if Stage == 1:
     Num1 -= 1
     UpdateDisplayNumber(Num1)
    elif Stage == 2:
     if Operation == 0:
      Operation = 5
      UpdateOperation()
     else:
      Operation -= 1
      UpdateOperation()
    elif Stage == 3:
     Num2 -=  1
     UpdateDisplayNumber(Num2)

def on_button_pressed_ab():
    global Stage, Num1, Num2, Operation, IsFinished
    if Stage == 1:
     Stage += 1
     UpdateOperation()
    elif Stage == 2:
     Stage += 1
     UpdateDisplayNumber(0)
    elif Stage == 3:
     Stage += 1
     Count()
    elif Stage == 4:
     if IsFinished:
      Num1 = 0
      Num2 = 0
      Operation = 0
      IsFinished = False
      Stage = 1
      UpdateDisplayNumber(0)

def on_button_pressed_b():
    global Num1, Operation, Num2
    if Stage == 1:
     Num1 += 1
     UpdateDisplayNumber(Num1)
    elif Stage == 2:
     if Operation == 5:
      Operation = 0
      UpdateOperation()
     else:
      Operation += 1
      UpdateOperation()
    elif Stage == 3:
     Num2 += 1
     UpdateDisplayNumber(Num2)
    elif Stage == 4:
     Count()

input.on_button_pressed(Button.A, on_button_pressed_a)
input.on_button_pressed(Button.AB, on_button_pressed_ab)
input.on_button_pressed(Button.B, on_button_pressed_b)
UpdateDisplayNumber(0)

# Made by Daniel Peterka 3A6
