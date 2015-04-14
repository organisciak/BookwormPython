
# coding: utf-8

# In[24]:

import json


# In[254]:

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


# In[268]:

class QueryBuilder:
    
    def __init__(self, fields):
        self.query = { "groups": [], "search_limits": []}
        for field in fields:
            if hasattr(self, field):
                print "%s conflicts with a built in attribute, renaming to %s_bw" % (field, field)
                field = field + "_bw"
            a = Field(field)
            setattr(self, field, a)
    
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
        return reduce(lambda x,y: x+y, args)
    
    def groups(self, *fields):
        self.query['groups'] = []
        for field in fields:
            self.query['groups'] += [field.name]
        return self
    
    def __repr__(self):
        return str(self.query)

q = QueryBuilder(['author_gender', 'country', "publish_year", "author_birth_country", "publisher"])
print q.search_limits(q.author_gender=="Female", q.country=="United States", q.publish_year==1890)
print q.search_limits(q.country != "Canada")
print q.search_limits((q.country == "USA") |OR| (q.author_birth_country == "USA"))
print q.search_limits(q.publisher.grep("Little,? Brown ((and|&) ?[Cc]o\.?)?"))

q = QueryBuilder(['year', 'author_party'])
reagan_bush1 = (q.year >= 1980) |AND| (q.year <= 1992)
bush2 = (q.year >= 2001) |AND| (q.year <= 2008)
clinton = (q.year >= 1993) |AND| (q.year <= 2000)
obama = (q.year >= 2009)
republican = (reagan_bush1 |OR| bush2) |AND| (q.author_party == "Republican")
democrat = (clinton |OR| obama) |AND| (q.author_party == "Democrat")
print q.search_limits(republican |OR| democrat)


# In[221]:

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


# In[107]:

q.date_year < 100 < q.date_year


# In[240]:

# Hack for custom |X| operators, via: http://code.activestate.com/recipes/384122/
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
#print json.dumps((q.date_year >= 1980) + (q.date_year <= 1990) |OR| (q.date_year > 2000) |AND| (q.languages == "English"), indent=2)


# In[276]:

fields = [u'lc_classes', u'lc_subclasses', u'fiction_nonfiction', u'genres', 
          u'languages', u'format', u'is_gov_doc', u'page_count_bin', u'word_count_bin', 
          u'publication_country', u'publication_state', u'publication_place', u'date_year']
q = QueryBuilder(fields)

hard_date_limit = (q.date_year > 1750) |AND| (q.date_year <= 1923)
q.search_limits(hard_date_limit).groups(q.publication_state)

