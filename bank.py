accounts = {
    "alex": 1500,
    "max": 1000
}
history = []
def transfer(accounts,history, sender, receiver, amount):
        if sender not in accounts:
            return False
        if receiver not in accounts:
            return False
        if receiver == sender:
            return False
        if not isinstance(amount,(int,float)):
            return False
        if amount <= 0:
            return False
        if amount > accounts[sender]:
            return False
        accounts[sender] -= amount
        accounts[receiver] += amount
        transaction = {
                "from": sender,
                "to": receiver,
                "amount": amount
            }
        history.append(transaction)
        return True
if __name__ == "__main__":
    
    transfer(accounts, history, "alex", "max", 500)

    print(accounts)
    print(history)