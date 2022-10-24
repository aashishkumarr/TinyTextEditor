
from enum import Enum


class Keystrokes(Enum):
  UP="Up"
  DOWN="DOWN"
  LEFT="Left"
  RIGHT="Right"
  BACKSPACE="Backspace"
  UNDO="Undo"
  NEWLINE="Newline"
  SPACE="Space"
  

def processInputText(l_keystrokes: list):
  cursor = [0,0]
  output_text = [[]] 
  for keystroke in l_keystrokes:
    print(keystroke)
    inputWithShift = keystroke.split("_")
    if(keystroke is Keystrokes.UP.value):
      if(cursor[0] > 0) :
        cursor[0] = cursor[0]-1
        if(cursor[1]>len(output_text[cursor[0]])):
          cursor[1] = len(output_text[cursor[0]])
      print("CURSOR", cursor)
    
    elif(keystroke is Keystrokes.DOWN.value):
      if(cursor[0] < len(output_text)-1):
        cursor[0] = cursor[0]+1
        if(cursor[1] > len(output_text[cursor[0]])):
          cursor[1] = len(output_text[cursor[0]])
      print("CURSOR", cursor)

    elif(keystroke is Keystrokes.LEFT.value):
      if(cursor == [0, 0]):
        continue
      elif(cursor[0]!=0 and cursor[1]==0):
        cursor = [cursor[0]-1, len(output_text[cursor[0]])]
      else:
        cursor[1] = cursor[1]-1
      print("CURSOR", cursor)

    elif(keystroke is Keystrokes.RIGHT.value):
      no_of_lines = len(output_text)-1
      end_of_current_line = len(output_text[cursor[0]])
      if(cursor == [no_of_lines, end_of_current_line]):
        continue
      elif(cursor[0] != no_of_lines and cursor[1] == end_of_current_line):
        cursor = [cursor[0]+1, 0]
      else:
        cursor[1] = cursor[1]+1
      print("CURSOR", cursor)

    elif(keystroke is Keystrokes.BACKSPACE.value):
      if(cursor == [0, 0]):
        continue
      elif(cursor[0] > 0 and cursor[1] == 0):
        cursor_y = len(output_text[cursor[0]-1])
        output_text[cursor[0]-1].extend(output_text[cursor[0]])
        output_text.pop(cursor[0])
        cursor = [cursor[0]-1, cursor_y]
      else:
        cursor[1] = cursor[1]-1
        output_text[cursor[0]].pop(cursor[1])
      print(output_text)
      print("CURSOR", cursor)

    elif(keystroke is Keystrokes.SPACE.value):
      output_text[cursor[0]].insert(cursor[1], " ")
      print(output_text)
      cursor[1] = cursor[1]+1  # maybe
      print(output_text)
      print("CURSOR", cursor)

    elif(keystroke is Keystrokes.UNDO.value):
      continue

    elif(keystroke is Keystrokes.NEWLINE.value):
      no_of_lines = len(output_text)
      end_of_current_line = len(output_text[cursor[0]])
      if(cursor[1] == 0):
        output_text.insert(cursor[0], [])
        cursor[0] = cursor[0]+1
      elif(cursor[1] == end_of_current_line ):
        cursor = [cursor[0]+1, 0]
        output_text.insert(cursor[0], [])
      elif(cursor[1] != 0 and cursor[1] != end_of_current_line):
        list_before_newline = output_text[cursor[0]][:(cursor[1])]
        list_after_newline = output_text[cursor[0]][(-1*(end_of_current_line-cursor[1])):]
        output_text[cursor[0]] = list_before_newline
        cursor = [cursor[0]+1, 0]
        output_text.insert(cursor[0], list_after_newline)
      print(output_text)
      print("CURSOR", cursor)


    elif(len(inputWithShift)==2 and inputWithShift[0] == "Shift" and inputWithShift[1].isalpha()):
      output_text[cursor[0]].insert(cursor[1], inputWithShift[1].upper())
      print(output_text)
      
      cursor[1] = cursor[1]+1
      print("CURSOR", cursor)

    elif(keystroke.isalnum()):
      output_text[cursor[0]].insert(cursor[1], keystroke.lower())
      print(output_text)
      
      cursor[1] = cursor[1]+1
      print("CURSOR", cursor)
  
  out = "\n".join(["".join(inner_list) for inner_list in output_text])
  print(output_text)
  print(out)


# [
#   "Shift_H", 'E', 'Y', 'Space', 'L', 'O', 'R', 'D', 'Left', 'Left', 'Left', 'Left',
#   'Newline', 'Newline', 'A', 'Right', 'Newline', 'W', 'Right', 'Right', 'L', 'Up', 'L', 'O'
# ]
# Output
# Hey

# allo
# world

# [
#     "Shift_H", 'E', 'Y', 'Space', 'L', 'O', 'R', 'D', 'Left', 'Left', 'Left', 'Left', 'Backspace',
#     'Newline', 'Backspace', 'Backspace', 'Newline', 'A', 'Right', 'Newline', 'W', 'Right', 'Right', 'L', 'Up', 'L', 'O'
# ]
# He
# allo
# world


processInputText([
    "Shift_H", 'E', 'Y', 'Space', 'L', 'O', 'R', 'D', 'Left', 'Left', 'Left', 'Left', 'Backspace',
    'Newline', 'Backspace', 'Backspace', 'Newline', 'A', 'Undo', 'Undo', 'Right', 'Newline', 'W', 'Right', 'Right', 'L', 'Up', 'L', 'O'
])
###
# Shift_H, E, Y, Space, L, O, R, D, Left, Left, Left, Left, Backspace, 
# Newline, Backspace, Backspace, Newline, A, Undo, Undo, Right, Newline,
#  W, Right, Right, L, Up, L, O
###