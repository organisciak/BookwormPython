import json
import pandas as pd
import logging
import time
import urllib

class Bwypy:
    default = {"database":"", "search_limits":[], 
           "words_collation":"Case_Sensitive", "compare_limits":[], "method":"return_json",
           "counttype":["TextCount", "WordCount"], "groups":[]}
    
    def __init__(self, endpoint, db):
        self.endpoint = endpoint
        self.default['database'] = db
        self._fields = None
    
    @property
    def fields(self):
        '''
        Return Pandas object with all the fields in a Bookworm
        '''
        if self._fields is None:
            q = { 'database': self.default['database'], 
                 'method':'returnPossibleFields'}        
            obj = self._fetch(q)
            df = pd.DataFrame(obj)
            self._fields = df
        return self._fields
    
    def stats(self):
        q = self.default.copy()
        q['search_limits'] = [{"date_year":{"$lte":10000}}] #Let's hope nobody's creating a bookworm on the history of the universe
        return self.search(q)
        
    def search(self, query, coerce_dtype=True):
        logging.debug(query)
        response = self._fetch(query, type="json")[0]
        rows = self._expand(response, query['groups'], query['counttype'])
        
        '''
        # Until Pandas supports compound dtype statements, this type coercion is pointless, so using convert_objects instead.
        # Watch https://github.com/pydata/pandas/issues/4464
        if coerce_dtype:
            # Get expected datatypes from DB
            fields = bw.fields
            # Key for sql dtypes => Pandas
            fieldkey = { "integer": "int64", "character": "string" }
            counttype_dtypes = { "TextCount": "uint64", "WordCount": "uint64", "WordsPerMillion": "float32", "TextPercent": "float16" }
            db_group_dtypes = [fields[fields.dbname == groupname]['type'].iloc[0] for groupname in q['groups']]
            count_dtypes = [counttype_dtypes[fieldname] for fieldname in q['counttype']]
            dtypes = [fieldkey[db_dtype] for db_dtype in db_group_dtypes] + count_dtypes
            df = pd.DataFrame(rows, dtype    
        else:
            df = pd.DataFrame(rows)
        '''
        
        df = pd.DataFrame(rows)
        if coerce_dtype:
            ''' Copying objects. Hmmm... '''
            df = df.convert_objects(convert_numeric=True)
        
        if (len(query['groups'])) > 0:
            df.set_index(query['groups'], inplace=True)
        return df
    
    def _fetch(self, query, type="pandas"):
        ''' Get results from '''
        start = time.time()
        f = urllib.urlopen("%s?queryTerms=%s" % (self.endpoint, json.dumps(query)))
        response = json.loads(f.read())
        if type == "pandas":
            response = pd.DataFrame(response)
        elif type == "json":
            pass
        logging.debug("Query time: %ds" % (time.time()-start))
        return response
            
    def _expand(self, o, grouplist, counttypes, collector=[]):
        ''' 
        A recursive method for exploding results into rows, one line per set of facets 
        '''
        new_coll = []
        if len(grouplist) == 0:
            l = []
            for i, val in enumerate(o):
                counttype = counttypes[i]
                l += [(counttype, val)]
            return [dict(collector + l)]
        else:
            l = []
            for k, v in o.items():
                item = (grouplist[0], k)
                new_coll = collector + [item]
                l += self._expand(v, grouplist[1:], counttypes, new_coll)
            return l
