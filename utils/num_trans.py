def arabic_to_chinese(num):
    chinese_digits = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
    chinese_units = ["", "十", "百", "千", "万", "亿"]

    if num == 0:
        return chinese_digits[0]

    result = ""
    unit_index = 0
    while num > 0:
        digit = num % 10
        if digit == 0:
            if result and result[-1] != chinese_digits[0]:
                result += chinese_digits[0]
        elif digit == 1 and unit_index == 1:
            result += chinese_units[unit_index]
        else:
            result += chinese_digits[digit] + chinese_units[unit_index]

        num //= 10
        unit_index += 1

    return result


def chinese_to_arabic(chinese_num):
    chinese_digits = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
    chinese_units = ["", "十", "百", "千", "万", "亿"]

    arabic_num = 0
    unit_value = 1

    for digit in reversed(chinese_num):
        if digit in chinese_digits:
            arabic_num += chinese_digits.index(digit) * unit_value
        elif digit in chinese_units:
            unit_value *= 10 ** chinese_units.index(digit)

    return arabic_num
