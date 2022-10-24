
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

def updateOutputState(output_states, **map_of_values_to_be_updated):
  for index, value in map_of_values_to_be_updated.iteritems():
    output_states[index] = value
  return output_states


def removeElementFromState(output_state, index_x, index_y):
  output_state["output_text"][index_x].pop(index_y)
  return output_state


def addElementToState(output_state, index_x, index_y, element):
  output_state["output_text"][index_x].insert(index_y, element)
  return output_state

def removeLineFromState(output_state, index_x):
  output_state["output_text"].pop(index_x)
  return output_state


def addLineToState(output_state, index_x, line):
  output_state["output_text"].insert(index_x, line)
  return output_state


def updateLineOnState(output_state, index_x, line):
  output_state["output_text"][index_x] = line
  return output_state

def processInputText(l_keystrokes: list):
  current_state = {
    "cursor": [0, 0],
    "output_text": [[]]
  }

  state_history = {
    "undo": []
  }

  cursor = current_state["cursor"]
  output_text = current_state["output_text"]
  for keystroke in l_keystrokes:
    print(keystroke)
    inputWithShift = keystroke.split("_")
    if(keystroke is Keystrokes.UP.value):
      if(cursor[0] > 0) :
        initial_cursor = [cursor[0], cursor[1]]
        cursor[0] = cursor[0]-1
        if(cursor[1]>len(output_text[cursor[0]])):
          cursor[1] = len(output_text[cursor[0]])
        state_history["undo"].append(lambda state: {**state, "cursor": [*initial_cursor]})
      print(output_text)
      print("CURSOR", cursor)
    
    elif(keystroke is Keystrokes.DOWN.value):
      if(cursor[0] < len(output_text)-1):
        initial_cursor = [cursor[0], cursor[1]]
        cursor[0] = cursor[0]+1
        if(cursor[1] > len(output_text[cursor[0]])):
          cursor[1] = len(output_text[cursor[0]])
        state_history["undo"].append(lambda state: {**state, "cursor": [*initial_cursor]})
      print(output_text)
      print("CURSOR", cursor)

    elif(keystroke is Keystrokes.LEFT.value):
      initial_cursor = [cursor[0], cursor[1]]
      if(cursor == [0, 0]):
        continue
      elif(cursor[0]!=0 and cursor[1]==0):
        cursor[0], cursor[1] = cursor[0]-1, len(output_text[cursor[0]])
      else:
        cursor[1] = cursor[1]-1
      state_history["undo"].append(lambda state: {**state, "cursor": [*initial_cursor]})
      print(output_text)
      print("CURSOR", cursor)

    elif(keystroke is Keystrokes.RIGHT.value):
      initial_cursor = [cursor[0], cursor[1]]
      no_of_lines = len(output_text)-1
      end_of_current_line = len(output_text[cursor[0]])
      if(cursor == [no_of_lines, end_of_current_line]):
        continue
      elif(cursor[0] != no_of_lines and cursor[1] == end_of_current_line):
         cursor[0], cursor[1] = cursor[0]+1, 0
      else:
        cursor[1] = cursor[1]+1
      state_history["undo"].append(lambda state: {**state, "cursor": [*initial_cursor]})
      print(output_text)
      print("CURSOR", cursor)

    elif(keystroke is Keystrokes.BACKSPACE.value):
      initial_cursor = [cursor[0], cursor[1]]
      if(cursor == [0, 0]):
        continue
      elif(cursor[0] > 0 and cursor[1] == 0):
        initial_cursor = [*cursor]

        index_of_current_line = cursor[0]
        index_of_line_extended = index_of_current_line - 1
        cursor_y = len(output_text[index_of_line_extended])
        initial_text_at_current_line = output_text[index_of_current_line]
        initial_text_at_extended_line = output_text[index_of_line_extended]

        output_text[index_of_line_extended].extend(
            initial_text_at_current_line)
        line_removed = output_text.pop(index_of_current_line)
        cursor[0], cursor[1] = index_of_line_extended, cursor_y

        state_history["undo"].append(
            lambda state: {**state, "cursor": [state["cursor"][0]+1, initial_cursor[1]],
                           "output_text":  
                           updateLineOnState(addLineToState(
                               state, state["cursor"][0]+1, line_removed), state["cursor"][0], initial_text_at_extended_line)["output_text"]})
      else:
        cursor[1] = cursor[1]-1
        element_removed = output_text[cursor[0]].pop(cursor[1])
        state_history["undo"].append(
            lambda state: {**state, "cursor": [state["cursor"][0], state["cursor"][1]+1], "output_text":  addElementToState(state, state["cursor"][0], state["cursor"][1], element_removed)["output_text"]})
      
      print(output_text)
      print("CURSOR", cursor)

    elif(keystroke is Keystrokes.SPACE.value):
      initial_cursor = [cursor[0], cursor[1]]
      output_text[cursor[0]].insert(cursor[1], " ")
      cursor[1] = cursor[1]+1  # maybe
      state_history["undo"].append(
          lambda state: {**state, "cursor": [state["cursor"][0], state["cursor"][1]-1], "output_text":  removeElementFromState(state, state["cursor"][0], state["cursor"][1]-1)["output_text"]})
      print(output_text)
      print("CURSOR", cursor)

    elif(keystroke is Keystrokes.UNDO.value):
      if(len(state_history["undo"])>0):
        
        
        undo_action = state_history["undo"].pop()
  
        updated_state = undo_action(current_state)
        
        output_text = updated_state["output_text"]
        cursor[0], cursor[1] = updated_state["cursor"][0], updated_state["cursor"][1]
        print(output_text)
        print("CURSOR", cursor)

    elif(keystroke is Keystrokes.NEWLINE.value):
      initial_cursor = [cursor[0], cursor[1]]
      # state_history["undo"].append(
      #     lambda state: {**state, "cursor": [*initial_cursor], "output_text": [[*l] for l in output_text ]})
      no_of_lines = len(output_text)
      end_of_current_line = len(output_text[cursor[0]])
      if(cursor[1] == 0):
        output_text.insert(cursor[0], [])
        cursor[0] = cursor[0]+1
        state_history["undo"].append(
            lambda state: {**state, "cursor": [state["cursor"][0]-1, state["cursor"][1]], "output_text":  removeLineFromState(state, state["cursor"][0]-1)["output_text"]})
      elif(cursor[1] == end_of_current_line ):
        cursor[0], cursor[1] = cursor[0]+1, 0
        output_text.insert(cursor[0], [])
        state_history["undo"].append(
            lambda state: {**state, "cursor": [state["cursor"][0]-1, cursor[1]], "output_text":  removeLineFromState(state, state["cursor"][0]-1)["output_text"]})
      elif(cursor[1] != 0 and cursor[1] != end_of_current_line):
        initial_cursor = [*cursor]
        list_before_newline = output_text[cursor[0]][:(cursor[1])]

        list_after_newline = output_text[cursor[0]][(-1*(end_of_current_line-cursor[1])):]
        output_text[cursor[0]] = list_before_newline
        cursor[0], cursor[1] = cursor[0]+1, 0
        output_text.insert(cursor[0], list_after_newline)

        state_history["undo"].append(
            lambda state: {**state, "cursor": [state["cursor"][0]-1, len(state["output_text"][state["cursor"][0]-1])], "output_text":
            removeLineFromState(updateLineOnState(state, state["cursor"][0]-1, state["output_text"][state["cursor"][0]-1]+state["output_text"][state["cursor"][0]]),
             state["cursor"][0])["output_text"]})
      print(output_text)
      print("CURSOR", cursor)


    elif(len(inputWithShift)==2 and inputWithShift[0] == "Shift" and inputWithShift[1].isalpha()):
      initial_cursor = [cursor[0], cursor[1]]
      
      output_text[cursor[0]].insert(cursor[1], inputWithShift[1].upper())
      print(output_text)
      
      cursor[1] = cursor[1]+1
      print("CURSOR", cursor)
      state_history["undo"].append(
          lambda state: {**state, "cursor":  [state["cursor"][0], state["cursor"][1]-1], "output_text":  removeElementFromState(state, state["cursor"][0], state["cursor"][1]-1)["output_text"]})
    
    elif(keystroke.isalnum()):
      initial_cursor = [cursor[0], cursor[1]]
     
      output_text[cursor[0]].insert(cursor[1], keystroke.lower())
      print(output_text)
      
      cursor[1] = cursor[1]+1
      print("CURSOR", cursor)
      state_history["undo"].append(
          lambda state: {**state, "cursor": [state["cursor"][0], state["cursor"][1]-1], "output_text":  removeElementFromState(state, state["cursor"][0], state["cursor"][1]-1)["output_text"]})
  
  out = "\n".join(["".join(inner_list)
                  for inner_list in current_state["output_text"]])
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
# processInputText([
#     "Shift_H", 'E', 'Y', 'Space', 'L', 'O', 'R', 'D', 'Left', 'Left', 'Left', 'Left', 'Backspace',
#     'Newline', 'Backspace', 'Backspace', 'Newline', 'A', 'Right', 'Newline', 'W', 'Right', 'Right', 'L', 'Up', 'L', 'O'
# ])
# He
# allo
# world



processInputText([
    "Shift_H",  'E', 'Y', 'Space','L', 'O', 'R', 'D', 'Left', 'Left',
    'Left', 'Left', 'Backspace', 'Newline',  'Backspace', 'Backspace', 'Newline', 'A', 'Undo',
     'Undo', 'Right', 'Newline', 'W', 'Right', 'Right', 'L', 'Up', 'L', 'O'
])
###
# Shift_H, E, Y, Space, L, O, R, D, Left, Left, Left, Left,
#  Backspace, Newline, Backspace, Backspace, Newline, A, Undo,
#  Undo, Right, Newline, W, Right, Right, L, Up, L, O
###