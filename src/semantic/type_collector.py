from ..cmp.ast_for_hulk import *
from ..cmp.semantic import *
from ..cmp import visitor


class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.context = Context()

        self.context.create_type('None')

        # Object Type 
        type_obj = self.context.create_type('Object')

        # Number Type        
        type_num = self.context.create_type('Number')
        type_num.set_parent(type_obj)

        type_bool = self.context.create_type('Boolean')
        type_bool.set_parent(type_obj)

        # String Type
        type_str = self.context.create_type('String')
        type_str.set_parent(type_obj)
        type_str.define_method('current', [], [], type_str)
        type_str.define_method('next', [], [], type_bool)
        type_str.define_method('size', [], [], type_num)

        # Function Type
        self.context.create_type("Function")

        # Range Type
        type_range = self.context.create_type('Range')
        type_range.set_parent(type_obj)
        type_range.define_method('current', [], [], type_num)
        type_range.define_method('next', [], [], type_bool)
        type_range.param_names = ['start', 'end']
        type_range.param_types = [type_num, type_num]
        type_range.define_attribute('start', type_num)
        type_range.define_attribute('end', type_num)
        type_range.define_attribute('current', type_num)

        # Built-In Functions
        f_print = self.context.get_type('Function').define_method('print', ['value'], [type_obj], type_str)
        f_exp = self.context.get_type('Function').define_method('exp', ['value'], [type_num], type_num)
        f_sqrt = self.context.get_type('Function').define_method('sqrt', ['value'], [type_num], type_num)
        f_log = self.context.get_type('Function').define_method('log', ['base', 'value'], [type_num, type_num],
                                                                type_num)
        f_sin = self.context.get_type('Function').define_method('sin', ['value'], [type_num], type_num)
        f_cos = self.context.get_type('Function').define_method('cos', ['value'], [type_num], type_num)
        f_rand = self.context.get_type('Function').define_method('rand', [], [], type_num)
        f_range = self.context.get_type('Function').define_method('range', ['start', 'end'], [type_num, type_num],
                                                                  type_range)

        for declaration in node.decl_list:
            self.visit(declaration)

        return self.context, self.errors

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):
        try:
            self.context.create_type(node.identifier)
        except SemanticError as ex:
            self.errors.append(ex.text)
            self.context.create_type(f'<error>{node.identifier}')
            node.identifier = f'<error>{node.identifier}'

    @visitor.when(ProtocolNode)
    def visit(self, node: ProtocolNode):
        try:
            self.context.create_type(node.identifier)
        except SemanticError as ex:
            self.errors.append(ex.text)
            self.context.create_type(f'<error>{node.identifier}')
            node.identifier = f'<error>{node.identifier}'
