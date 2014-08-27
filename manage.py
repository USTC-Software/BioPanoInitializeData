__author__ = 'Beibeihome'
import os
from pymongo import *
from mongoengine import *
from regulondb import *
from Modules.kegg_parse import node
import CONSTANT


OVERWRITE = True
db = MongoClient()[CONSTANT.DATABASE]


def count():
    client = MongoClient()
    db = client[CONSTANT.DATABASE]
    db.drop_collection('count')
    db.count.insert({'type': 'node', 'value': 0})
    db.count.insert({'type': 'link', 'value': 0})
    db.count.insert({'type': 'product', 'value': 0})


def regulondb():
    path = './regulondb/manage.py'
    # I don't know what is {} using for,but this function can't be without it
    execfile(path, {})



def regulondb_link():
    path = './regulondb/add_ref.py'
    execfile(path, {})


def product_process():
    path = './regulondb/product.py'
    execfile(path, {})


def kegg_node(number=None):
    basepath = './kegg/'
    #paths = [basepath + 'compound.py', basepath + 'enzyme.py', basepath + 'module.py', basepath + 'protein.py']
    #kind = {'0': 'Compound', '1': 'Enzyme', '2': 'Module', '3': 'Protein'}
    paths = [basepath + 'compound.py', basepath + 'module.py', basepath + 'enzyme.py']
    kind = {'0': 'Compound', '1': 'Module', '2': 'Enzyme'}
    if number == None:
        db.drop_collection('kegg_node')
        for path in paths:
            execfile(path, {})
    else:
        db.node.remove({'TYPE': kind[str(number)]})
        execfile(paths[number], {})


def kegg_reaction():
    path = './kegg/reaction.py'
    #order = 'python ' + path
    #os.system(order)
    db.node.remove({'TYPE': 'Reaction'})
    execfile(path, {})


def kegg_reaction_function_link():
    path = './kegg/mm_parse.py'
    db = MongoClient()[CONSTANT.DATABASE]
    db.drop_collection('module__function_link')
    #order = 'python ' + path
    #os.system(order)
    execfile(path, {})


def database_link():
    path = './database_link/database_link.py'
    #order = 'python ' + path
    #os.system(order)
    execfile(path, {})


def kegg_connect():
    path = './kegg/kegg_link.py'
    execfile(path, {})


def patch1():
    path1 = './regulondb/TU_TF_link.py'
    #execfile(path1, {})
    path2 = './Sequence Analyse/UTR_importing.py'
    execfile(path2, {})


def patch2():
    db.drop_collection('node_ref')
    db.drop_collection('link_ref')
    path = './Patch/Fishing Patch.py'
    execfile(path, {})


def uniprot_update():
    path = uniprot_path = './other/uniprot.py'
    execfile(uniprot_path, {})


def log_create():
    path = './log_create.py'
    execfile(path, {})


def rebuild():
    client = MongoClient()
    db = client[CONSTANT.DATABASE]
    if OVERWRITE:
        for collection in db.collection_names():
            if collection != 'system.indexes':
                db.drop_collection(collection)
    print 'count log creating'
    count()
    print 'run regulondb importing from super manage.py'
    regulondb()
    print 'product importing '
    product_process()
    print 'run kegg_node importing from super manage.py'
    kegg_node()
    print 'run kegg_reaction importing from super manage.py'
    kegg_reaction()
    print 'run reaction connection from super manage.py'
    kegg_connect()
    print 'run reaction function sort from super manage.py'
    kegg_reaction_function_link()
    print 'run link setting between gene and enzyme from super manage.py'
    database_link()

    print 'patch 1 built in August'
    patch1()

    print 'Fishing patch built in August 22'
    #patch2()

    print 'working log creating'
    log_create()

    print 'uniprot updating'
    uniprot_update()


def main():
    rebuild()
    #patch2()
    #kegg_node(0)
    #kegg_reaction_function_link()
    #database_link()
    #patch1()
    #kegg_connect()
    #kegg_reaction()

#main()
#product_process()
log_create()