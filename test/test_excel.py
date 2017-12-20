import yaml
from cerberus import Validator
import xlrd

def test_execl():
    data = xlrd.open_workbook("./test/template_student.xls")
    table = data.sheets()[0]
    for index in range(table.nrows-1):
        row_ins = table.row_values(index+1)
        name =  row_ins[0]
        codeDtype = row_ins[1]
        sex = row_ins[2]
        if sex == '男':
            sex = "mela"
        elif sex == '女':
            sex = 'famele'
        else:
             sex = 'unspecified'

        if row_ins[3] =='':
            userStatus = "active"
        else:
            userStatus = row_ins[3]



def validator():
    schema="""
a:
  type: string
a_d:
  type: dict
  schema:
    foo: 
      type: string
    bar:
      type: string
      dependencis: ^a
    """
    document= \
"""
a_d:
  foo: abc
"""
    v = Validator(yaml.load(schema))
    v.validate(yaml.load(document))
    print(v.errors)


