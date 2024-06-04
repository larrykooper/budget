import datetime
import pytz

from psycopg import sql

import src.flask_app.database.db_pool as db_pool

from src.adapters.repositories.category_repository import CategoryRepository

class LineItemWrite():

    # INSERT

    def add_line_item(self, line_item) -> int:
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
            show_on_spending_report,
            is_medical_reimbursement,
            is_synthetic,
            created,
            updated
        )
        VALUES (
            %(transaction_date)s,
            %(post_date)s,
            %(description)s,
            %(amount)s,
            %(category_id)s,
            %(transaction_type_id)s,
            %(account_id)s,
            %(check_number)s,
            %(type_detail_id)s,
            %(show_on_spending_report)s,
            %(is_medical_reimbursement)s,
            %(is_synthetic)s,
            %(created)s,
            %(updated)s
        ) RETURNING id;
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
            'show_on_spending_report': line_item.show_on_spending_report,
            'is_medical_reimbursement': line_item.is_medical_reimbursement,
            'is_synthetic': line_item.is_synthetic,
            'created': current_time,
            'updated': current_time
        }
        new_key = db_pool.insert_with_returned_id(query, params)
        return new_key


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
        category_repo = CategoryRepository()
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
        # If user has changed item to a tax category, update show_on_spending_report to False
        tax_cats_dicts = category_repo.get_ids_for_tax_cats()
        # tax_cats_dicts looks like [{'id': 16}, {'id': 47}]
        tax_cats = [x['id'] for x in tax_cats_dicts]
        if int(new_value) in tax_cats:
            self.set_sosp_to_false(id)

    def set_sosp_to_false(self, line_item_id):
        current_time = datetime.datetime.now(pytz.timezone("America/New_York"))
        query = """
            UPDATE line_item
            SET show_on_spending_report = 'f',
            updated = %(time)s
            WHERE id = %(line_item_id)s
            """
        params = {
            'line_item_id': line_item_id,
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

        # Exception 1A to Rule 1
        # Transaction_type is credit and account is Checking
        # And description contains both VENMO and CASHOUT
        #  Set show_on_spending_report to TRUE
        # Reason: Venmo cashouts offset spending
        # Also, we must make the amount negative
        qstring = """
        UPDATE line_item
        SET show_on_spending_report = 't',
        amount = -1 * amount
        FROM transaction_type, account
        WHERE line_item.transaction_type_id = transaction_type.id
        AND line_item.account_id = account.id
        AND transaction_type.name = 'credit'
        AND account.name = 'Checking'
        AND description LIKE {}
        AND description LIKE {}
        """
        params = {}
        executable_sql = sql.SQL(qstring).format(sql.Literal('%%VENMO%%'), sql.Literal('%%CASHOUT%%'))
        db_pool.update(executable_sql, params)

        # Rule 2: Account is Checking and description starts with "Payment to Chase card"
        # Reason: These items are when I pay a Chase credit card
        qstring = """
        UPDATE line_item
        SET show_on_spending_report = 'f'
        FROM account
        WHERE line_item.account_id = account.id
        AND account.name = 'Checking'
        AND UPPER(description) LIKE {}
        """
        params = {}
        executable_sql = sql.SQL(qstring).format(sql.Literal('PAYMENT TO CHASE CARD%%'))
        db_pool.update(executable_sql, params)

        # Rule 3: Account is Checking, transaction_type is 'dslip', and type_detail is 'check_deposit'
        # Reason: This is a deposit, not spending
        query = """
        UPDATE line_item
        SET show_on_spending_report = 'f'
        FROM transaction_type, account, type_detail
        WHERE line_item.transaction_type_id = transaction_type.id
        AND line_item.account_id = account.id
        AND line_item.type_detail_id = type_detail.id
        AND transaction_type.name = 'dslip'
        AND type_detail.name = 'check_deposit'
        AND account.name = 'Checking'
        """
        params = {}
        db_pool.update(query, params)

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

        # Rule 7: Account is 3307 or 2161 and description starts with "Payment Thank You"
        # Reason: This is me paying off a credit card
        qstring = """
        UPDATE line_item
        SET show_on_spending_report = 'f'
        FROM account
        WHERE line_item.account_id = account.id
        AND (account.name = 'Amazon-3307' OR account.name = 'Sapphire-2161')
        AND description LIKE {}
        """
        params = {}
        executable_sql = sql.SQL(qstring).format(sql.Literal('Payment Thank You%%'))
        db_pool.update(executable_sql, params)

        # Rule 8: Transaction type name is 'credit_card_payment'
        # Reason: Credit card payments are not spending, they are transfers.
        query = """
        UPDATE line_item
        SET show_on_spending_report = 'f'
        FROM transaction_type
        WHERE line_item.transaction_type_id = transaction_type.id
        AND transaction_type.name = 'credit_card_payment'
        """
        params = {}
        db_pool.update(query, params)

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

    def update_is_medical_reimbursement(self, deposits_to_update: list):
        query = """
        UPDATE line_item
        SET is_medical_reimbursement = 't'
        WHERE id = ANY(%(id_list)s)
        """
        params = {
            'id_list': deposits_to_update
        }
        db_pool.update(query, params)


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