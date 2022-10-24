from engine import process_input_text


TEST_INPUTS = [
  {
    "input": [
        "Shift_H", 'E', 'Y', 'Space', 'L', 'O', 'R', 'D', 'Left', 'Left', 'Left', 'Left', 'Backspace',
        'Newline', 'Backspace', 'Backspace', 'Newline', 'A', 'Right', 'Newline', 'W', 'Right', 'Right', 'L', 'Up', 'L', 'O'
      ],
    "expected_output": "He\nallo\nworld"
  },
  {
    "input": [
        "Shift_H",  'E', 'Y', 'Space', 'L', 'O', 'R', 'D', 'Left', 'Left',
        'Left', 'Left', 'Backspace', 'Newline',  'Backspace', 'Backspace', 'Newline', 'A', 'Undo',
        'Undo', 'Right', 'Newline', 'W', 'Right', 'Right', 'L', 'Up', 'L', 'O'
    ],
    "expected_output": "Hello\nworld"
  }
]

def test_text_editor_engine():
  for test_unit in TEST_INPUTS:
    output = str(process_input_text(test_unit["input"]))
    assert output == test_unit["expected_output"], "Doesn't match the expected output"
  print("All tests passed")

test_text_editor_engine()


