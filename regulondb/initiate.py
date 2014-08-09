__author__ = 'feiyicheng'

from toolbox import *


def main():
    conn = pymongo.Connection()
    db = conn.igemdata

    db.link.remove()
    db.node.remove()

    db.product.remove()

    db.count.update({'type': 'node'}, {'type': 'node', 'value': 0})
    db.count.update({'type': 'link'}, {'type': 'link', 'value': 0})
    db.count.update({'type': 'product'}, {'type': 'product', 'value': 0})
