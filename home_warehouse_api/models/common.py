import graphene


# TODO: FIX enums to behave like string checkers
# class sortByEnum(graphene.Enum):
#     '''Sorting enum'''
#     ASCENDING = '+'
#     DESCENDING = '-'

#     @property
#     def description(self):
#         if self == sortByEnum.ASCENDING:
#             return 'Sort Ascending'
#         if self == sortByEnum.DESCENDING:
#             return 'Sort Descending'


# class filterByEnum(graphene.Enum):
#     '''FilterBy enum'''
#     EQUAL = '$eq'
#     GREATER = '$gt'
#     LESSER = '$lt'

#     @property
#     def description(self):
#         if self == filterByEnum.EQUAL:
#             return 'Comparison returns true if its equal'
#         if self == filterByEnum.GREATER:
#             return 'Comparison returns true if its greater'
#         if self == filterByEnum.LESSER:
#             return 'Comparison returns true if its lesser'

class SortRaportInput(graphene.InputObjectType):
    custom_column = graphene.ID()
    value = graphene.String()


class FilterRaportInput(graphene.InputObjectType):
    custom_column = graphene.ID()
    comparison = graphene.String()
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
