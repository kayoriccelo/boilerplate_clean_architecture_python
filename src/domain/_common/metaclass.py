
class EntityMetaclass(type):
    def __init__(cls, name, bases, dictionary):
        super(EntityMetaclass, cls).__init__(name, bases, dictionary)

        for key, attribute in dictionary.items():
            if hasattr(attribute, 'set_name'):
                attribute.set_name(f'__{name}', key)
