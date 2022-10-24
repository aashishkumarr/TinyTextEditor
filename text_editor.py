from util import add_element_to_state, add_line_to_state, remove_element_from_state, remove_line_from_state, update_line_on_state

## Text Editor supports 
# - Typing text using normal characters(letters) and whitespace(space/newline).
# - Moving the cursor around in the text using the four arrow keys.
# - Deleting characters(including newlines) using the Backspace key.
# - Undo(one key-stroke per undo, including arrow keys)
#   Maintains a history state for undo which tracks all the changes done on the current state
#   which can later be applied for the undo operation. Similarly, a redo state can also be maintained
#   which could store all the actions needed for each undo operation.
# - [TODO] For select function, could maintain one more cursor property to maintain the end of the selection
#   and then have a clipboard field to store the copy text and paste on either the selection or at the cursor
##
class TextEditor:
  def __init__(self, cursor, output_text):
    self.cursor = cursor
    self.output_text = output_text
    self.state_history = {
      "undo": []
    }

  def __str__(self):
    """
    formats the output_text into a string
    """
    return "\n".join(["".join(inner_list) for inner_list in self.output_text])
  
  def printTextEditorState(self):
    print(self.output_text)
    print("CURSOR", self.cursor)
  

  def moveCursorUp(self):
    """
    update cursor positions for UP operation
    """
    if(self.cursor[0] > 0):
      initial_cursor = [self.cursor[0], self.cursor[1]]
      self.cursor[0] = self.cursor[0]-1
      self.cursor[1] = min(self.cursor[1], len(self.output_text[self.cursor[0]]))
      self.state_history["undo"].append(
          lambda state: {**state, "cursor": [*initial_cursor]})
    return 0

  def moveCursorDown(self):
    """
    update cursor positions for DOWN operation
    """
    if(self.cursor[0] < len(self.output_text)-1):
      initial_cursor = [self.cursor[0], self.cursor[1]]
      self.cursor[0] = self.cursor[0]+1
      self.cursor[1] = min(self.cursor[1], len(self.output_text[self.cursor[0]]))
      self.state_history["undo"].append(
          lambda state: {**state, "cursor": [*initial_cursor]})
    return 0

  def moveCursorLeft(self):
    """
    update cursor positions for LEFT operation
    """
    ## when the cursor is at the origin (leftmost location)
    initial_cursor = [self.cursor[0], self.cursor[1]]
    if(self.cursor == [0, 0]):
        return -1
    ## when the cursor is at the begining of a line, it will shift to previous line
    elif(self.cursor[0] != 0 and self.cursor[1] == 0):
      self.cursor[0], self.cursor[1] = self.cursor[0]-1, len(self.output_text[self.cursor[0]])
    else:
      self.cursor[1] = self.cursor[1]-1
    
    self.state_history["undo"].append(
        lambda state: {**state, "cursor": [*initial_cursor]})
    return 0
  
  def moveCursorRight(self):
    """
    update cursor positions for RIGHT operation
    """
    initial_cursor = [self.cursor[0], self.cursor[1]]
    no_of_lines = len(self.output_text)-1
    end_of_current_line = len(self.output_text[self.cursor[0]])
    ## when the cursor is at end of the editor (rightmost location)
    if(self.cursor == [no_of_lines, end_of_current_line]):
        return -1
    ## when the cursor is at the end of a line, it will shift to next line
    elif(self.cursor[0] != no_of_lines and self.cursor[1] == end_of_current_line):
      self.cursor[0], self.cursor[1] = self.cursor[0]+1, 0
    else:
      self.cursor[1] = self.cursor[1]+1
    self.state_history["undo"].append(
          lambda state: {**state, "cursor": [*initial_cursor]})
    return 0

  def executeBackspace(self):
    """
    - deletes the last input character or newline, updates the cursor
    - when the cursor is at the begining of a line, 
    it will add the contents of current line to previous line and 
    then removes the current line and updates the cursor
    """
    initial_cursor = [self.cursor[0], self.cursor[1]]
    ## when the cursor is the origin  (leftmost location)
    if(self.cursor == [0, 0]):
      return -1
    ## when the cursor is at the beginning of a line
    elif(self.cursor[0] > 0 and self.cursor[1] == 0):
      initial_cursor = [*self.cursor]

      index_of_current_line = self.cursor[0]
      index_of_previous_line = index_of_current_line - 1
      initial_end_of_previous_line = len(self.output_text[index_of_previous_line]) 

      initial_text_at_current_line = self.output_text[index_of_current_line]
      initial_text_at_extended_line = self.output_text[index_of_previous_line]
      
      ## adds the content of current line to previous line
      self.output_text[index_of_previous_line].extend(
          initial_text_at_current_line)
      ## then removes current line
      line_removed = self.output_text.pop(index_of_current_line)

      self.cursor[0], self.cursor[1] = index_of_previous_line, initial_end_of_previous_line

      self.state_history["undo"].append(
          lambda state: {**state, "cursor": [state["cursor"][0]+1, initial_cursor[1]],
                          "output_text":  
                            update_line_on_state(
                              add_line_to_state(state["output_text"], state["cursor"][0]+1, line_removed), 
                              state["cursor"][0], initial_text_at_extended_line)})
    else:
      self.cursor[1] = self.cursor[1]-1
      element_removed = self.output_text[self.cursor[0]].pop(self.cursor[1])
      self.state_history["undo"].append(
          lambda state: {**state, "cursor": [state["cursor"][0], state["cursor"][1]+1], 
                         "output_text":  add_element_to_state(state["output_text"], state["cursor"][0], state["cursor"][1], element_removed)})
    
    return 0

  def addsSpace(self):
    """
    adds a whitespace and update the cursor
    """
    self.output_text[self.cursor[0]].insert(self.cursor[1], " ")
    self.cursor[1] = self.cursor[1]+1 
    self.state_history["undo"].append(
        lambda state: {**state, "cursor": [state["cursor"][0], state["cursor"][1]-1], "output_text":  remove_element_from_state(state["output_text"], state["cursor"][0], state["cursor"][1]-1)})

  def executeUndo(self):
    """
    undo the last operation
    """
    if(len(self.state_history["undo"])>0):
      undo_action = self.state_history["undo"].pop()
      current_state = {
        "cursor": self.cursor,
        "output_text": self.output_text
      }
      updated_state = undo_action(current_state)
      self.output_text = updated_state["output_text"]
      self.cursor[0], self.cursor[1] = updated_state["cursor"][0], updated_state["cursor"][1]

  def addsNewline(self):
    end_of_current_line = len(self.output_text[self.cursor[0]])
    ## when cursor is at the beginning of a line,
    ## it adds an empty line at current cursor position and cursor moves to next line
    if(self.cursor[1] == 0):
        self.output_text.insert(self.cursor[0], [])
        self.cursor[0] = self.cursor[0]+1
        self.state_history["undo"].append(
            lambda state: {**state, "cursor": [state["cursor"][0]-1, state["cursor"][1]], "output_text":  remove_line_from_state(state["output_text"], state["cursor"][0]-1)})
    ## when cursor is at the end of a line,
    ## it adds a newline at next line and moves the cursor to it's start position
    elif(self.cursor[1] == end_of_current_line):
        self.cursor[0], self.cursor[1] = self.cursor[0]+1, 0
        self.output_text.insert(self.cursor[0], [])
        self.state_history["undo"].append(
            lambda state: {**state, "cursor": [state["cursor"][0]-1, self.cursor[1]], "output_text":  remove_line_from_state(state["output_text"], state["cursor"][0]-1)})
    ## when the cursor is in somewhere in the line,
    ## it splits the line into two at the cursor position
    else:
        list_before_newline = self.output_text[self.cursor[0]][:(self.cursor[1])]
        list_after_newline = self.output_text[self.cursor[0]][(-1*(end_of_current_line-self.cursor[1])):]

        self.output_text[self.cursor[0]] = list_before_newline
        self.cursor[0], self.cursor[1] = self.cursor[0]+1, 0
        self.output_text.insert(self.cursor[0], list_after_newline)

        self.state_history["undo"].append(
            lambda state: {**state, "cursor": [state["cursor"][0]-1, len(state["output_text"][state["cursor"][0]-1])], "output_text":
                           remove_line_from_state(
                              update_line_on_state(state["output_text"], 
                                state["cursor"][0]-1, 
                                state["output_text"][state["cursor"][0]-1]+state["output_text"][state["cursor"][0]]),
                              state["cursor"][0])})

  def adds_char(self, inputChar: str):
    self.output_text[self.cursor[0]].insert(self.cursor[1], inputChar)
    self.cursor[1] = self.cursor[1]+1
    self.state_history["undo"].append(
        lambda state: {**state, "cursor":  [state["cursor"][0], state["cursor"][1]-1], "output_text":  remove_element_from_state(state["output_text"], state["cursor"][0], state["cursor"][1]-1)})
  
      

  

