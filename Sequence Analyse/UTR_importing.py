__author__ = 'Beibeihome'

from mongoengine import *
import re
import xlrd
import CONSTANT

SOURCE_PATH = './regulondb/collection/node/UTR_5_3_sequence.xlsx'
connect(CONSTANT.DATABASE)


class UTR(DynamicDocument):
    OPERON_NAME = StringField()
    TU_NAME = StringField()
    PROMOTER_NAME = StringField()
    SEQUENCE_5 = StringField()
    SEQUENCE_3 = StringField()


def field_fix(field):

    field[1] = 'TU_NAME'
    field[field.index("5' UTR Sequence")] = 'SEQUENCE_5'
    field[field.index("3' UTR Sequence")] = 'SEQUENCE_3'
    for i in xrange(0 , len(field)):
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
            log.save()
            print str(count) + ' log has been saved'
            count += 1

add_ref_utr(SOURCE_PATH)

