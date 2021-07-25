from graphene.relay import Node


class CustomNode(Node):
    '''Node object for root objects'''
    class Meta:
        name = 'CustomNode'

    @staticmethod
    def to_global_id(type, id):
        return id


class EmbeddedNode(Node):
    '''Node object for embbeded objects'''
    class Meta:
        name = 'EmbeddedNode'
