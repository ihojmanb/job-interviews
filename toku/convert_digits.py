# a function receives a string 'input_string' and two integers,
# 'start_position' and 'end_position'. The function needs to 
# convert the numbers to its equivalent alphabetical capitalized form
# and return the input_string with the number digits modified between 
# the start_position and end_position

# if end_position > length of input_string, return "INVALID"
# if start_position > end_position, return "INVALID"
# if start_position < 1, return "INVALID"
# if start_position is 1, it means to start at the first character of the
# input_string

# alphabetical capitalized number representation dict.
alphabetical_number = {
    "1":"ONE",
    "2":"TWO",
    "3":"THREE",
    "4":"FOUR",
    "5":"FIVE",
    "6":"SIX",
    "7":"SEVEN",
    "8":"EIGHT",
    "9":"NINE",
    "0":"ZERO",
}
# procedural version od the digit converter
def digit_converter(input_string, start_position, end_position):
    new_string = input_string[:start_position - 1]
    replacing_string = '' 
    for index in range(start_position - 1, end_position):
        
        if input_string[index].isdigit():
            replacing_string = alphabetical_number[input_string[index]]
            new_string += replacing_string
        else:
            new_string += input_string[index]  
    new_string += input_string[end_position:]
        
    return new_string

# functional version of the digit converter
def functional_digit_converter(input_string, start_position, end_position):
    string_prefix = input_string[:start_position -1]
    replaced_substring = ''.join(list(map(lambda char: alphabetical_number[char] if 
    char.isdigit() else char, iter(input_string[start_position - 1:end_position]))))
    string_suffix = input_string[end_position:]
    new_string = string_prefix + replaced_substring + string_suffix
    return new_string

def convert_digits(input_string, start_position, end_position):
    if (start_position < 1 or end_position > len(input_string) 
    or start_position > end_position):
        return "INVALID"
    else:
        return functional_digit_converter(input_string, start_position, end_position)
