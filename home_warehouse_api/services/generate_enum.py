def generate_enum(enumName, enumDict):
    """Generate python enum"""
    enum_template = """
    @unique
    class {enumName}(Enum)
    {enumBody}
    """
    enumBody = '\n'.join([f"{name} = '{value}'" for (name, value) in enumDict.items()])
    return enum_template.format(enumName=enumName, enumBody=enumBody)
