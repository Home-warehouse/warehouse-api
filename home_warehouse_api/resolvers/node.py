from graphene.relay import Node

class CustomNode(Node):
    class Meta:
        name = 'CustomNode'

    @staticmethod
    def to_global_id(type, id):
        return id
