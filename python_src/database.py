from __future__ import print_function
import sys, sqlite3, re, os, random

# This module uses sqlite3 databases with multiple tables.
# The path to the database file is specified at the module level.
from .sqlite_files import __path__ as manifolds_paths
manifolds_path = manifolds_paths[0]
database_path = os.path.join(manifolds_path, 'plausible_knots.sqlite')

split_filling_info = re.compile(r'(.*?)((?:\([0-9 .+-]+,[0-9 .+-]+\))*$)')

def get_tables(ManifoldTable):
    """
    Functions such as this one are meant to be called in the
    __init__.py module in snappy proper.  To avoid circular imports,
    it takes as argument the class ManifoldTable from database.py in
    snappy. From there, it builds all of the Manifold tables from the
    sqlite databases manifolds.sqlite and more_manifolds.sqlite in
    manifolds_src, and returns them all as a list.
    """

    class LinkExteriorsTable(ManifoldTable):
        """
        Link exteriors usually know a DT code describing the associated link.
        """
        _select = 'select name, triangulation, DT from %s '

        def _finalize(self, M, row):
            M.set_name(row[0])
            M._set_DTcode(row[2])


    class PlausibleKnots(LinkExteriorsTable):
        """ 
        A database of knots with at most 18 crossings that are
        "plausibly slice" in that they have signature 0 and a
        normalized Alexander polynomial that factors as f(t) f(t^-1)
        as in Theorem 8.18 of [Lickorish, Intro to knot theory].
        """

        _regex = re.compile(r'[KL]*[0-9]+[anhst]+[_]*([0-9]+)$')
        
        def __init__(self, **kwargs):
            return LinkExteriorsTable.__init__(self,
                                         table='plausible_knots_view',
                                         db_path=database_path,
                                         **kwargs)

        def _configure(self, **kwargs):
            """
            Process the ManifoldTable filter arguments and then add
            the ones which are specific to links.
            """
            ManifoldTable._configure(self, **kwargs)
            conditions = []

            alt = kwargs.get('alternating', None)
            if alt == True:
                conditions.append("name like '%a%'")
            elif alt == False:
                conditions.append("name like '%n%'")
            flavor = kwargs.get('knots_vs_links', None)
            if flavor == 'knots':
                conditions.append('cusps=1')
            elif flavor == 'links':
                conditions.append('cusps>1')
            if 'crossings' in kwargs:
                N = int(kwargs['crossings'])
                conditions.append(
                    "(name like '_%da%%' or name like '_%dn%%')"%(N,N))
            if self._filter:
                if len(conditions) > 0:
                    self._filter += (' and ' + ' and '.join(conditions))
            else:
                self._filter = ' and '.join(conditions)

    return [PlausibleKnots()]


def connect_to_db(db_path):
    """
    Open the given sqlite database, ideally in read-only mode.
    """
    uri = 'file:' + db_path + '?mode=ro'
    return sqlite3.connect(uri, uri=True)


def get_DT_tables():
    """
    Returns two barebones databases for looking up DT codes by name. 
    """
    class DTCodeTable(object):
        """
        A barebones database for looking up a DT code by knot/link name.
        """
        def __init__(self, name='', table='', db_path=database_path, **filter_args):
            self._table = table
            self._select = 'select DT from ' + table + ' '
            self.name = name
            self._connection = connect_to_db(db_path)
            self._cursor = self._connection.cursor()

        def __repr__(self):
            return self.name

        def __getitem__(self, link_name):
            select_query = self._select + ' where name="{}"'.format(link_name)
            return self._cursor.execute(select_query).fetchall()[0][0]
        
        def __len__(self):
            length_query = 'select count(*) from ' + self._table
            return self._cursor.execute(length_query).fetchone()[0]


    PlausibleKnotDTcodes = DTCodeTable(name='PlausibleKnotDTcodes',
                                        table='plausible_knots_view',
                                        db_path=database_path)
    return [PlausibleKnotDTcodes]
