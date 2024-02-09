#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from decimal import Decimal
from datetime import date
import sys
import pathlib
import sqlite3
from collections import namedtuple, OrderedDict
# import utils

from rich.console import Console
console = Console()


class Display:
    def __init__(self, desc: list, rows: list):
        """
        Display result as:
        :desc: [desc[0] for desc in curs.description]
        :rows: curs.fetchall()
        (table | vertical | list of namedtuple object | list of dicts | list of an OrderedDict
        """
        self.desc = desc
        self.rows = rows

    @property
    def as_orderedDict(self):
        """
        Return a list of OrderedDict
        >>> db_handler.make_query(query, display=True).as_orderedDict
        """
        rowdicts = [OrderedDict(zip(self.desc, row)) for row in self.rows]
        return rowdicts

    @property
    def as_namedtuple(self):
        """
        Return a list of OrderedDict
        >>> db_handler.make_query(query, display=True).as_namedtuple
        """
        for ind, value in enumerate(self.desc):
            # namedtuple take this form: Parts = namedtuple('Parts', 'id_num desc cost amount')
            # find white space on fields_name and change it to '_' chars
            index = value.find(' ')     # index of white space inside value; find return the index
            if index > 0:
                self.desc[ind] = value.replace(' ', '_')
        Row = namedtuple('Row', self.desc)               # getting the key from description
        rows = [Row(*r) for r in self.rows]              # getting values
        return rows

    @property
    def richtable_display(self):
        """
        Display result of query in terminal with rich.table
        """
        from rich.table import Table
        table = Table(header_style='bold magenta')
        for desc in self.desc: table.add_column(desc)
        for row in self.rows:
            row = map(str, row)
            table.add_row(*row)
        console.print(table)
        console.print('\[[#17a2b8]Counts[/]]: {} Rows'.format(len(self.rows)), style='bold')


