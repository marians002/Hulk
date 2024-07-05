class Context:
    def __init__(self) -> None:
        self.types = {}
        self.scope = Scope()
    
    # ----------------
    # TYPES MINI CRUD
    # ----------------

    def create_type(self, name, value):
        self.types[name] = value

    def get_type(self, name):
        if name in self.types:
            return self.types[name]
        return None   # i think this will never happen

class Scope:
    def __init__(self, parent = None):
        self.parent = parent
        self.functions = {}
        self.variables = {}
        
    # ----------------------------------
    # VARIABLE AND FUNCTIONS MINI CRUD
    # ----------------------------------
        
    # VARIABLE SECTION
    def create_variable(self, name, value):
        self.variables[name] = value

    def edit_variable(self, name, new_value):
        if name in self.variables:
            self.variables[name] = new_value
        else:
            parent = self.parent
            if parent is not None:
                parent.edit_variable(name, new_value)

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        else:
            parent = self.parent
            if parent is not None: 
                return parent.get_variable(name)

    # FUNCTION SECTION
    def create_function(self, name, value):
        # this works to define functions and redefine functions
        self.functions[name] = value

    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        else:
            if self.parent is not None:
                return self.parent.get_function(name)
        return 
    

    

