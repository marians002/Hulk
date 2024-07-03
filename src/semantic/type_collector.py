from ..cmp.ast_for_hulk import *
from ..cmp.semantic import *
from ..cmp.visitor import visitor

class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()

        self.context.create_type('None')
        self.context.create_type('<void>')      
        # self.context.types['void'] = VoidType()
        # self.context.types['error'] = ErrorType()


        # Object Type (creation only)
        type_obj = self.context.create_type('obj')

        # Number Type        
        type_num = self.context.create_type('num')
        type_num.set_parent(type_obj)

        type_bool = self.context.create_type('bool')
        type_bool.set_parent(type_obj)

        # String Type
        type_str = self.context.create_type('str')
        type_str.set_parent(type_obj)
        type_str.define_method('current', [], [], type_str)
        type_str.define_method('next', [], [], type_bool)
        type_str.define_method('len', [], [], type_num)

        # Object Type (methods definition)
        type_obj.define_method('equals', ['other'], [type_obj], type_bool)
        type_obj.define_method('toString', [], [], type_str)

        # Function Type
        self.context.create_type("Function")

        # Built-In Functions
        f_print = self.context.get_type('Function').define_method('print', ['value'], [type_obj], type_str)
        f_exp = self.context.get_type('Function').define_method('exp', ['base', 'exponent'], [type_num, type_num], type_num)
        f_sqrt = self.context.get_type('Function').define_method('sqrt', ['value'], [type_num], type_num)
        f_log = self.context.get_type('Function').define_method('log', ['base', 'value'], [type_num, type_num], type_num)
        f_sin = self.context.get_type('Function').define_method('sin', ['value'], [type_num], type_num)
        f_cos = self.context.get_type('Function').define_method('cos', ['value'], [type_num], type_num)
        f_rand = self.context.get_type('Function').define_method('rand', [], [], type_num)


        for declaration in node.decl_list:
            self.visit(declaration)

        return self.context, self.errors
        
    # Your code here!!!
    # wtf
    # @visitor.when(ClassDeclarationNode)
    # def visit(self, node):
    #     try:
    #         self.context.create_type(node.id)   
    #     except SemanticError as ex:
    #         self.errors.append(ex.text)