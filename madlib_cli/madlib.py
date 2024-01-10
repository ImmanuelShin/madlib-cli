import os, re
from datetime import datetime

def print_instructions():
  """
  Prints the instructions for playing the MadLibs game.
  """
  print('''
Welcome to the MadLibs game!

In this game, you'll be asked to provide various words - nouns, verbs, adjectives, etc.
These words will be used to fill in the blanks in a story, creating often humorous or whimsical results.

How to play:
1. You will be prompted to enter different types of words (like a noun, a verb, or an adjective).
2. Enter any word that fits the requested type.
3. Type 'undo' to undo your last entered word.
4. Once all words are provided, the completed story will be revealed!

Ready to have some fun? Let's get started!
  ''')

def read_template(file_path):
  """
  Reads a template file and returns its content.

  Args:
  file_path (str): The path to the template file.

  Returns:
  str: The content of the file as a string.

  Raises:
  FileNotFoundError: If the file at the specified path does not exist.
  """
  if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file '{file_path}' was not found.")
  
  with open(file_path, 'r') as file:
    return file.read()

def parse_template(string):
  """
  Extracts placeholders from a template string and returns a tuple containing the 
  template with placeholders replaced by empty braces and a tuple of extracted placeholders.

  Args:
  string (str): The template string with placeholders.

  Returns:
  tuple: A tuple containing the modified template string and a tuple of placeholders.
  """
  parts_of_speech = tuple(re.findall(r'\{([a-zA-Z]+)\}', string))
  stripped_string = re.sub(r'\{[a-zA-Z]+\}', '{}', string)
  return stripped_string, parts_of_speech

def merge(empty, list):
  """
  Fills the placeholders in the template string with the user's inputs.

  Args:
  empty (str): The template string with empty placeholders.
  list (list of str): A list of user inputs.

  Returns:
  str: The completed MadLibs story.
  """
  return empty.format(*list)

def write(madlib):
  """
  Writes the completed MadLibs story to a file with a unique timestamp in its name.

  Args:
  madlib (str): The completed MadLibs story.
  """
  timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  output_file_path = f'madlib_cli\\assets/completed_madlib_{timestamp}.txt'
  with open(output_file_path, 'w') as file:
    file.write(madlib)

def input_loop(list):
  """
  Loops through a list of parts of speech, prompting the user for inputs, and returns a list of those inputs.

  Args:
  list (list of str): A list of parts of speech.

  Returns:
  list of str: A list containing the user's inputs.
  """
  inputs = []
  i = 0

  while i < len(list):

    if inputs:
      print("\nWords you have entered so far:", ", ".join(inputs))
      print("Type 'undo' to change your last input.")

    user_input = input(f"Enter a {list[i]}: ")

    if user_input.strip() == '':
      user_input = "blank"

    if user_input.lower() == 'undo' and inputs:
      inputs.pop()
      if i != 0:
        i -=1
      continue

    inputs.append(user_input)
    i += 1

  return inputs

def main():
  """
  The main function to run the MadLibs game. It orchestrates reading the template, getting user inputs, 
  merging inputs into the template, and writing the result to a file.
  """
  print_instructions()
  try:
    template = read_template('madlib_cli\\assets\dark_and_stormy_night_template.txt')

    stripped_string, parts_of_speech = parse_template(template)

    inputs = input_loop(parts_of_speech)

    merged_madlib = merge(stripped_string, inputs)
    print("\n")
    print("Here is your completed MadLib:")
    print(merged_madlib)
    print("\n")
    write(merged_madlib)

  except FileNotFoundError as error:
    print(error)

if __name__ == "__main__":
    main()