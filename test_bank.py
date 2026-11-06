from bank import transfer
def test_insufficient_funds():
    accounts = {"alex": 1500, "max": 1000}
    history = []
    transfer(accounts,history,"alex","max",2000)
    assert transfer(accounts, history, "alex", "max", 2000) is False
    assert accounts["alex"] == 1500
    assert accounts["max"] == 1000
    assert history == []
def test_successful_transfer():
    accounts = {"alex": 1500, "max": 1000}
    history = []
    result = transfer(accounts,history,"alex","max",500)
    assert result is True
    assert accounts["alex"] == 1000
    assert accounts["max"] == 1500
    assert len(history) == 1
    assert history == [{'from': 'alex', 'to': 'max', 'amount': 500}]



