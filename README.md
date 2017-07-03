BookwormPython
================

A library for connecting to a remote Bookworm instance through Python.

There are two main classes to know about:

- `BWQuery` takes the Bookworm server URL and wraps Bookworm's JSON query format ([described in the API docs](https://bookworm-project.github.io/Docs/query_structure.html)). You can run a query with `BWQuery.run()`.
- `BWResults` is an object holding the Bookworm results, with functions that allow display of the results as `csv`, `json`, or Pandas `DataFrame`.

There is also a `set_options` class, which allows global database and endpoint setting`

## BW Query object

To start:

```python
import bwypy
```


### Intialize from JSON

```python
jsonq = '''{
   "database": "hathipd",
   "method": "return_json", 
   "search_limits": {
       "date_year": {"$gt": 1790, "$lt": 1923 }
   },
   "counttype": ["TextCount"],
   "groups": ["date_year"]
   }'''
bw = bwypy.BWQuery(json=jsonq, endpoint='https://bookworm.htrc.illinois.edu/cgi-bin/dbbindings.py')
```

```python
bw.json
```

    {'counttype': ['TextCount'],
     'database': 'hathipd',
     'groups': ['date_year'],
     'method': 'return_json',
     'search_limits': {'date_year': {'$gt': 1790, '$lt': 1923}}}

```python
bw.groups
```

    ['date_year']

```python
bw.search_limits
```

    {'date_year': {'$gt': 1790, '$lt': 1923}}


```python
bw.database
```

    'hathipd'

## Run a query

Query results are returns as a BWResults object

```python
bw.groups = ['page_count_bin', 'is_gov_doc']
bw_results = bw.run()
bw_results.json()
```

    {'L - Between 350 and 550': {'': [563222], 'No': [30973]},
     'M - Between 150 and 350': {'': [549374], 'No': [30020]},
     'S - Less than 150': {'': [466445], 'No': [25737]},
     'XL - Greater than 550': {'': [529501], 'No': [28435]},
     'unknown': {'': [1325704], 'No': [73659]}}

```python
bw_results.dataframe()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>TextCount</th>
    </tr>
    <tr>
      <th>page_count_bin</th>
      <th>is_gov_doc</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th rowspan="2" valign="top">XL - Greater than 550</th>
      <th></th>
      <td>529501</td>
    </tr>
    <tr>
      <th>No</th>
      <td>28435</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">unknown</th>
      <th></th>
      <td>1325704</td>
    </tr>
    <tr>
      <th>No</th>
      <td>73659</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">L - Between 350 and 550</th>
      <th></th>
      <td>563222</td>
    </tr>
    <tr>
      <th>No</th>
      <td>30973</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">M - Between 150 and 350</th>
      <th></th>
      <td>549374</td>
    </tr>
    <tr>
      <th>No</th>
      <td>30020</td>
    </tr>
    <tr>
      <th rowspan="2" valign="top">S - Less than 150</th>
      <th></th>
      <td>466445</td>
    </tr>
    <tr>
      <th>No</th>
      <td>25737</td>
    </tr>
  </tbody>
</table>
</div>




```python
print(bw_results.csv())
```

    page_count_bin,is_gov_doc,TextCount
    XL - Greater than 550,,529501
    XL - Greater than 550,No,28435
    unknown,,1325704
    unknown,No,73659
    L - Between 350 and 550,,563222
    L - Between 350 and 550,No,30973
    M - Between 150 and 350,,549374
    M - Between 150 and 350,No,30020
    S - Less than 150,,466445
    S - Less than 150,No,25737
    
    


