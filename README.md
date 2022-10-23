# Tiny Text Editor
Create a tiny text editor using your conventional OO imperative language of choice.

The task is not to implement an interactive editor, and you should not implement any kind of UI.
Instead, make an enum representing various keystrokes, e.g. A, Shift_A, Up, Left, Backspace etc., and hard-code an array of these keystrokes in the code to process as input.
After processing the input the application can dump the resulting text lines in the console.
So, the task is to implement the "engine" inside the editor that takes keystrokes and forms the resulting text.
A visual UI could be added on top of that, to interact with this engine (instead of the enum), but that is not a part of the task.

The editor should support the following actions (all four are equally important):
- Typing text using normal characters (letters) and whitespace (space/newline).
- Moving the cursor around in the text using the four arrow keys.
- Deleting characters (including newlines) using the Backspace key.
- Undo (one key-stroke per undo, including arrow keys)

For the arrow keys, assume that we are using a fixed font, i.e. all characters have the same width.

You don't have to implement support for selecting text, e.g. Shift-Arrow-key, or copy/paste, but we would like you to structure the code to make the addition of these features fairly easy.

Please consider making an application that would perform well on larger texts, like >100.000 characters.

As an example, the following set of keystrokes:

Shift_H, E, Y, Space, L, O, R, D, Left, Left, Left, Left, Backspace, Newline, Backspace, Backspace, Newline, A, Undo, Undo, Right, Newline, W, Right, Right, L, Up, L, O

should produce the following two lines (this is a markdown file, the tripple-quotes are not part of the output, but markdown formatting of this text):

```
Hello
world
```
