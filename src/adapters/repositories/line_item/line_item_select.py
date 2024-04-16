import datetime

from psycopg import sql

import src.flask_app.database.db_pool as db_pool

class LineItemSelect():

    # SELECT

    def get_for_synth_trans(
        self,
        id
    ) -> dict:
        """
        Read one line tiem
        """
        qstring = """
        SELECT
        id,
        transaction_date,
        amount
        FROM line_item
        WHERE id = {}
        """
        params = {}
        executable_sql = sql.SQL(qstring).format(sql.Literal(id))
        data = db_pool.get_data(executable_sql, params, single_row=True)
        return data


    def get_for_spending_report(
            self,
            start_date: datetime.date,
            end_date: datetime.date,
            sort_column: str,
            sort_direction: str,
            sort_table: str = None,
            ) -> list[dict]:
        """
        You cannot use the "%s" pattern to pass field names, table names,
        or snippets of SQL (such as ASC) to "execute." You can only use the
        "%s" pattern to pass values.
        So in this case I had to use sql.Identifier to pass the field name,
        and sql.SQL to pass the sort direction.
        See: https://www.psycopg.org/psycopg3/docs/api/sql.html
        ---
        """
        qstring = """
        SELECT
            li.id,
            transaction_date,
            post_date,
            description,
            amount,
            cat.name AS cat_name,
            transaction_type_id,
            acc.name AS account_name,
            check_number,
            type_detail_id,
            comment,
            show_on_spending_report
        FROM line_item li
        LEFT JOIN category cat
        ON li.category_id = cat.id
        LEFT JOIN transaction_type tt
        ON li.transaction_type_id = tt.id
        LEFT JOIN account acc
        ON acc.id = li.account_id
        WHERE li.transaction_date BETWEEN %(start_date)s AND %(end_date)s
        AND li.show_on_spending_report
        ORDER BY {} {}
        """
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        executable_sql = sql.SQL(qstring).format(sql.Identifier(sort_table, sort_column), sql.SQL(sort_direction))
        data = db_pool.get_data(executable_sql, params, single_row=False)
        return data

    def get_for_spending_by_cat(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
        sort_column: str,
        sort_direction: str,
        ) -> list[dict]:
        qstring = """
        SELECT cat.name AS catname, SUM(amount) AS amtsum
        FROM line_item li
        LEFT JOIN category cat
        ON li.category_id = cat.id
        WHERE transaction_date BETWEEN %(start_date)s AND %(end_date)s
        AND show_on_spending_report
        GROUP BY catname
        ORDER BY {} {}
        """
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        executable_sql = sql.SQL(qstring).format(sql.Identifier(sort_column), sql.SQL(sort_direction))
        data = db_pool.get_data(executable_sql, params, single_row=False)
        return data

    def total_spending_per_month_for_year(
        self,
        start_of_year: datetime.date,
        end_of_year: datetime.date
    ) -> list[dict]:
        query = """
        SELECT EXTRACT(MONTH FROM transaction_date) AS mymonth, SUM(amount)
        FROM line_item
        WHERE transaction_date BETWEEN %(start_of_year)s AND %(end_of_year)s
        AND show_on_spending_report
        GROUP BY EXTRACT(MONTH FROM transaction_date)
        ORDER BY EXTRACT(MONTH FROM transaction_date)
        """
        params = {
            'start_of_year': start_of_year,
            'end_of_year': end_of_year
        }
        data = db_pool.get_data(query, params, single_row=False)
        return data

    def total_spending_per_month(
        self,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> list[dict]:
        query = """
        SELECT SUM(amount)
        FROM line_item
        WHERE transaction_date BETWEEN %(start_date)s AND %(end_date)s
        AND show_on_spending_report
        """
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        data = db_pool.get_data(query, params, single_row=True)
        return data

    def get_bank_deposits(
        self,
        start_of_year: datetime.date,
        end_of_year: datetime.date
    ) -> list[dict]:
        query = """
        SELECT li.id, transaction_date, description, amount, is_medical_reimbursement
        FROM line_item li
        INNER JOIN account acc
        ON li.account_id = acc.id
        INNER JOIN transaction_type tt
        ON li.transaction_type_id = tt.id
        INNER JOIN type_detail td
        ON li.type_detail_id = td.id
        WHERE transaction_date BETWEEN %(start_of_year)s AND %(end_of_year)s
        AND tt.name = 'dslip'
        AND td.name = 'check_deposit'
        AND acc.name = 'Checking'
        ORDER BY transaction_date
        """
        params = {
            'start_of_year': start_of_year,
            'end_of_year': end_of_year
        }
        data = db_pool.get_data(query, params, single_row=False)
        return data
