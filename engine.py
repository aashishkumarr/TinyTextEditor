
from enum import Enum

from text_editor import TextEditor

class Keystrokes(Enum):
  UP="Up"
  DOWN="DOWN"
  LEFT="Left"
  RIGHT="Right"
  BACKSPACE="Backspace"
  UNDO="Undo"
  NEWLINE="Newline"
  SPACE="Space"


def print_output_text(l_keystrokes: list):
  """
  runs process_input_text on l_keystrokes list and print the resultant string
  """
  print(process_input_text(l_keystrokes))


def process_input_text(l_keystrokes: list):
  """
  parse the input list of keystrokes and do the operations to 
  returns the text editor object
  """
  text_editor = TextEditor([0,0], [[]])
  for keystroke in l_keystrokes:
    inputWithShift = keystroke.split("_")

    if(keystroke is Keystrokes.UP.value):
      text_editor.moveCursorUp()
    
    elif(keystroke is Keystrokes.DOWN.value):
      text_editor.moveCursorDown()

    elif(keystroke is Keystrokes.LEFT.value):
      text_editor.moveCursorLeft()

    elif(keystroke is Keystrokes.RIGHT.value):
      text_editor.moveCursorRight()
      

    elif(keystroke is Keystrokes.BACKSPACE.value):
      text_editor.executeBackspace()
      

    elif(keystroke is Keystrokes.SPACE.value):
      text_editor.addsSpace()
      

    elif(keystroke is Keystrokes.UNDO.value):
      text_editor.executeUndo()
      

    elif(keystroke is Keystrokes.NEWLINE.value):
      text_editor.addsNewline()
      
    ## adds uppercase letters when keystrokes is with shift
    elif(len(inputWithShift)==2 and inputWithShift[0] == "Shift" and inputWithShift[1].isalpha()):
      text_editor.adds_char(inputWithShift[1].upper())
    
    elif(keystroke.isalnum()):
     text_editor.adds_char(keystroke.lower())
     
  return text_editor


print_output_text([
    "Shift_H",  'E', 'Y', 'Space', 'L', 'O', 'R', 'D', 'Left', 'Left',
    'Left', 'Left', 'Backspace', 'Newline',  'Backspace', 'Backspace', 'Newline', 'A', 'Undo',
    'Undo', 'Right', 'Newline', 'W', 'Right', 'Right', 'L', 'Up', 'L', 'O'
])