```python
bw_results.tolist()
```




    [{'TextCount': 529501,
      'is_gov_doc': '',
      'page_count_bin': 'XL - Greater than 550'},
     {'TextCount': 28435,
      'is_gov_doc': 'No',
      'page_count_bin': 'XL - Greater than 550'},
     {'TextCount': 1325704, 'is_gov_doc': '', 'page_count_bin': 'unknown'},
     {'TextCount': 73659, 'is_gov_doc': 'No', 'page_count_bin': 'unknown'},
     {'TextCount': 563222,
      'is_gov_doc': '',
      'page_count_bin': 'L - Between 350 and 550'},
     {'TextCount': 30973,
      'is_gov_doc': 'No',
      'page_count_bin': 'L - Between 350 and 550'},
     {'TextCount': 549374,
      'is_gov_doc': '',
      'page_count_bin': 'M - Between 150 and 350'},
     {'TextCount': 30020,
      'is_gov_doc': 'No',
      'page_count_bin': 'M - Between 150 and 350'},
     {'TextCount': 466445,
      'is_gov_doc': '',
      'page_count_bin': 'S - Less than 150'},
     {'TextCount': 25737,
      'is_gov_doc': 'No',
      'page_count_bin': 'S - Less than 150'}]




```python
bw_results.tuples()
```




    [('XL - Greater than 550', '', 529501),
     ('XL - Greater than 550', 'No', 28435),
     ('unknown', '', 1325704),
     ('unknown', 'No', 73659),
     ('L - Between 350 and 550', '', 563222),
     ('L - Between 350 and 550', 'No', 30973),
     ('M - Between 150 and 350', '', 549374),
     ('M - Between 150 and 350', 'No', 30020),
     ('S - Less than 150', '', 466445),
     ('S - Less than 150', 'No', 25737)]



## Initialize blank BW

Rather than entering an already constructed json query, BWQuery can be used to construct from scratch.

An endpoint and database are required, at minimum.

```python
newq = bwypy.BWQuery()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    NameError: No endpoint. Provide to BWQuery on initialization or set globally.


```python
newq = bwypy.BWQuery(database='hathipd', endpoint='https://bookworm.htrc.illinois.edu/cgi-bin/dbbindings.py')
```

```python
newq.json
```

    {'compare_limits': [],
     'counttype': ['TextCount', 'WordCount'],
     'database': 'hathipd',
     'groups': [],
     'method': 'return_json',
     'search_limits': {},
     'words_collation': 'Case_Sensitive'}


```python
newq.run().dataframe()
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TextCount</th>
      <th>WordCount</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4552862</td>
      <td>7.328341e+11</td>
    </tr>
  </tbody>
</table>
</div>


```python
newq.groups
```

    []


```python
newq.groups = ['foo']
```

    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)    

    KeyError: 'The following groups are not supported in this BW: foo'



