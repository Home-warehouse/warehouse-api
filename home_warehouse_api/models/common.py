import graphene


class BuildInputBoilerplate:
    '''Build InputObjectType for graphene mutations and resolvers'''
    def __init__(self, creating_new=False):
        self.name = self.__class__.__name__
        self.creating_new = creating_new
        if creating_new:
            self.name = f'Creating{self.name}'

    def BuildInput(self):
        class Input(graphene.InputObjectType):
            # TODO: Assign Meta name to self.name here instead during building input
            # class Meta:
            #     name = self.name
            #     description = ""
            pass
        return Input


class filterByType(graphene.Enum):
    '''FilterBy enum'''
    EQUAL = '$eq'
    GREATER = '$gt'
    LESSER = '$lt'

    @property
    def description(self):
        if self == filterByType.EQUAL:
            return 'Comparison returns true if its equal'
        if self == filterByType.GREATER:
            return 'Comparison returns true if its greater'
        if self == filterByType.LESSER:
            return 'Comparison returns true if its lesser'


class SortRaportInput(graphene.InputObjectType):
    custom_column = graphene.ID()
    value = graphene.String()


class FilterRaportInput(graphene.InputObjectType):
    custom_column = graphene.ID()
    comparison = graphene.InputField(filterByType)
    value = graphene.String()


product_filter_fields = {
        'show_custom_columns': graphene.List(
                    graphene.String,
                    description="List of IDs of custom columns which are present in products"
        ),
        'filter_by': graphene.Argument(graphene.List(
            FilterRaportInput), required=False),
        'sort_by': graphene.Argument(SortRaportInput),
        'limit': graphene.Int()
    }
