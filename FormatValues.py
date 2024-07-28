# FormatValues.py
def to_title_case(value):
    return value.title()

def to_upper_case(value):
    return value.upper()

def format_currency(value):
    return "${:,.2f}".format(value)

def validate_province(province, valid_provinces):
    return province.upper() in valid_provinces

# New function added for returning multiple values
def calculate_totals(base, *args):
    total = base + sum(args)
    return total, total * 0.15  # total and HST
