def is_bouncy(number: int):
    digits = str(number)
    increasing = False
    decreasing = False

    for i in range(len(digits) - 1):
        if digits [i] < digits [i + 1]:
            increasing = True
        elif digits [i] > digits [i + 1]:
            decreasing = True

    return increasing and decreasing

def least_number_with_bouncy_ratio(percent: int) -> int:
    if not 1 <= percent <= 99:
        raise ValueError("El porcentaje debe estar entre 1 y 99.")

    bouncy_count = 0
    number = 1

    while True:
        if is_bouncy(number):
            bouncy_count += 1
        if bouncy_count * 100 == percent * number:
            return number
        number += 1  
