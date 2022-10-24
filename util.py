##
# Util functions for adding, removing, updating the output state of the state_history object
##

def remove_element_from_state(output_state:list, index_x: int, index_y: int):
  """
  removes an element at position index_x, index_y in output_state[][]
  """
  output_state[index_x].pop(index_y)
  return output_state


def add_element_to_state(output_state: list, index_x: int, index_y: int, element):
  """
  adds an element at position index_x, index_y in output_state[][]
  """
  output_state[index_x].insert(index_y, element)
  return output_state


def remove_line_from_state(output_state: list, index_x: int):
  """
  removes an line/row at position index_x in output_state[][]
  """
  output_state.pop(index_x)
  return output_state


def add_line_to_state(output_state: list, index_x: int, line: list):
  """
  adds an line/row at position index_x in output_state[][]
  """
  output_state.insert(index_x, line)
  return output_state


def update_line_on_state(output_state: list, index_x: int, line: list):
  """
  updates line/row at position index_x with input line in output_state[][]
  """
  output_state[index_x] = line
  return output_state 