class SqliteFunc:
    def __init__(self, db_name):
        self.db_name = db_name
        if pathlib.Path(db_name).is_file() and pathlib.Path(db_name).exists():
            pass
        else:
            utils.logger.error(f'DB with name {db_name} does not exist.')
            utils.logger.info('Creating database and tables.')
            self.create_tables()

    def login(self):
        """
        login to database; if database does not exist; than create it
        """
        try:
            conn = sqlite3.connect(self.db_name)
        except sqlite3.Error as err:
            exc_type, exc_object, exc_traceback = sys.exc_info()
            exc_lineno = exc_traceback.tb_lineno
            utils.logger.error(f'{exc_lineno} :: {err}')
        else:
            conn.execute('PRAGMA foreign_keys = 1')
            curs = conn.cursor()
            return conn, curs

    def make_query(self, query: str, params=(), display: bool = False):
        """
        CRUD Function
        if select return tuple(desc, rows)
        else update or delete; return rowcount of affected rows

        :query: like select * from table name
        :params: query params
        :display: return display instance

        >>> make_query('select * from table_name where id = ?', [1])
        """
        conn, curs = self.login()
        try:
            curs.execute(query, params)
        except sqlite3.Error as err:
            exc_type, exc_object, exc_traceback = sys.exc_info()
            exc_lineno = exc_traceback.tb_lineno
            utils.logger.error(f'{exc_lineno} :: {err}')
            return err
        else:
            stmt = query.split()[0].upper()
            if stmt == 'SELECT':
                desc = [desc[0] for desc in curs.description]
                rows = curs.fetchall()
                if display:
                    return self.display(desc, rows)
                else:
                    return (desc, rows)
            else:
                conn.commit()
                return curs.rowcount
        finally:
            if conn: conn.close()

    # =====: Global Methods :===== #
    def create_tables(self):
        """This function will create all table"""
        # base_clients table
        tables = {
            'base_clients': [
                'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
                'added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
                'name VARCHAR(255) NOT NULL UNIQUE',
                'address VARCHAR(255) NOT NULL',
                'phone VARCHAR(255) NOT NULL UNIQUE',
                'nif VARCHAR(255) NOT NULL UNIQUE',
                'nis VARCHAR(255) NOT NULL UNIQUE',
                'ai VARCHAR(255) NOT NULL UNIQUE',
                'n_registre VARCHAR(255) NOT NULL UNIQUE',
            ],
            # ===========================================================
            'base_products': [
                'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
                'name VARCHAR(255)',
                'ref VARCHAR(255) NOT NULL UNIQUE',
                'qte INTEGER UNSIGNED NOT NULL',
                'prix_achat VARCHAR(255) NOT NULL',
                'prix_detail VARCHAR(255) NOT NULL',
                'prix_gros VARCHAR(255)',
                'prix_supergros VARCHAR(255)',
            ],
            # ===========================================================
            'base_facture': [
                'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
                'fact_date DATE',
                'fact_number VARCHAR(255) NOT NULL',
                'client_id INTEGER NOT NULL',
                'total VARCHAR(255)',
                'tva VARCHAR(255)',
                'total_ttc VARCHAR(255)',
                'payment VARCHAR(255)',
                'remains VARCHAR(255)',
                'paid_date DATE',
                'fact_type VARCHAR(50)',
                'CONSTRAINT fk_client_id FOREIGN KEY (client_id) REFERENCES base_clients(id) ON DELETE CASCADE'
            ],
            'base_facturedetails': [
                'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
                'fact_id INTEGER NOT NULL',
                'fact_number VARCHAR(255) NOT NULL',
                'product_id INTEGER NOT NULL',
                'qte INTEGER UNSIGNED',
                'price VARCHAR(255)',
                'total VARCHAR(255)',
                'CONSTRAINT fk_fact_id FOREIGN KEY(fact_id) REFERENCES base_facture(id) ON DELETE CASCADE',
            ],
            'base_versement': [
                'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
                'vers_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
                'client_id INTEGER NOT NULL',
                'payment VARCHAR(255)',
                'CONSTRAINT fk_client_vers_id FOREIGN KEY(client_id) REFERENCES base_clients(id) ON DELETE CASCADE'
            ]
        }
        for table_name, fields in tables.items():
            result = self.create_table(table_name, fields)
            print(f'Result for creating table {table_name} :: {result}')

    def create_table(self, table_name: str, fields: list):
        """
        usage : create_tables('table_name', ['id INTEGER', 'add_date DATETIME'])
        return: result from sqlite3
        """
        query = 'CREATE TABLE {}(\n{}\n)'.format(table_name, ',\n'.join(fields))
        return self.make_query(query)

    def create_index(self, index_name, table_name, field):
        """
        create_index('idx_code_article', 'table_name', 'id')
        return the result from sqlite3
        """
        query = 'CREATE INDEX {} ON {}({})'.format(index_name, table_name, field)
        return self.make_query(query)

    def get_id(self, column, table_name, value):
        """
        return the id
        SELECT id FROM {table_name} WHERE {id | name | desig} = {value}
        :column    : column to get data with id, number, client_id
        :table_name: table name
        :value     : value to search by
        """
        query = 'SELECT id FROM {} WHERE {} = ?'.format(table_name, column)
        desc, result = self.make_query(query, [value])
        return result[0][0]

    def dump_records(self, fields: list, table_name: str):
        # records = Products.objects.values_list(*fields)
        # conver the records to a list of tuples
        # rows = list(records)
        query = f'SELECT {", ".join(fields)} FROM {table_name}'
        _, rows = self.make_query(query)
        return rows

    def stringify(self, number: Decimal) -> str:
        return str(number)

    def display(self, desc, rows):
        """This will return a display instance"""
        display_inst = Display(desc, rows)
        return display_inst

    def count_table(self, table_name: str) -> int:
        query = f'SELECT COUNT(id) FROM {table_name}'
        _, result = self.make_query(query)
        return result[0][0]

    def delete_item(self, table_name: str, item_id):
        """Delete item FROM table_name where id = item_id"""
        query = 'DELETE FROM {} WHERE id = ?'.format(table_name)
        result = self.make_query(query, [item_id])
        return result

    # =====: Clients Methods :===== #
    def new_client(self, name, address, phone, nif, nis, ai, n_register):
        query = 'INSERT INTO base_clients(name, address, phone, nif, nis, ai, n_registre) VALUES(?, ?, ?, ?, ?, ?, ?)'
        params = [name, address, phone, nif, nis, ai, n_register]
        result = self.make_query(query, params)
        return result

    def search(self, fields, table_name, by, value):
        """
        Search in database
        :fields: fields to retrieve from database
        :table_name: the table name
        :by: column to search by (id, name, ...)
        :value: value to search for
        """
        value = f'%{value}%'
        query = f'SELECT {", ".join(fields)} FROM {table_name } WHERE {by} LIKE ?'
        params = [value]
        _, rows = self.make_query(query, params)
        return rows

    def get_clients_name(self, client_id=None) -> list:
        """
        Get all client names from Clients Table
        :client_id: return the client name for the given client_id
        """
        if client_id:
            query = 'SELECT name FROM base_clients WHERE id = ?'
            params = [client_id]
            _, rows = self.make_query(query, params)
            return rows[0][0]
        else:
            query = 'SELECT name FROM base_clients'
            _, rows = self.make_query(query)
            client_names = [row[0] for row in rows]
            return client_names

    def get_client_address(self, client_name: str):
        """Return client address"""
        query = 'SELECT address FROM base_clients WHERE name = ?'
        _, address = self.make_query(query, [client_name])
        return address[0][0]

    def get_client_details(self, client_id: str):
        """Get all Client Details"""
        query = 'SELECT * FROM base_clients WHERE id = ?'
        client = self.make_query(query, [client_id], display=True).as_namedtuple
        return client[0]

    def get_client_credits(self, client_id: str):
        """Get all Client Credits"""
        query = 'SELECT SUM(remains) FROM base_facture WHERE client_id = ?'
        _, result = self.make_query(query, [client_id])
        return result[0][0]

    def update_client(self, params: list):
        query = 'UPDATE base_clients SET name = ?, address = ?, phone = ?, nif = ?, nis = ?, ai = ?, n_registre = ? WHERE id = ?'
        result = self.make_query(query, params)
        return result

    # =====: Products Methods :===== #
    def new_product(self, name, ref, qte, prix_achat, prix_detail, prix_gros, prix_supergros):
        query = '''INSERT INTO base_products(name, ref, qte, prix_achat, prix_detail, prix_gros, prix_supergros)
                   VALUES(?, ?, ?, ?, ?, ?, ?)'''
        params = [name, ref, qte, prix_achat, prix_detail, prix_gros, prix_supergros]
        result = self.make_query(query, params)
        return result

    def product_details(self, prod_id):
        """Get all fields FROM base_products table for a given product_id"""
        query = 'SELECT * FROM base_products WHERE id = ?'
        params = [prod_id]
        result = self.make_query(query, params, display=True).as_namedtuple
        return result[0]

    def update_product(self, params: list):
        query = '''UPDATE base_products SET name = ?, ref = ?, qte = ?, prix_achat = ?, prix_detail = ?,
                   prix_gros = ?, prix_supergros = ? WHERE id = ?'''
        result = self.make_query(query, params)
        return result

    # =====: Factures Methods :===== #
    def dump_factures(self, fact_type):
        """Dump all factures by type"""
        query = '''SELECT f.id, f.fact_date, f.fact_number, f.fact_type, c.name, f.total, f.tva, f.total_ttc,
                   f.payment, f.remains, f.paid_date
                   FROM base_facture AS f LEFT JOIN base_clients as c ON f.client_id == c.id
                   WHERE fact_type = ?'''
        _, rows = self.make_query(query, [fact_type])
        return rows

    def search_factures(self, by, value):
        """
        Search for facutres
        TODO: add fact_type to the search if needed
        """
        value = f'%{value}%'
        query = f'''SELECT f.id, f.fact_date, f.fact_number, f.fact_type, c.name, f.total, f.tva, f.total_ttc,
                   f.payment, f.remains, f.paid_date
                   FROM base_facture AS f LEFT JOIN base_clients as c ON f.client_id == c.id
                   WHERE {by} LIKE ?'''
        _, rows = self.make_query(query, [value])
        return rows

    def facture_by_client(self, client_id):
        """Return all the facture for the given client_id"""
        query = '''SELECT f.id, f.fact_date, f.fact_number, f.fact_type, c.name, f.total, f.tva, f.total_ttc,
                   f.payment, f.remains, f.paid_date
                   FROM base_facture AS f LEFT JOIN base_clients as c ON f.client_id == c.id
                   WHERE f.client_id = ?'''
        _, rows = self.make_query(query, [client_id])
        return rows

    def get_fact_number(self, fact_type):
        """
        return the last fact number to add to the next facture
        :fact_type: each type has his own number
        """
        query = 'SELECT MAX(fact_number) FROM base_facture WHERE fact_type = ?'
        _, result = self.make_query(query, [fact_type])
        fact_number = result[0][0]
        if not fact_number:
            return 0
        return fact_number

    def save_proforma(self, fact_date, fact_num, client_name, cart, tva: int, total_ttc: Decimal):
        """
        Save New Facture Proforma
        This function will save the facture without updating stocks
        """
        conn, curs = self.login()
        client_id = self.get_id('name', 'base_clients', client_name)
        total_price = cart.get_total_price()
        inv_query = '''INSERT INTO base_facture(fact_number, fact_date, client_id, total, tva, total_ttc, payment, remains, fact_type)
                       VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        params = [fact_num, fact_date, client_id, self.stringify(total_price), self.stringify(tva),
                  self.stringify(total_ttc), 0, 0, 'facture proforma']
        try:
            curs.execute(inv_query, params)
            fact_id = curs.lastrowid
            products = [prod for prod in cart]
            for product in products:
                prod_id, _, qte, price, total = product
                # insert invoice details
                query = 'INSERT INTO base_facturedetails(fact_id, fact_number, product_id, qte, price, total) VALUES(?, ?, ?, ?, ?, ?)'
                curs.execute(query, [fact_id, fact_num, prod_id, qte, self.stringify(price), self.stringify(total)])
        except sqlite3.Error as err:
            exc_type, exc_object, exc_traceback = sys.exc_info()
            exc_lineno = exc_traceback.tb_lineno
            utils.logger.error(f'Insert new Proforma: {exc_lineno} :: {err}')
            return False
        else:
            conn.commit()
            return True
        finally:
            if conn: conn.close()

    def save_invoice(self, fact_date, fact_num, client_name, cart, tva: Decimal, total_ttc: Decimal, versement: Decimal,
                     fact_type: str):
        """Save New Facture OR Bon de livraison"""
        conn, curs = self.login()

        client_id = self.get_id('name', 'base_clients', client_name)
        total_price = cart.get_total_price()
        remains = total_ttc - versement
        if remains <= 0:   # means facture paid
            paid_date = fact_date
        else:
            paid_date = ''

        inv_query = '''INSERT INTO base_facture(
                       fact_number, fact_date, client_id, total, tva, total_ttc, payment, remains, paid_date, fact_type)
                       VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        params = [fact_num, fact_date, client_id, self.stringify(total_price), self.stringify(tva),
                  self.stringify(total_ttc), self.stringify(versement), self.stringify(remains), paid_date, fact_type]
        try:
            curs.execute(inv_query, params)
            fact_id = curs.lastrowid

            # insert in versement to keep track of first fact versement
            query = 'INSERT INTO base_versement(vers_date, payment, client_id) VALUES(?, ?, ?)'
            curs.execute(query, [fact_date, self.stringify(versement), client_id])

            products = [prod for prod in cart]
            # INSERT into FacturesDetails
            for product in products:
                prod_id, _, qte, price, total = product
                # UPDATE The Main QTE
                curs.execute('SELECT qte FROM base_products WHERE id = ?', [prod_id])
                db_qte = curs.fetchone()[0]
                new_qte = db_qte - qte                  # update qte
                params = [new_qte, prod_id]
                curs.execute('UPDATE base_products SET qte = ? WHERE id = ?', params)

                # insert invoice details
                query = 'INSERT INTO base_facturedetails(fact_id, fact_number, product_id, qte, price, total) VALUES(?, ?, ?, ?, ?, ?)'
                curs.execute(query, [fact_id, fact_num, prod_id, qte, self.stringify(price), self.stringify(total)])

        except sqlite3.Error as err:
            exc_type, exc_object, exc_traceback = sys.exc_info()
            exc_lineno = exc_traceback.tb_lineno
            utils.logger.error(f'Insert new facture: {exc_lineno} :: {err}')
            return False
        else:
            conn.commit()
            return True
        finally:
            if conn: conn.close()

    def get_facture(self, fact_id: str):
        """Get facture details for the given fact_id"""
        query = 'SELECT * FROM base_facture WHERE id = ?'
        result = self.make_query(query, [fact_id], display=True).as_namedtuple
        return result[0]

    def get_fact_details(self, fact_id: str) -> list:
        """Get facture details from FactureDetails table"""
        query = '''SELECT p.name, fd.qte, fd.price, fd.total FROM base_facturedetails AS fd
                   LEFT JOIN base_products AS p ON p.id == fd.product_id
                   WHERE fd.fact_id = ?'''
        _, rows = self.make_query(query, [fact_id])
        return rows

    def get_versement(self, client_id: str):
        """Select versement details from versement table for the give client_id"""
        query = 'SELECT vers_date, payment FROM base_versement WHERE client_id = ?'
        _, rows = self.make_query(query, [client_id])
        return rows

    def save_versement(self, client_id: str, payment: str):
        """Save a new versement"""
        payment = Decimal(payment)
        today = date.today().strftime('%d/%m/%Y')
        conn, curs = self.login()
        query = 'INSERT INTO base_versement(vers_date, client_id, payment) VALUES(?, ?, ?)'
        try:
            # TODO: return the count of rowcount if multiple facture has been updated
            # count = 0
            result = curs.execute(query, [today, client_id, self.stringify(payment)])
            utils.logger.debug('INSERT New_vers cli_id({})::payment({})::result({})'.format(client_id, payment, curs.rowcount))

            # select facture with remains for client_id
            query = 'SELECT id, total, remains FROM base_facture WHERE client_id = ? AND remains > 0'
            _, rows = self.make_query(query, [client_id])      # retrieve all non payed invoices
            for row in rows:
                fact_id, total_db, remains = row
                remains = Decimal(remains)
                if payment == remains:
                    # means pay one facture
                    new_total = remains - payment
                    query = 'UPDATE base_facture SET payment = payment + ?, remains = ?, paid_date = ? WHERE id = ?'
                    result = curs.execute(query, [self.stringify(payment), self.stringify(new_total), today, fact_id])
                    msg = 'UPDATING fact id:{}; pay:{}; total:{}; result:{}'.format(fact_id, payment, new_total, result.rowcount)
                    utils.logger.debug(msg)
                    utils.logger.debug('Done consuming payment. return')
                    break
                elif payment < remains:
                    # means facture stay with remains
                    new_remain = remains - payment
                    query = 'UPDATE base_facture SET payment = payment + ?, remains = ? WHERE id = ?'
                    result = curs.execute(query, [self.stringify(payment), self.stringify(new_remain), fact_id])
                    msg = 'UPDATING fact id:{}; pay:{}; total:{}; result:{}'.format(fact_id, payment, new_remain, result.rowcount)
                    utils.logger.debug(msg)
                    break
                elif payment > remains:
                    # payment greater than facture; and this will run again
                    payment = payment - remains
                    query = 'UPDATE base_facture SET payment = ?, remains = 0, paid_date = ? WHERE id = ?'
                    result = curs.execute(query, [total_db, today, fact_id])
                    utils.logger.debug('Pay > Remains')
                    msg = 'Result:{}, fact id:{}; total_db:{}; pay:{}; remains:0.'.format(fact_id, payment, payment, result.rowcount)
                    utils.logger.debug(msg)
        except sqlite3.Error as err:
            utils.logger.error(err)
        else:
            conn.commit()
            return True
        finally:
            if conn: conn.close()