```python
newq.groups = ['publication_country']
newq.run().dataframe()
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TextCount</th>
      <th>WordCount</th>
    </tr>
    <tr>
      <th>publication_country</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>No place, unknown, or undetermined</th>
      <td>8144</td>
      <td>1.137803e+09</td>
    </tr>
    <tr>
      <th>United Kingdom Misc. Islands</th>
      <td>2</td>
      <td>4.984400e+04</td>
    </tr>
    <tr>
      <th>Australia</th>
      <td>799</td>
      <td>2.968196e+08</td>
    </tr>
    <tr>
      <th>United States</th>
      <td>1962339</td>
      <td>3.212052e+11</td>
    </tr>
    <tr>
      <th>Wales</th>
      <td>41</td>
      <td>1.241756e+07</td>
    </tr>
    <tr>
      <th>England</th>
      <td>10656</td>
      <td>1.831402e+09</td>
    </tr>
    <tr>
      <th>unknown</th>
      <td>1937740</td>
      <td>2.954869e+11</td>
    </tr>
    <tr>
      <th>Latvia</th>
      <td>64</td>
      <td>1.987412e+07</td>
    </tr>
    <tr>
      <th>Northern Ireland</th>
      <td>10</td>
      <td>2.987728e+06</td>
    </tr>
    <tr>
      <th>Scotland</th>
      <td>863</td>
      <td>1.483882e+08</td>
    </tr>
    <tr>
      <th>Soviet Socialist Republic</th>
      <td>152</td>
      <td>1.947023e+07</td>
    </tr>
    <tr>
      <th>United Kingdom</th>
      <td>536001</td>
      <td>9.987234e+10</td>
    </tr>
    <tr>
      <th>Canada</th>
      <td>78663</td>
      <td>9.747256e+09</td>
    </tr>
    <tr>
      <th>Russian S.F.S.R.</th>
      <td>3427</td>
      <td>8.390290e+08</td>
    </tr>
    <tr>
      <th>South Australia</th>
      <td>29</td>
      <td>4.146067e+06</td>
    </tr>
    <tr>
      <th>Victoria</th>
      <td>50</td>
      <td>1.064348e+07</td>
    </tr>
    <tr>
      <th>Estonia</th>
      <td>25</td>
      <td>4.242192e+06</td>
    </tr>
    <tr>
      <th>New South Wales</th>
      <td>5</td>
      <td>5.819920e+05</td>
    </tr>
    <tr>
      <th>Georgian S.S.R.</th>
      <td>0</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>Ukraine</th>
      <td>59</td>
      <td>7.314677e+06</td>
    </tr>
    <tr>
      <th>Soviet Union</th>
      <td>13784</td>
      <td>2.186202e+09</td>
    </tr>
    <tr>
      <th>Tasmania</th>
      <td>1</td>
      <td>8.426800e+04</td>
    </tr>
    <tr>
      <th>Lithuania</th>
      <td>8</td>
      <td>9.289520e+05</td>
    </tr>
  </tbody>
</table>
</div>



### Global settings

Since it's unlikely be be consistently switching databases or endpoints, these settings can be set globally with `set_options`:


```python
bwypy.set_options(endpoint='https://bookworm.htrc.illinois.edu/cgi-bin/dbbindings.py',
                        database='global')

bwypy.BWQuery(verify_fields=False).database
```

    'global'

Or in a `with` block:

```python
with bwypy.set_options(endpoint='https://bookworm.htrc.illinois.edu/cgi-bin/dbbindings.py', database='with_block'):
    bw = bwypy.BWQuery(verify_fields=False)
