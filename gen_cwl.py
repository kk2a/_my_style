import re

def extract_commands(file_path):
    commands = []
    environments = []
    theorems = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # \newcommand
            match = re.match(r'\\newcommand\{\\(\w+)\}\[?(\d*)\]?\{', line)
            if match:
                command = match.group(1)
                num_args = match.group(2)
                if num_args:
                    args = ''.join([f'{{arg{i+1}}}' for i in range(int(num_args))])
                else:
                    args = ''
                commands.append(f'\\{command}{args}')
            
            # \newenvironment
            match = re.match(r'\\newenvironment\{(\w+)\}', line)
            if match:
                environment = match.group(1)
                environments.append(f'\\begin{{{environment}}}\n\\end{{{environment}}}')
            
            # \newtheorem
            match = re.match(r'\\newtheorem\{(\w+)\}', line)
            if match:
                theorem = match.group(1)
                theorems.append(f'\\begin{{{theorem}}}\n\\end{{{theorem}}}')
            
            # \NewDocumentEnvironment
            match = re.match(r'\\NewDocumentEnvironment\{(\w+)\}', line)
            if match:
                environment = match.group(1)
                environments.append(f'\\begin{{{environment}}}\n\\end{{{environment}}}')
    
    return commands, environments, theorems

def write_cwl(commands, environments, theorems, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        for command in commands:
            file.write(command + '\n')
        for environment in environments:
            file.write(environment + '\n')
        for theorem in theorems:
            file.write(theorem + '\n')

if __name__ == "__main__":
    sty_file_path = '_my_style.sty'
    cwl_file_path = '_my_style.cwl'
    
    commands, environments, theorems = extract_commands(sty_file_path)
    write_cwl(commands, environments, theorems, cwl_file_path)
    print(f"Generated {cwl_file_path} from {sty_file_path}")