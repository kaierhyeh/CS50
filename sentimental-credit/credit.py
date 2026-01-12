number = input("Number: ")


def Luhn(number: str) -> bool:
    total = 0

    # Iterate with enumerate
    for i, c in enumerate(number[::-1]):
        value = int(c)
        if i % 2 == 1:
            value *= 2
            if value > 9:
                value = value // 10 + value % 10
        total += value
    return total % 10 == 0
# enumerate(...), which 回傳 tuple(index, value) (tuple就是一組資料，創建後無法更改)
# [::-1] reverses the string
# / and // are float and integer division respectively
# [Syntax]
# sequence[start:end:step]
#     x[1:]	From index 1 to the end
#     x[:3]	From start to index 2
#     x[::2]	From start to end, every 2 steps
#     x[::-1]	From end to start, step = -1 → reversed


def company(number: str) -> str:
    d = len(number)
    num = int(number[:2])    # Extract first 2 digits

    if num // 10 == 4 and (d == 13 or d == 16):
        return "VISA"
    elif (num == 34 or num == 37) and d == 15:
        return "AMEX"
    elif 51 <= num <= 55 and d == 16:
        return "MASTERCARD"
    else:
        return "INVALID"


if not Luhn(number):
    print("INVALID")
else:
    print(company(number))
