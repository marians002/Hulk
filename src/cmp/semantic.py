import itertools as itt
from collections import OrderedDict


class SemanticError(Exception):
    @property
    def text(self):
        return self.args[0]


class Attribute:
    def __init__(self, name, typex):
        self.name = name
        self.type = typex

    def __str__(self):
        return f'[attrib] {self.name} : {self.type.name};'

    def __repr__(self):
        return str(self)


class Method:
    def __init__(self, name, param_names, params_types, return_type):
        self.name = name
        self.param_names = param_names
        self.param_types = params_types
        self.return_type = return_type

    def __str__(self):
        params = ', '.join(f'{n}:{t.name}' for n, t in zip(self.param_names, self.param_types))
        return f'[method] {self.name}({params}): {self.return_type.name};'

    def __eq__(self, other):
        return other.name == self.name and \
            other.return_type == self.return_type and \
            other.param_types == self.param_types


class Protocol:
    def __init__(self, name: str, node = None):
        self.name = name
        self.node = node
        self.methods = []
        self.parent = None

    def set_parent(self, parent):
        if self.parent:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def get_method(self, name: str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            
    def define_method(self, name: str, param_names: list, param_types: list, return_type, node=None):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')
        method = Method(name, param_names, param_types, return_type, node)
        self.methods.append(method)
        return method
    
    def not_ancestor_conforms_to(self, other):
        if not isinstance(other, Protocol):
            return False
        try:
            return all(method.can_substitute_with(self.get_method(method.name)) for method in other.methods)
        # If a method is not defined in the current type (or its ancestors), then it is not conforming
        except SemanticError:
            return False

    def conforms_to(self, other):
        if other == ObjectType():
            return True
        elif isinstance(other, Type):
            return False
        return self == other or (self.parent is not None and self.parent.conforms_to(
            other)) or self._not_ancestor_conforms_to(other)

    def __str__(self):
        output = f'protocol {self.name}'
        parent = '' if self.parent is None else f' extends {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.methods else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)

class Type:
    def __init__(self, name: str):
        self.name = name
        self.attributes = []
        self.methods = []
        self.parent = None

    def set_parent(self, parent):
        if self.parent is not None:
            raise SemanticError(f'Parent type is already set for {self.name}.')
        self.parent = parent

    def get_attribute(self, name: str):
        try:
            return next(attr for attr in self.attributes if attr.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_attribute(name)
            except SemanticError:
                raise SemanticError(f'Attribute "{name}" is not defined in {self.name}.')

    def define_attribute(self, name: str, typex):
        try:
            self.get_attribute(name)
        except SemanticError:
            attribute = Attribute(name, typex)
            self.attributes.append(attribute)
            return attribute
        else:
            raise SemanticError(f'Attribute "{name}" is already defined in {self.name}.')

    def get_method(self, name: str):
        try:
            return next(method for method in self.methods if method.name == name)
        except StopIteration:
            if self.parent is None:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')
            try:
                return self.parent.get_method(name)
            except SemanticError:
                raise SemanticError(f'Method "{name}" is not defined in {self.name}.')

    def define_method(self, name: str, param_names: list, param_types: list, return_type):
        if name in (method.name for method in self.methods):
            raise SemanticError(f'Method "{name}" already defined in {self.name}')

        method = Method(name, param_names, param_types, return_type)
        self.methods.append(method)
        return method

    def all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_attributes(False)
        for attr in self.attributes:
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.all_methods(False)
        for method in self.methods:
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def conforms_to(self, other):
        return other.bypass() or self == other or self.parent is not None and self.parent.conforms_to(other)

    def bypass(self):
        return False

    def __str__(self):
        output = f'type {self.name}'
        parent = '' if self.parent is None else f' : {self.parent.name}'
        output += parent
        output += ' {'
        output += '\n\t' if self.attributes or self.methods else ''
        output += '\n\t'.join(str(x) for x in self.attributes)
        output += '\n\t' if self.attributes else ''
        output += '\n\t'.join(str(x) for x in self.methods)
        output += '\n' if self.methods else ''
        output += '}\n'
        return output

    def __repr__(self):
        return str(self)


class ErrorType(Type):
    def __init__(self):
        Type.__init__(self, '<error>')

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Type)


class VoidType(Type):
    def __init__(self):
        Type.__init__(self, '<void>')

    def conforms_to(self, other):
        raise Exception('Invalid type: void type.')

    def bypass(self):
        return True

    def __eq__(self, other):
        return isinstance(other, VoidType)


class IntType(Type):
    def __init__(self):
        Type.__init__(self, 'int')

    def __eq__(self, other):
        return other.name == self.name or isinstance(other, IntType)

class ObjectType(Type):
    def __init__(self) -> None:
        super().__init__('Object')

    def __eq__(self, other):
        return isinstance(other, ObjectType) or other.name == self.name

class IntrinsicType(Type):
    def __init__(self):
        Type.__init__(self, '<auto>')

    def __eq__(self, other):
        return isinstance(other, IntrinsicType) or other.name == self.name

    def bypass(self):
        return True

class SelfType(Type):
    def __init__(self, referred_type: Type = None) -> None:
        super().__init__('Self')
        self.referred_type = referred_type

    def get_attribute(self, name: str) -> Attribute:
        if self.referred_type:
            return self.referred_type.get_attribute(name)

        return super().get_attribute(name)

    def __eq__(self, other):
        return isinstance(other, SelfType) or other.name == self.name


#region VectorType
class VectorType(Type):
    def __init__(self, element_type):
        super().__init__('Vector')
        self.element_type = element_type

    def conforms_to(self, other):
        if isinstance(other, VectorType):
            return self.element_type.conforms_to(other.element_type)
        return super().conforms_to(other)

    def __eq__(self, other):
        return isinstance(other, VectorType) and self.element_type == other.element_type

    def __str__(self):
        return f'Vector of {self.element_type.name}'

    def __repr__(self):
        return str(self)


class Context:
    def __init__(self):
        self.types = {}
        self.functions = {}
        self.protocols = {}

    def create_type(self, name: str):
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        typex = self.types[name] = Type(name)
        return typex

    def get_type(self, name: str):
        try:
            return self.types[name]
        except KeyError:
            raise SemanticError(f'Type "{name}" is not defined.')

    def create_protocol(self, name: str, node=None):
        if name in self.protocols:
            raise SemanticError(f'Protocol with the same name ({name}) already in context.')
        if name in self.types:
            raise SemanticError(f'Type with the same name ({name}) already in context.')
        protocol = self.protocols[name] = Protocol(name, node)
        return protocol
    
    def get_protocol(self, name: str):
        try:
            return self.protocols[name]
        except KeyError:
            raise SemanticError(f'Protocol "{name}" is not defined.')
        
    def create_function(self, name: str, param_names: list, param_types: list, return_type, node = None):
        if name in self.functions:
            raise SemanticError(f'Function with the same name ({name}) already in context.')
        function = self.functions[name] = Method(name, param_names, param_types, return_type, node)
        return function
    
    def get_function(self, name: str):
        try:
            return self.functions[name]
        except KeyError:
            raise SemanticError(f'Function "{name}" is not defined.')

    def __str__(self):
        return ('{\n\t' +
                '\n\t'.join(y for x in self.types.values() for y in str(x).split('\n')) +
                '\n\t'.join(y for x in self.protocols.values() for y in str(x).split('\n')) +
                '\n\t'.join(y for x in self.functions.values() for y in str(x).split('\n')) +
                '\n}')

    def __repr__(self):
        return str(self)


class VariableInfo:
    def __init__(self, name, vtype):
        self.name = name
        self.type = vtype


class Scope:
    def __init__(self, parent=None):
        self.locals = []
        self.parent = parent
        self.children = []
        self.index = 0 if parent is None else len(parent)
        self.ret_type = IntrinsicType()

    def __len__(self):
        return len(self.locals)

    def create_child(self):
        child = Scope(self)
        self.children.append(child)
        return child

    def define_variable(self, vname, vtype):
        info = VariableInfo(vname, vtype)
        self.locals.append(info)
        return info

    def find_variable(self, vname, index=None):
        locals = self.locals if index is None else itt.islice(self.locals, index)
        try:
            return next(x for x in locals if x.name == vname)
        except StopIteration:
            return self.parent.find_variable(vname, self.index) if self.parent is None else None

    def is_defined(self, vname):
        return self.find_variable(vname) is not None

    def is_local(self, vname):
        return any(True for x in self.locals if x.name == vname)


def get_fca(types: list[Type]):
    if not types:
        return None
    if len(types) == 1:
        return types[0]

    # check ErrorType:
    if any(isinstance(item, ErrorType) for item in types):
        return ErrorType()

    # check AUTO_TYPE
    # if any(isinstance(item, AutoType) for item in types):
    #     return AutoType()

    current = types[0]
    while current:
        for item in types:
            if not item.conforms_to(current):
                break
        else:
            return current
        current = current.parent

    # This part of the code is supposed to be unreachable
    return None