bw.database
```

    'with_block'

The priority for variables is:

- set with an _init_ argument
- set within the query json (for database)
- set within a `with` block with `set_options`
- set globally with `set_options`

## More BWQuery functions

Parser for `getAvailableFields`, used internally on initialization if `integrity_check=True`:

```python
bw = bwypy.BWQuery(json=jsonq, endpoint='https://bookworm.htrc.illinois.edu/cgi-bin/dbbindings.py')
bw.fields()
```

<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>anchor</th>
      <th>dbname</th>
      <th>description</th>
      <th>name</th>
      <th>tablename</th>
      <th>type</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>bookid</td>
      <td>lc_classes</td>
      <td></td>
      <td>lc_classes</td>
      <td>lc_classesLookup</td>
      <td>character</td>
    </tr>
    <tr>
      <th>1</th>
      <td>bookid</td>
      <td>lc_subclasses</td>
      <td></td>
      <td>lc_subclasses</td>
      <td>lc_subclassesLookup</td>
      <td>character</td>
    </tr>
    <tr>
      <th>2</th>
      <td>bookid</td>
      <td>fiction_nonfiction</td>
      <td></td>
      <td>fiction_nonfiction</td>
      <td>fiction_nonfictionLookup</td>
      <td>character</td>
    </tr>
    <tr>
      <th>3</th>
      <td>bookid</td>
      <td>genres</td>
      <td></td>
      <td>genres</td>
      <td>genresLookup</td>
      <td>character</td>
    </tr>
    <tr>
      <th>4</th>
      <td>bookid</td>
      <td>languages</td>
      <td></td>
      <td>languages</td>
      <td>languagesLookup</td>
      <td>character</td>
    </tr>
    <tr>
      <th>5</th>
      <td>bookid</td>
      <td>format</td>
      <td></td>
      <td>format</td>
      <td>formatLookup</td>
      <td>character</td>
    </tr>
    <tr>
      <th>6</th>
      <td>bookid</td>
      <td>is_gov_doc</td>
      <td></td>
      <td>is_gov_doc</td>
      <td>is_gov_docLookup</td>
      <td>character</td>
    </tr>
    <tr>
      <th>7</th>
      <td>bookid</td>
      <td>page_count_bin</td>
      <td></td>
      <td>page_count_bin</td>
      <td>page_count_binLookup</td>
      <td>character</td>
    </tr>
    <tr>
      <th>8</th>
      <td>bookid</td>
      <td>word_count_bin</td>
      <td></td>
      <td>word_count_bin</td>
      <td>word_count_binLookup</td>
      <td>character</td>
    </tr>
    <tr>
      <th>9</th>
      <td>bookid</td>
      <td>publication_country</td>
      <td></td>
      <td>publication_country</td>
      <td>publication_countryLookup</td>
      <td>character</td>
    </tr>
    <tr>
      <th>10</th>
      <td>bookid</td>
      <td>publication_state</td>
      <td></td>
      <td>publication_state</td>
      <td>publication_stateLookup</td>
      <td>character</td>
    </tr>
    <tr>
      <th>11</th>
      <td>bookid</td>
      <td>publication_place</td>
      <td></td>
      <td>publication_place</td>
      <td>publication_placeLookup</td>
      <td>character</td>
    </tr>
    <tr>
      <th>12</th>
      <td>bookid</td>
      <td>date_year</td>
      <td></td>
      <td>date_year</td>
      <td>fastcat</td>
      <td>integer</td>
    </tr>
  </tbody>
</table>
</div>

Return all possible values for the field.

```python
bw.field_values(field='lc_classes')
```

    ['unknown',
     'Language and Literature',
     'General and Old World History',
     'Social Sciences',
     'Science',
     'Philosophy, Psychology, and Religion',
     'Law',
     'Technology',
     'General Works',
     'History of the United States and British, Dutch, French, and Latin America',
     'Political Science',
     'Agriculture',
     'History of America',
     'Education',
     'Bibliography, Library Science, and General Information Resources',
     'Medicine',
     'Fine Arts',
     'Geography, Anthropology, and Recreation',
     'Music',
     'Auxiliary Sciences of History',
     'Military Science',
     'Naval Science']


```python
bw.field_values(field='is_gov_doc')
```

    ['', 'No']

## Testing validation

If BWQuery was initialized without turning off `verify_fields`, or if the `fields` method was run at any point, it will check queries against the known fields for that database. 

Much of the time, field validation throws an automatic error:

```python
bw = bwypy.BWQuery(json=jsonq, endpoint='https://bookworm.htrc.illinois.edu/cgi-bin/dbbindings.py')
bw.search_limits = { 'fake_field': 'whatever_value'}
```

    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    KeyError: 'The following search_limit fields are not supported in this BW: fake_field'


There are some fancy ways that you can set values where the validation isn't run. In those cases, next time validation runs, if it crashes the query is reverted to an older versions.


```python
bw.search_limits['date_year_wrong'] = 1
print("Uh oh, we got a bad field set! -- ", bw.search_limits)
try:
    bw._validate()
except:
    print("But it reverted after a failure! -- " , bw.search_limits)
```

    Uh oh, we got a bad field set! --  {'date_year': {'$lt': 1923, '$gt': 1790}, 'date_year_wrong': 1}
    But it reverted after a failure! --  {'date_year': {'$lt': 1923, '$gt': 1790}}
    

### Turning off validation

Checking allowable fields means an extra call to the database. If you know the schema already, just turn off `verify_fields`.


```python
%%time
bwypy.BWQuery(json=jsonq, endpoint='https://bookworm.htrc.illinois.edu/cgi-bin/dbbindings.py', verify_fields=False)
```

    Wall time: 0 ns

    <bwypy.core.BWQuery at 0x1fb45630358>


