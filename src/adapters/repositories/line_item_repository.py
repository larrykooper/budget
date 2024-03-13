import datetime
import pytz

from psycopg import sql

from src.adapters.repositories.abstract_repository import AbstractRepository
import src.flask_app.database.db_pool as db_pool

class LineItemRepository(AbstractRepository):

    # INSERT

    def add_line_item(self, line_item):
        current_time = datetime.datetime.now(pytz.timezone("America/New_York"))
        query = """
        INSERT INTO line_item (
            transaction_date,
            post_date,
            description,
            amount,
            category_id,
            transaction_type_id,
            account_id,
            check_number,
            type_detail_id,
            data_hash,
            show_on_spending_report,
            created,
            updated
        )
            VALUES (%(transaction_date)s, %(post_date)s, %(description)s, %(amount)s,
              %(category_id)s, %(transaction_type_id)s, %(account_id)s, %(check_number)s,
              %(type_detail_id)s, %(data_hash)s, %(show_on_spending_report)s,  %(created)s, %(updated)s);
        """
        params = {
            'transaction_date': line_item.transaction_date,
            'post_date': line_item.post_date,
            'description': line_item.description,
            'amount': line_item.amount,
            'category_id': line_item.category_id,
            'transaction_type_id': line_item.transaction_type_id,
            'account_id': line_item.account_id,
            'check_number': line_item.check_number,
            'type_detail_id': line_item.type_detail_id,
            'data_hash': line_item.data_hash,
            'show_on_spending_report': line_item.show_on_spending_report,
            'created': current_time,
            'updated': current_time
        }
        results = db_pool.insert(query, params)
        return results

    # SELECT

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
        Credit card payments are not spending, they are transfers.
        """
        qstring = """
        SELECT
            li.id,
            transaction_date,
            post_date,
            description,
            amount,
            category_id,
            transaction_type_id,
            account_id,
            check_number,
            type_detail_id,
            comment,
            show_on_spending_report
        FROM line_item li
        LEFT JOIN category cat
        ON li.category_id = cat.id
        LEFT JOIN transaction_type tt
        ON li.transaction_type_id = tt.id
        WHERE li.transaction_date BETWEEN %(start_date)s AND %(end_date)s
        AND tt.name <> 'credit_card_payment'
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
        ) -> list[dict]:
        query = """
        SELECT cat.name, SUM(amount)
        FROM line_item li
        LEFT JOIN category cat
        ON li.category_id = cat.id
        WHERE transaction_date BETWEEN %(start_date)s AND %(end_date)s
        AND show_on_spending_report
        GROUP BY cat.name
        ORDER BY cat.name
        """
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        data = db_pool.get_data(query, params, single_row=False)
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

    # UPDATE

    def update_comment(self, new_value, id):
        current_time = datetime.datetime.now(pytz.timezone("America/New_York"))
        query = """
        UPDATE line_item
        SET comment = %(new_value)s,
        updated = %(time)s
        WHERE id = %(line_item_id)s
        """
        params = {
            'new_value': new_value,
            'line_item_id': id,
            'time': current_time
        }
        db_pool.update(query, params)

    def update_category(self, new_value, id):
        current_time = datetime.datetime.now(pytz.timezone("America/New_York"))
        query = """
        UPDATE line_item
        SET category_id = %(new_value)s,
        updated = %(time)s
        WHERE id = %(line_item_id)s
        """
        params = {
            'new_value': new_value,
            'line_item_id': id,
            'time': current_time
        }
        db_pool.update(query, params)

    def update_show_on_spending_report(self):
        """
        Note for future: I can delete some of these rules when there are no more
        files from Amex, Apple, Capital One, or Discover.
        I can delete Rule 4, Rule 5, and Rule 6.
        """
        # Rule 1: Transaction_type is credit and account is Checking
        # Reason: Credit items are not spending
        query = """
        UPDATE line_item
        SET show_on_spending_report = 'f'
        FROM transaction_type, account
        WHERE line_item.transaction_type_id = transaction_type.id
        AND line_item.account_id = account.id
        AND transaction_type.name = 'credit'
        AND account.name = 'Checking'
        """
        params = {}
        db_pool.update(query, params)

        # Rule 2: Account is Checking and description starts with "Payment to Chase card"
        # Reason: These items are when I pay a Chase credit card
        qstring = """
        UPDATE line_item
        SET show_on_spending_report = 'f'
        FROM account
        WHERE line_item.account_id = account.id
        AND account.name = 'Checking'
        AND description LIKE {}
        """
        params = {}
        executable_sql = sql.SQL(qstring).format(sql.Literal('Payment to Chase card%%'))
        db_pool.update(executable_sql, params)

        # Rule 3: Description starts with REMOTE ONLINE DEPOSIT
        # Reason: Deposit, not spending
        qstring = """
        UPDATE line_item
        SET show_on_spending_report = 'f'
        WHERE description LIKE {}
        """
        params = {}
        executable_sql = sql.SQL(qstring).format(sql.Literal('REMOTE ONLINE DEPOSIT%%'))
        db_pool.update(executable_sql, params)

        # Rule 4: Account is Checking and description starts with AMERICAN EXPRESS ACH PMT
        # Reason: Because this is me paying an Amex card
        qstring = """
        UPDATE line_item
        SET show_on_spending_report = 'f'
        FROM account
        WHERE line_item.account_id = account.id
        AND account.name = 'Checking'
        AND description LIKE {}
        """
        params = {}
        executable_sql = sql.SQL(qstring).format(sql.Literal('AMERICAN EXPRESS ACH PMT%%'))
        db_pool.update(executable_sql, params)

        # Rule 5: Account is Discover and description starts with either INTERNET PAYMENT or CASHBACK BONUS
        # Reason: This is either a card bonus or me paying off a card
        qstring = """
        UPDATE line_item
        SET show_on_spending_report = 'f'
        FROM account
        WHERE line_item.account_id = account.id
        AND account.name = 'Discover'
        AND (description LIKE {}
        OR description LIKE {})
        """
        params = {}
        executable_sql = sql.SQL(qstring).format(sql.Literal('INTERNET PAYMENT%%'),
                        sql.Literal('CASHBACK BONUS%%'))
        db_pool.update(executable_sql, params)

        # Rule 6: Account is Checking and description starts with APPLECARD or DISCOVER or CAPITAL ONE
        # Reason: This is me paying off a credit card
        qstring = """
        UPDATE line_item
        SET show_on_spending_report = 'f'
        FROM account
        WHERE line_item.account_id = account.id
        AND account.name = 'Checking'
        AND (description LIKE {}
        OR description LIKE {}
        OR description LIKE {})
        """
        params = {}
        executable_sql = sql.SQL(qstring).format(sql.Literal('APPLECARD%%'),
                    sql.Literal('CAPITAL ONE%%'),
                    sql.Literal('DISCOVER%%'))
        db_pool.update(executable_sql, params)

    def recategorize_existing_line_items_starts_with(self, new_category_id, search_term):
        """
        Recategorize existing line items based on a starts_with rule
        """
        qstring = """
        UPDATE line_item
        SET category_id =  %(new_category_id)s
        WHERE LOWER(description) LIKE {}
        """
        params = {
            'new_category_id': new_category_id
        }
        literal_param = f"{search_term}%%"
        executable_sql = sql.SQL(qstring).format(sql.Literal(literal_param))
        db_pool.update(executable_sql, params)

    def recategorize_existing_line_items_contains(self, new_category_id, search_term):
        """
        Recategorize existing line items based on a contains rule
        """
        qstring = """
        UPDATE line_item
        SET category_id =  %(new_category_id)s
        WHERE LOWER(description) LIKE {}
        """
        params = {
            'new_category_id': new_category_id
        }
        literal_param = f"%%{search_term}%%"
        executable_sql = sql.SQL(qstring).format(sql.Literal(literal_param))
        db_pool.update(executable_sql, params)


    """
    this worked to recategorize the existing line items
    via a new rule

    WITH new_category AS (
    SELECT id FROM category
    WHERE name = 'Doctor'
    )
    UPDATE line_item
    SET category_id = new_category.id
    FROM new_category
    WHERE LOWER(description) LIKE '%cognitive and behavioral%'  <-- contains rule

    """
    # DELETE

    def delete_line_item(self, id):
        query = """
        DELETE FROM line_item
        WHERE id = %(line_item_id)s
        """
        params = {
            'line_item_id': id
        }
        db_pool.delete(query, params)