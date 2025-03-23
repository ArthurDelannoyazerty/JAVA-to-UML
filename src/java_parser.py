from pprint import pprint
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class JavaFile:
    package:    Optional[str] = None
    imports:    list[str]     = field(default_factory=lambda: [])
    class_name: Optional[str] = None
    extends:    Optional[str] = None
    implements: list[str]     = field(default_factory=lambda: [])
    
    @property
    def class_path(self) -> str:
        return f'{self.package}.{self.class_name}'
    
    @property
    def extend_package(self) -> str:
        # If extend is imported, then its package is not from the current package
        for import_class_path in self.imports:
            if self.extends in import_class_path:
                return import_class_path
        return self.package         # else, the class_path is  the current package
    
    @property
    def extend_class_path(self) -> str:
        return f'{self.extend_package}.{self.extends}'

    @property
    def implements_class_path(self) -> list[str]:
        return [f'{self.package}.{implement}' for implement in self.implements]



class JavaParser:
    def __init__(self, filepath:str):
        with open(filepath, 'r') as f:
            self.text_lines = f.readlines()
        self.filepath = filepath
        self.java_file = JavaFile()
        # pprint(self.text_lines)
    

    def parse(self) -> JavaFile:
        for index_line, line in enumerate(self.text_lines):
            if line.startswith('package'):
                package_name = line.split(' ')[1].strip(' ;\n')
                self.java_file.package = package_name
                continue
            elif line.startswith('import'):
                import_name = line.split(' ')[1].strip(' ;\n')
                self.java_file.imports.append(import_name)
                continue
            elif ' class ' in line:
                splited_line = line.split(' ')
                for index, word in enumerate(splited_line):
                    word = word.strip(' \n')
                    if word=='class':
                        self.java_file.class_name = splited_line[index+1]
                    elif word=='extends':
                        self.java_file.extends = splited_line[index+1]
                    elif word=='implements':
                        # Init variables for the char by char loop
                        string_complete_implements = ''                                         # the final string that contains all the implements
                        current_char = ''                                                       # Current char
                        index_char_implements = line.find('implements') + len('implements')     # index of the start of the implements in the current line
                        index_line_implements = index_line                                      # index of the current line
                        while current_char!='{':
                            if index_char_implements==len(self.text_lines[index_line_implements]):          # if end of the line, next line and start of the new line
                                index_line_implements += 1
                                index_char_implements = 0
                            current_char = self.text_lines[index_line_implements][index_char_implements]    # current char
                            string_complete_implements += current_char                                      # Add the current char to the final string
                            index_char_implements += 1                                                      # next char
                        
                        # remove '{', split the implements by ',' and removed useless char ' \n\t' and store it 
                        string_complete_implements = string_complete_implements[:-1]                            
                        splited_implements = string_complete_implements.split(',')
                        splited_implements = [implement.strip(' \n\t') for implement in splited_implements]
                        
                        self.java_file.implements = splited_implements
        return self.java_file
                        

if __name__=='__main__':
    import os
    filepath = os.environ.get('EXAMPLE_JAVA_FILEPATH')
    parser = JavaParser(filepath)
    java_file = parser.parse()
    
    pprint(java_file)
