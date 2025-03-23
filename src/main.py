import os

from java_parser import JavaParser
from uml_constructor import UMLConstructor

def find_files_recursive_folder(folder_path:str, file_extension:str) -> list:
    list_filepath = list()
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in [f for f in filenames if f.endswith(file_extension)]:
            filepath = dirpath.replace("\\","/") + "/" + filename
            list_filepath.append(filepath)
    return list_filepath





def main():
    project_path = 'data/java_files_exemple'
    java_filepath = find_files_recursive_folder(project_path, '.java')
    
    uml_constructor = UMLConstructor()
    for filepath in java_filepath:
        try:
            javafile = JavaParser(filepath).parse()
            uml_constructor.add_javafile(javafile, add_imports=False)
        except:
            continue
    uml = uml_constructor.get_uml()

    with open('data/output/o.txt', 'w') as f:
        f.write(uml)


if __name__=='__main__':
    main()