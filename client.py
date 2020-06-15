import requests
from pyless.utils.enums.parameter_keys import ParameterKeys as key

api_url = "https://o7nhypit90.execute-api.us-east-1.amazonaws.com/prod/loans"


def create_loan(amount, interest, monthly_payment, loan_length):
    x = requests.post(api_url, json={key.AMOUNT: float(amount),
                                 key.INTEREST_RATE: float(interest),
                                 key.LENGTH_OF_LOAN: int(loan_length),
                                 key.MONTHLY_PAYMENT: float(monthly_payment)})
    print(x.json())


def update_loan(loan_id, amount, interest, monthly_payment, loan_length):

    data_out = dict()
    data_out[key.U_ID] = int(loan_id)
    if amount:
        data_out[key.AMOUNT] = float(amount)
    if interest:
        data_out[key.INTEREST_RATE] = float(interest)
    if monthly_payment:
        data_out[key.MONTHLY_PAYMENT] = float(monthly_payment)
    if loan_length:
        data_out[key.LENGTH_OF_LOAN] = int(loan_length)

    x = requests.put(api_url, json=data_out)
    print(x.json())


def get_loan(loan_id):
    x = requests.get(api_url+f"?{key.U_ID}={int(loan_id)}")
    print(x.json())


def get_loan_details():
    print("Loan Amount:", end=" ")
    amount = input()
    print("Interest Rate:", end=" ")
    interest = input()
    print("Monthly Payment:", end=" ")
    monthly_payment = input()
    print("Length of Loan in months:", end=" ")
    loan_length = input()

    return amount, interest, monthly_payment, loan_length


def get_loan_id():
    print("Loan id:", end=" ")
    loan_id = input()
    return loan_id


while True:
    # get which function to call
    print("\n\n\n========")
    print("0: Create Loan")
    print("1: Get Loan")
    print("2: Update Loan")
    print("Which Function do you want to call?", end=" ")
    func_state = input()
    # get inputs for that function
    if func_state == "0":
        print("===============\nCreate a Loan Selected")
        amount, interest, monthly_payment, loan_length = get_loan_details()
        create_loan(amount, interest, monthly_payment, loan_length )

    elif func_state == "1":
        print("===============\nGet a Loan Selected")
        loan_id = get_loan_id()
        if loan_id is None:
            print("Loan Id can not be none, invalid input")
            continue
        get_loan(loan_id)

    elif func_state == "2":
        print("===============\nGet a Loan Selected")
        loan_id = get_loan_id()
        if loan_id is None:
            print("Loan Id can not be none, invalid input")
            continue
        amount, interest, monthly_payment, loan_length = get_loan_details()
        update_loan(loan_id, amount, interest, monthly_payment, loan_length)

    else:
        print("Invalid Input, try again.\n\n\n\n")
        continue




    # call function/display out put
