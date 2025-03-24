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
        is_multi_line_comment = False
        for index_line, line in enumerate(self.text_lines):

            # Comment part handle
            if '/*' in line:
                is_multi_line_comment = True
                continue    # no '*/' in the same line

            if is_multi_line_comment and '*/' in line:
                is_multi_line_comment = False
                continue

            if '//'==line.lstrip(' \t')[:2]:        # Current line is a single line comment
                continue

            if is_multi_line_comment:
                continue


            if line.startswith('package'):
                package_name = line.split(' ')[1].strip(' ;\n')
                self.java_file.package = package_name
                continue
            elif line.startswith('import'):
                import_name = line.split(' ')[1].strip(' ;\n')
                self.java_file.imports.append(import_name)
                continue
            elif ' class ' in line:

                # get the full line
                complete_line_class = ''                # the final string that contains all the implements
                index_char = 0
                current_char = line[index_char]         # Current char
                index_line_class = index_line           # index of the current line
                while current_char!='{':
                    if current_char=='\n':                    # if end of the line, next line and start of the new line
                        index_line_class += 1
                        index_char = 0
                    current_char = self.text_lines[index_line_class][index_char]        # update current char
                    complete_line_class += current_char                                      # Add the current char to the final string
                    index_char += 1                                                      # next char
                complete_line_class = complete_line_class[:-1]

                # full class line analysis
                splited_line_class = complete_line_class.split(' ')
                for index, word in enumerate(splited_line_class):
                    word = word.strip(' \n')
                    if word=='class':
                        self.java_file.class_name = splited_line_class[index+1]
                    elif word=='extends':
                        self.java_file.extends = splited_line_class[index+1]
                    elif word=='implements':
                        
                        if 'extends' in splited_line_class[index:]:
                            index_extends = splited_line_class.index('extends')
                            implements_words_list = splited_line_class[index+1:index_extends]
                        else:
                            implements_words_list = splited_line_class[index+1:]

                        implement_words = ' '.join(implements_words_list)
                        splited_implements = implement_words.split(',')
                        splited_implements = [implement.strip(' \n\t') for implement in splited_implements]
                        
                        self.java_file.implements = splited_implements
        return self.java_file
                        

if __name__=='__main__':
    import os
    filepath = os.environ.get('EXAMPLE_JAVA_FILEPATH')
    parser = JavaParser(filepath)
    java_file = parser.parse()
    
    pprint(java_file)
