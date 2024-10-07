import os

def get_all_lines(directory):
    all_lines = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                all_lines.extend(f.readlines())
    return all_lines

directory = 'godot-docs-html-stable\\_sources'
lines = get_all_lines(directory)
print(f"Total lines collected: {len(lines)}")

lines = [line.strip() for line in lines if len(line.strip()) > 1]
print(f"Total non-empty lines collected: {len(lines)}")

lines = [line for line in lines if not line.startswith(':')]
print(f"Total lines after removing lines starting with ':': {len(lines)}")

lines = [line for line in lines if not line.startswith('==')]
print(f"Total lines after removing lines starting with '==': {len(lines)}")

lines = [line for line in lines if not line.startswith('--')]
print(f"Total lines after removing lines starting with '--': {len(lines)}")

lines = [line for line in lines if len(line) > 25]
print(f"Total lines after removing lines with less than 25 characters: {len(lines)}")

lines = [line for line in lines if len(line.split()) > 3]
print(f"Total lines after removing lines with less than 4 words: {len(lines)}")

lines = [line for line in lines if ' <' not in line or line.index(' <') > 5]
print(f"Total lines after filtering lines that don't contain ' <' or index of ' <' is greater than 5: {len(lines)}")

lines = [line.replace('.. ', '') for line in lines]
print(f"Total lines after replacing '.. ' with '': {len(lines)}")

lines = [line.replace('__', '') for line in lines]
print(f"Total lines after replacing '__' with '': {len(lines)}")

lines = [line.replace('::', ':') for line in lines]
print(f"Total lines after replacing '::' with ':': {len(lines)}")

lines = [line.replace('`_', '`') for line in lines]
print(f"Total lines after replacing '`_' with '`': {len(lines)}")

#print(lines[60:100])
print(len(lines))

with open('train-smart.txt', 'w', encoding='utf-8') as f:
    f.write('All information provided is copyright to the parties associated and listed in the text. This GPT model abides by all those copyrights and falls under them as well.\n')
    f.write('This training data is sourced from the Godot Engine documentation, which is licensed under the MIT license. The documentation is available at https://docs.godotengine.org/en/stable/index.html\n')
    f.write('Important Notice at the end of every answer: `This information is provided as is and is not guaranteed to be correct. Please refer to the official documentation for the most accurate information. The idea started as an experiment, and will hopefully be usefull to you for thoughts, ideas, and finding what you might be able to use. (edg3)`\n')
    f.write('\n'.join(lines))