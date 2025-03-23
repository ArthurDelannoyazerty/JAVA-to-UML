from dataclasses import dataclass
from enum import StrEnum
from java_parser import JavaFile

from typing_extensions import Self

class UMLConstructor:
    class ClassRelation(StrEnum):
        EXTEND    = '<|--' 
        IMPLEMENT = '<|..'

    
    def __init__(self):
        self.packages:dict[list]    = dict()        # {"package1": [class1, class2], "package2": [class1, class2]}
        self.implements:list[tuple] = list()        # [(class_path1, class_path2), ...]    
        self.extends:list[tuple]    = list()        # [(class_path1, class_path2), ...]    
        self.imports:list           = list()        # [class_path1, class_path2, ...]

    def add_javafile(self, javafile:JavaFile, add_imports:bool=False) -> Self:
        self.add_package(javafile.package, javafile.class_name)
        self.add_extend(javafile)
        self.add_implements(javafile)
        if add_imports: self.add_imports(javafile)
        return self


    def add_package(self, package:str, class_name:str) -> None:
        if package not in self.packages:
            self.packages[package] = list()
        self.packages[package].append(class_name)
    

    def add_extend(self, javafile:JavaFile) -> None:
        self.add_package(javafile.extend_package, javafile.extends)
        self.extends.append((javafile.class_path, javafile.extend_class_path))

    def add_implements(self, javafile:JavaFile) -> None:
        for implement_class_path in javafile.implements_class_path:
            self.implements.append((javafile.class_path, implement_class_path))

    def add_imports(self, javafile:JavaFile) -> None:
        self.imports.extend(javafile.imports)


    def get_uml(self) -> str:
        uml = '@startuml\n\n'
        
        for package, class_name_list in self.packages.items():
            uml +=f'package {package} {{'
            for class_name in class_name_list :
                uml += f'\n\tclass {class_name}'
            uml += '\n}\n\n'
        
        uml += '\n\n\'EXTENDS'
        for extend_source, extend_destination in self.extends:
            uml += f'\n{extend_source}  {UMLConstructor.ClassRelation.EXTEND}  {extend_destination}'

        uml += '\n\n\'IMPLEMENTS'
        for implement_source, implement_destination in self.implements:
            uml += f'\n{implement_source}  {UMLConstructor.ClassRelation.IMPLEMENT}  {implement_destination}'
        
        uml += '\n\n\'IMPORTS'
        for imports in self.imports:
            uml += f'\nclass {imports}'

        uml += '\n\n@enduml'
        return uml
    


if __name__=='__main__':
    javafile = JavaFile(package='esa.esoc.ops.osc.must.dataaccess', 
                        imports=['java.sql.ResultSet', 'java.sql.SQLException', 
                                'java.text.SimpleDateFormat', 'java.util.LinkedList', 
                                'esa.esoc.ops.osc.dataaccess.MustException', 
                                'esa.esoc.ops.osc.utils.time.TimeUtils'], 
                        class_name='MUSTParamTimeRecordsImpl', 
                        extends='MUSTParamRecordsImpl', 
                        implements=['MUSTParamTimeRecords'])
    print(javafile)

    uml_constructor = UMLConstructor()
    uml_constructor.add_javafile(javafile, add_imports=True)
    uml = uml_constructor.get_uml()
    print(uml)

    with open('data/output/o.txt', 'w') as f:
        f.write(uml)