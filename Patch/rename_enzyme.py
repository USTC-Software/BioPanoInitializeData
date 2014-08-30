__author__ = 'Beibeihome'

from pymongo import *
import CONSTANT

## 2014/8/28
## This Patch change attribute in kegg database that NAME to ENTRY, NAME_KEGG to NAME
## After Patch, Version = 1.1.1.0

db = MongoClient()[CONSTANT.DATABASE]
log_path = './log/rename_enzyme.txt'
enzyme_log = './log/edited_enzyme_log.txt'

## 1 step: rename kegg data directly
db.node.update({'$or': [{'TYPE':'Compound'}, {'TYPE':'Enzyme'}]}, {'$rename': {'NAME': 'ENTRY'}}, multi=True)
db.node.update({'$or': [{'TYPE':'Compound'}, {'TYPE':'Enzyme'}]}, {'$rename': {'NAME_KEGG': 'NAME'}}, multi=True)

## 2 step: establish gene:enzyme table
gene_exist_table = {}
multi_gene = []
for enzyme in db.node.find({'TYPE': 'Enzyme'}):
    for gene in enzyme['GENES']:
        if gene not in gene_exist_table.keys():
            gene_exist_table[gene] = [enzyme['_id'], ]
            #gene_exist_table[gene] = [enzyme['NAME'], ]
        else:
            gene_exist_table[gene].append(enzyme['_id'])
            #gene_exist_table[gene].append(enzyme['NAME'])
            multi_gene.append(gene)
print 'gene_exist_table has been built'

## 3 step: search uniprot reference table to find taget gene and edit its enzyme name
edited_count = 0
edited_id_list = []
for gene_name in gene_exist_table.keys():
    gene_name = gene_name.replace('-', '').split('_')[0]   #genename uniprotize
    gene_uniprot = db.uniprot.find_one({'gene_name': gene_name})
    if gene_uniprot is not None:
        protein_name = gene_uniprot['protein_name']
        for enzyme_id in gene_exist_table[gene_name]:
            # log enzyme id of enzyme edited
            if enzyme_id not in edited_id_list:
                edited_id_list.append(enzyme_id)
            db.node.update({'_id': enzyme_id}, {'$set': {'NAME': protein_name}})
            edited_count += 1

## 4 step: create log
fp_enzyme_edited = open(enzyme_log, 'w')
log_file = open(log_path, 'w')

log_file.write('with multi enzyme genes\n')
log_file.write(str(multi_gene) + '\n')

log_file.write('details\n')
log_file.write(str(gene_exist_table))

log_file.write('edited enzyme count: ' + str(edited_count) + '\n')
log_file.write('edited enzyme list: \n' + str(edited_id_list) + '\n')
fp_enzyme_edited.write(str(edited_id_list))

log_file.close()
fp_enzyme_edited.close()

## 5 step: create enzyme log which has not been edited
log_enzyme_unedited_path = './log/enzyme_unedited.txt'
fp_unedited = open(log_enzyme_unedited_path, 'w')

enzyme_dict = {}
for enzyme in db.node.find({'TYPE': 'Enzyme'}):
    if enzyme['_id'] not in edited_id_list:
        enzyme_dict[enzyme['ENTRY']] = [enzyme['NAME'],enzyme['GENES']]

fp_unedited.write(str(enzyme_dict))
fp_unedited.close()