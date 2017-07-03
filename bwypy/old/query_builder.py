class Field:
    def __init__(self, name):
        self.name = name

    def __eq__(self, obj):
        return FieldDict({self.name: {"$eq": obj}})

    def __ne__(self, obj):
        return FieldDict({self.name: {"$ne": obj}})

    def __gt__(self, obj):
        return FieldDict({self.name: {"$gt": obj}})

    def __ge__(self, obj):
        return FieldDict({self.name: {"$gte": obj}})

    def __lt__(self, obj):
        return FieldDict({self.name: {"$lt": obj}})

    def __le__(self, obj):
        return FieldDict({self.name: {"$lte": obj}})

    def grep(self, regex):
        return FieldDict({self.name: {"$grep": regex}})

''' Custom word class, because 'word' does not seem
to be treated consistently like other fields.
'''


class WordField(Field):
    def __init__(self):
        Field.__init__(self, 'word')

    def __eq__(self, obj):
        return FieldDict({self.name: obj})


class QueryBuilder:

    def __init__(self, fields):
        self.query = {"groups": [], "search_limits": []}
        for field in fields:
            if hasattr(self, field):
                print("%s conflicts with a built in attribute, renaming to "
                      "%s_bw" % (field, field))
                field = field + "_bw"
            a = Field(field)
            setattr(self, field, a)

        self.word = WordField()

    ''' Overload square brackets '''
    def __getitem__(self, *args):
        self.query['search_limits'] = list(args)
        return self

    def search_limits(self, *args):
        lims = self._limits(*args)
        if type(lims) is not list:
            lims = [lims]
        self.query['search_limits'] = lims
        return self

    def compare_limits(self, *args):
        lims = self._limits(args)
        self.query['compare_limits'] = lims
        return self

    def _limits(self, *args):
        # Merge all the individual FieldDicts
        merged = args[0]
        for arg in args[1:]:
            merged += arg
        return merged

    def groups(self, *fields):
        self.query['groups'] = []
        for field in fields:
            self.query['groups'] += [field.name]
        return self

    def __repr__(self):
        return str(self.query)


class FieldDict(dict):
    def __add__(self, obj):
        newdict = FieldDict()
        all_keys = set(self.keys() + obj.keys())
        for key in all_keys:
            newdict[key] = []
            if key in self:
                if type(self[key]) is not list:
                    newdict[key] += [self[key]]
                else:
                    newdict[key] += self[key]
            if key in obj:
                if type(obj[key]) is not list:
                    newdict[key] += [obj[key]]
                else:
                    newdict[key] += obj[key]
        return newdict


# Hack for custom |X| operators, via:
# http://code.activestate.com/recipes/384122/
class Infix:
    def __init__(self, function):
        self.function = function

    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __or__(self, other):
        return self.function(other)

    def __rlshift__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))

    def __rshift__(self, other):
        return self.function(other)

    def __call__(self, value1, value2):
        return self.function(value1, value2)


def _and(x,y):
    return FieldDict({ "$and" : [x, y]})

AND = Infix(_and)

OR = Infix(lambda x,y: FieldDict({ "$or" : [x, y]}) )
