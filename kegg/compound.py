__author__ = 'Beibeihome'

from Modules.kegg_parse import *
from mongoengine import *
import os
import string
import re


class Compound(DynamicDocument):
    ID = IntField()
    NAME = StringField()
    NAME_KEGG = StringField()
    EXACT_MASS = FloatField()
    MOL_WEIGHT = FloatField()
    REMARK = StringField()
    REFERENCE = ListField(StringField())
    EDGE = ListField(ReferenceField(link))

    meta = {
        'collection': 'node'
    }

    def name_set(self, text):
        text = text.rstrip(string.letters + ' \n')
        self.NAME = text.lstrip()

    def normal_set(self, field, text):
        text = text.replace(' ', '')
        order = 'self.' + field + ' = text'
        exec order

    def float_set(self, field, text):
        text = text.strip()
        text = float(text)
        order = 'self.' + field + ' = text'
        exec order

    def reference_set(self, text):
        text = text.strip()
        text = ''.join([' ', text])
        text = re.split('[\s][\d][\s]', text)
        for log in text:
            log = log.strip()
        text.remove('')
        self.REFERENCE = text

    def data_save(self, dict):
        id_database = count.objects.filter(type='node')[0]
        self.ID = id_database['value']
        id_database['value'] += 1
        id_database.save()
        self.TYPE = 'Compound'
        for key in dict:
            text = dict[key]
            if key == 'ENTRY':
                self.name_set(text)
            elif key in ['EXACT_MASS', 'MOL_WEIGHT']:
                self.float_set(key, text)
            elif key == 'REFERENCE':
                self.reference_set(text)
            elif key == 'NAME':
                self.normal_set('NAME_KEGG', text)
            else:
                self.normal_set(key, text)


def main():
    BASEPATH = './kegg/compound/'
    connect('igemdata')
    #save the paths of .cvs files
    paths = []
    for filelist in os.listdir(BASEPATH):
        filepath = os.path.join(BASEPATH, filelist)
        if '.xml' in filepath:
            paths.append(filepath)

    for path in paths:
        connect('igemdata')
        fp = file(path, 'rU')
        parse_dict = kegg_split(fp)
        node = Compound()
        node.data_save(parse_dict)
        node.save()
        fp.close()
        print path + ' has saved successfully'


main()