if __name__ == '__main__':
    db_name = '/home/dabve/python/desktop_app/idir_app/server/pyqtapp/db.sqlite'
    db_handler = SqliteFunc(db_name)

    django_db_name = '/home/dabve/python/desktop_app/idir_app/server/db.sqlite3'
    django_dbhandler = SqliteFunc(django_db_name)

    query = 'SHOW CREATE TABLE Animal;'
    desc, rows = db_handler.make_query(query)
    for row in rows:
        print(row)
        query = 'INSERT INTO base_clients values(?, ?, ?, ?, ?, ?, ?, ?, ?)'
        result = django_dbhandler.make_query(query, row)
        # print(result)
        # print(row)
    # =============================================================
    # for table in ['base_products', 'base_clients', 'base_facture', 'base_facturedetails', 'base_versement']:
        # result = db_handler.make_query(f'DROP TABLE {table}')
        # print(f'-- DROP {table} :: {result}')
    # db_handler.create_tables()
    # =============================================================
    # result = db_handler.get_client_credits(1)
    # print(result)
    # result = db_handler.new_client('Amine philip', 'Douar boula', '0554000000', '123456', '123456', '123456')
    # print(result)
    # desc, rows = db_handler.dump_records(['name', 'address', 'phone', 'nif', 'nis', 'n_registre'], 'base_clients')
    # for row in rows:
        # print(row)
