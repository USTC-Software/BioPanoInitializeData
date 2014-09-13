__author__ = 'Beibeihome'

from mongoengine import *
import re
import xlrd
import CONSTANT
from pymongo import *

SOURCE_PATH = './regulondb/collection/node/UTR_5_3_sequence.xlsx'
connect(CONSTANT.DATABASE)
db = MongoClient()[CONSTANT.DATABASE]


class UTR(DynamicDocument):
    OPERON_NAME = StringField()
    TU_NAME = StringField()
    PROMOTER_NAME = StringField()
    TYPE = StringField()
    SEQUENCE_5 = StringField()
    SEQUENCE_3 = StringField()


def field_fix(field):

    field[1] = 'TU_NAME'
    field[field.index("5' UTR Sequence")] = 'SEQUENCE_5'
    field[field.index("3' UTR Sequence")] = 'SEQUENCE_3'
    for i in xrange(0, len(field)):
        field[i] = field[i].upper()
        field[i] = field[i].replace("'", '_')
        field[i] = field[i].replace(' ', '_')
        #remove string in the () or []
        field[i] = field[i].split('(')[0]
        field[i] = field[i].split('[')[0]


def add_ref_utr(path):
    count = 0
    if path.endswith('xlsx'):
        data = xlrd.open_workbook(path)
        table = data.sheets()[0]
        field = table.row_values(0)
        field_fix(field)
        for i in xrange(1, table.nrows):
            group = table.row_values(i)
            log = UTR()
            for j in xrange(0, len(group)):
                exec('log.%s = group[j]' % field[j])
            log['TYPE'] = 'O_T_P'
            log.save()
            print str(count) + ' log has been saved'
            count += 1

    for gene in db.node.find({'TYPE': 'Gene'}):
        dic = {}
        if 'Gene sequence' in gene.keys():
            dic['node_id'] = gene['_id']
            dic['TYPE'] = 'Gene'
            dic['SEQUENCE'] = gene['Gene sequence']

add_ref_utr(SOURCE_PATH)

