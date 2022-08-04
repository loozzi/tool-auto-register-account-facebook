import os
fileName = input('file output: ')
fileName = fileName + '.txt'
os.chdir(os.getcwd() + '\\output')

def read_text_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

data = ''

for file in os.listdir():
    # Check whether file is in text format or not
    if file.endswith(".txt"):
        file_path = f"{os.getcwd()}\\{file}"

        # call read text file function
        data += read_text_file(file_path)

with open(fileName, 'w') as f:
    f.writelines(data)

