"""Contain all the basic objects useful for the manipulation of relationnal algrebra"""
#TO DO : Revoir la structure
class Expr():
    def __init__(self, relation):
        this.relation = relation

class Rel():
    pass

class Operation():
    def __init__(self, left_member, right_member):
        self.left_member = left_member
        self.right_member = right_member

class Eq(Operation):
    def __init__(self, left_member, right_member):
        super.__init__(self, left_member, right_member)


class Cst():
    def __init__(self, value):
        self.value = value 

class Table():
    pass

