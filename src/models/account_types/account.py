class Account:

    @staticmethod
    def instantiate_account(account: str):
        from src.models.account_types.capital_one import CapitalOne
        from src.models.account_types.chase_checking import ChaseChecking
        from src.models.account_types.sapphire import Sapphire
        if account == "Capital-One":
            return CapitalOne()
        if account == "Checking":
            return ChaseChecking()
        if account == "Sapphire-2161":
            return Sapphire()