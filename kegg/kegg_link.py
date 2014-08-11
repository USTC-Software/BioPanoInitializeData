__author__ = 'Beibeihome'
from Modules.kegg_parse import *


class count(Document):
    type = StringField()
    value = IntField()


def getID(node_or_link):
    counter = count.objects.filter(type=node_or_link)[0]
    ID = counter['value']
    counter['value'] += 1
    counter.save()
    return ID


def setLink(doc1, doc2, type1, type2):
    if not type1:
        type1 = doc1.TYPE
    if not type2:
        type2 = doc2.TYPE
    link_instance = link()
    link_instance.ID = getID('link')
    link_instance.NODE1 = doc1
    link_instance.NODE2 = doc2
    link_instance.TYPE1 = type1
    link_instance.TYPE2 = type2
    link_instance.save()
    doc1.EDGE.append(link_instance.id)
    doc2.EDGE.append(link_instance.id)


def reaction_compound_linkset():
    connect('igemdata')

    #faven't been used
    reaction_counter = 0
    found_counter = 0
    missed_counter = 0
    for reaction in node.objects(TYPE='Reaction').timeout(False):
        reaction_counter += 1
        if reaction_counter % 100 == 0:
            print str(reaction_counter) + ' reactions has been analysed,and now ' + reaction.NAME + ' is on the process'
        ## reaction is a node whose TYPE is Reaction
        for reactant in reaction.REACTANTS:
            #reactant is a String Form
            reactant_node = node.objects(NAME=reactant).first()
            if not reactant_node:
                #print 'Reaction_Reactants_Connect: ' + reactant + ' in ' + reaction.NAME + ' is not found'
                missed_counter += 1

            else:
                setLink(reactant_node, reaction, 'Compound', 'Reaction')

        for product in reaction.PRODUCTS:
            #product is a String
            product_node = node.objects(NAME=product).first()
            if not product_node:
                #print 'Reaction_Product_Connect: ' + product + ' in ' + reaction.NAME + ' is not found'
                missed_counter += 1
            else:
                setLink(reaction, product_node, 'Reaction', 'Compound')

        if 'ENZYME' in reaction and reaction.ENZYME:
            #print 'Has Enzyme'
            for enzyme in reaction.ENZYME:
                enzyme_node = node.objects(NAME=enzyme).first()
                if not enzyme_node:
                    #print 'Reaction_Enzyme_Connect: ' + enzyme + ' in ' + reaction.NAME + ' is not found'
                    missed_counter += 1
                else:
                    setLink(enzyme_node, reaction, 'Enzyme', 'Reaction')

reaction_compound_linkset()