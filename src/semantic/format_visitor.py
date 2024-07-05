import sys
sys.path.append('/home/marian/Documents/MATCOM/Compilación/Hulk Repo/Hulk/')
from src.cmp import visitor
from src.cmp.ast_for_hulk import *


class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode'
        decl_list = '\n'.join(self.visit(declaration, tabs + 1) for declaration in node.decl_list)
        global_exp = self.visit(node.global_exp, tabs + 1)
        return f'{ans}\n{decl_list}\n{global_exp}'

    @visitor.when(FunctionNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__FunctionNode: def {node.id}(<params>) : {node.ret_type} -> <body>'
        params = '\t' * (tabs + 1) + 'params:\n' + '\n'.join(self.visit(param, tabs + 1) for param in node.params)
        if node.body:
            body = '\t' * (tabs + 1) + 'Body:\n' + self.visit(node.body, tabs + 1)
        else:
            body = '\t' * (tabs + 1) + f'Body: None'
        return f'{ans}\n{params}\n{body}'

    @visitor.when(TypeNode)
    def visit(self, node, tabs=0):
        inherits = 'None' if node.inherits is None else f": {node.inherits}"
        ans = '\t' * tabs + f'\\TypeNode: class {node.id} (<params>) inherits {inherits} (<args>)'
        params = '\t' * (tabs + 1) + 'Params:\n' + '\n'.join(self.visit(param, tabs + 1) for param in node.params)
        attr_list = '\t' * (tabs + 1) + 'Attributes:\n' + '\n'.join(
            self.visit(attr, tabs + 1) for attr in node.attr_list)
        args = '\t' * (tabs + 1) + 'Args:\n' + '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{params}\n{args}\n{attr_list}'

    @visitor.when(ProtocolNode)
    def visit(self, node, tabs=0):
        extends = 'None' if node.extends is None else f": {node.extends}"
        method_decl_col = '\t' * (tabs + 1) + 'MethodDeclCol:\n' + '\n'.join(
            self.visit(method_decl, tabs + 1) for method_decl in node.method_decl_col)
        ans = '\t' * tabs + f'\\__ProtocolNode: protocol {node.id} {extends} {node.method_decl_col}'
        return f'{ans}\n{method_decl_col}'

    @visitor.when(DeclareVarNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__DeclareVarNode: let {node.id} : {node.type_name} = <expr>'
        value = '\t' * (tabs + 1) + f'None' if node.value is None else self.visit(node.value, tabs + 1)
        return f'{ans}\n{value}'

    @visitor.when(BlockNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__BlockNode'
        statement_list = '\n'.join(self.visit(statement, tabs + 1) for statement in node.statement_list)
        return f'{ans}\n{statement_list}'

    @visitor.when(AndNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AndNode'
        left_exp = self.visit(node.left_exp, tabs + 1)
        right_exp = self.visit(node.right_exp, tabs + 1)
        return f'{ans}\n{left_exp}\n{right_exp}'

    @visitor.when(OrNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__OrNode'
        left_exp = self.visit(node.left_exp, tabs + 1)
        right_exp = self.visit(node.right_exp, tabs + 1)
        return f'{ans}\n{left_exp}\n{right_exp}'

    @visitor.when(NotNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NotNode'
        exp = self.visit(node.exp, tabs + 1)
        return f'{ans}\n{exp}'

    @visitor.when(ConcatNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ConcatNode'
        left_exp = self.visit(node.left_exp, tabs + 1)
        right_exp = self.visit(node.right_exp, tabs + 1)
        return f'{ans}\n{left_exp}\n{right_exp}'

    @visitor.when(EqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__EqualNode'
        left_exp = self.visit(node.left_exp, tabs + 1)
        right_exp = self.visit(node.right_exp, tabs + 1)
        return f'{ans}\n{left_exp}\n{right_exp}'

    @visitor.when(NotEqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NotEqualNode'
        left_exp = self.visit(node.left_exp, tabs + 1)
        right_exp = self.visit(node.right_exp, tabs + 1)
        return f'{ans}\n{left_exp}\n{right_exp}'

    @visitor.when(LessThanNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LessThanNode'
        left_exp = self.visit(node.left_exp, tabs + 1)
        right_exp = self.visit(node.right_exp, tabs + 1)
        return f'{ans}\n{left_exp}\n{right_exp}'

    @visitor.when(LessEqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LessEqualNode'
        left_exp = self.visit(node.left_exp, tabs + 1)
        right_exp = self.visit(node.right_exp, tabs + 1)
        return f'{ans}\n{left_exp}\n{right_exp}'

    @visitor.when(GreaterThanNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__GreaterThanNode'
        left_exp = self.visit(node.left_exp, tabs + 1)
        right_exp = self.visit(node.right_exp, tabs + 1)
        return f'{ans}\n{left_exp}\n{right_exp}'

    @visitor.when(GreaterEqualNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__GreaterEqualNode'
        left_exp = self.visit(node.left_exp, tabs + 1)
        right_exp = self.visit(node.right_exp, tabs + 1)
        return f'{ans}\n{left_exp}\n{right_exp}'

    @visitor.when(PlusNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PlusNode'
        left_exp = self.visit(node.left_exp, tabs + 1)
        right_exp = self.visit(node.right_exp, tabs + 1)
        return f'{ans}\n{left_exp}\n{right_exp}'

    @visitor.when(MinusNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__MinusNode'
        left_exp = self.visit(node.left_exp, tabs + 1)
        right_exp = self.visit(node.right_exp, tabs + 1)
        return f'{ans}\n{left_exp}\n{right_exp}'

    @visitor.when(ProductNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProductNode'
        left_exp = self.visit(node.left_exp, tabs + 1)
        right_exp = self.visit(node.right_exp, tabs + 1)
        return f'{ans}\n{left_exp}\n{right_exp}'

    @visitor.when(DivisionNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__DivisionNode'
        left_exp = self.visit(node.left_exp, tabs + 1)
        right_exp = self.visit(node.right_exp, tabs + 1)
        return f'{ans}\n{left_exp}\n{right_exp}'

    @visitor.when(ModNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ModNode'
        left_exp = self.visit(node.left_exp, tabs + 1)
        right_exp = self.visit(node.right_exp, tabs + 1)
        return f'{ans}\n{left_exp}\n{right_exp}'

    @visitor.when(PowNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PowNode'
        left_exp = self.visit(node.left_exp, tabs + 1)
        right_exp = self.visit(node.right_exp, tabs + 1)
        return f'{ans}\n{left_exp}\n{right_exp}'

    @visitor.when(NegativeNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NegativeNode'
        exp = self.visit(node.exp, tabs + 1)
        return f'{ans}\n{exp}'

    @visitor.when(NumberNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__NumberNode: {node.value}'

    @visitor.when(StringNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__StringNode: {node.value}'

    @visitor.when(BoolNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__BoolNode: {node.value}'

    @visitor.when(IsNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__IsNode: is {node.type_name}'
        exp = self.visit(node.exp, tabs + 1)
        return f'{ans}\n{exp}'

    @visitor.when(AsNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AsNode: as {node.type_name}'
        exp = self.visit(node.exp, tabs + 1)
        return f'{ans}\n{exp}'

    @visitor.when(VarNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__VarNode: {node.id}'

    @visitor.when(InvoqueFuncNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__InvoqueFuncNode: {node.identifier}(<args>)'
        args = '\t' * (tabs + 1) + 'Args:\n' + '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{args}'

    @visitor.when(AttrCallNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__AttrCallNode: {node.identifier} \n {self.visit(node.exp, tabs + 1)}'

    @visitor.when(PropCallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PropCallNode: \n {self.visit(node.exp, tabs + 1)}'
        function = self.visit(node.function, tabs + 1)
        return f'{ans}\n{function}'

    @visitor.when(IfNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__IfNode'
        conditions = '\n'.join(
            str(self.visit(cond[0], tabs + 1)) + '\n' + str(self.visit(cond[1], tabs + 1)) for cond in node.conditions)
        return f'{ans}\n{conditions}'

    @visitor.when(WhileNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__WhileNode'
        condition = self.visit(node.condition, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{condition}\n{body}'

    @visitor.when(ForNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ForNode'
        var = self.visit(node.var, tabs + 1)
        exp = self.visit(node.exp, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{var}\n{exp}\n{body}'

    @visitor.when(LetNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LetNode'
        var_decl = '\t' * (tabs + 1) + 'Declarations:\n' + '\n'.join(
            self.visit(decl, tabs + 1) for decl in node.var_decl)
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{var_decl}\n{body}'

    @visitor.when(AssignNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AssignNode: \n {self.visit(node.identifier, tabs + 1)}'
        exp = self.visit(node.exp, tabs + 1)
        return f'{ans}\n{exp}'

    @visitor.when(NewNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NewNode: new {node.type_name}(<args>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{args}'

    @visitor.when(IndexNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__IndexNode: \n {self.visit(node.exp, tabs + 1)}'
        index = self.visit(node.index, tabs + 1)
        return f'{ans}\n{index}'

    @visitor.when(VectorNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VectorNode: <args>'
        exp_list = '\n'.join(self.visit(exp, tabs + 1) for exp in node.exp_list)
        return f'{ans}\n{exp_list}'

    @visitor.when(VectorComprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VectorComprNode'
        exp = self.visit(node.exp, tabs + 1)
        var = self.visit(node.var, tabs + 1)
        iter_exp = self.visit(node.iter_exp, tabs + 1)
        return f'{ans}\n{var}\n{exp}\n{iter_exp}'
