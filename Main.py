import datetime
import time
import os
from FormatValues import to_title_case, to_upper_case, format_currency, validate_province, calculate_totals

# Load constants from Const.dat
with open('Const.dat') as f:
    data = f.read().split()
    policy_number = int(data[0])
    basic_premium = float(data[1])
    discount = float(data[2])
    extra_liability_cost = float(data[3])
    glass_coverage_cost = float(data[4])
    loaner_car_cost = float(data[5])
    hst_rate = float(data[6])
    processing_fee = float(data[7])

# Validate province and payment method using lists
valid_provinces = ['ON', 'QC', 'NS', 'NB', 'MB', 'BC', 'PE', 'SK', 'AB', 'NL']
valid_payment_methods = ['Full', 'Monthly', 'Down Pay']

def get_customer_info():
    first_name = to_title_case(input("Enter first name: "))
    last_name = to_title_case(input("Enter last name: "))
    address = input("Enter address: ")
    city = to_title_case(input("Enter city: "))
    province = input("Enter province: ")
    while not validate_province(province, valid_provinces):
        print("Invalid province. Please enter a valid province.")
        province = input("Enter province: ")
    postal_code = input("Enter postal code: ")
    phone_number = input("Enter phone number: ")
    return first_name, last_name, address, city, to_upper_case(province), postal_code, phone_number

def get_car_info():
    num_cars = int(input("Enter the number of cars being insured: "))
    extra_liability = to_upper_case(input("Extra liability coverage (Y/N): "))
    glass_coverage = to_upper_case(input("Glass coverage (Y/N): "))
    loaner_car = to_upper_case(input("Loaner car coverage (Y/N): "))
    return num_cars, extra_liability, glass_coverage, loaner_car

def get_payment_info():
    payment_method = input("Enter payment method (Full, Monthly, Down Pay): ")
    while payment_method not in valid_payment_methods:
        print("Invalid payment method. Please enter a valid payment method.")
        payment_method = input("Enter payment method (Full, Monthly, Down Pay): ")
    down_payment = 0
    if payment_method == 'Down Pay':
        down_payment = float(input("Enter down payment amount: "))
    return to_title_case(payment_method), down_payment

def get_claims():
    claims = []
    while True:
        claim_number = input("Enter claim number (or 'done' to finish): ")
        if claim_number.lower() == 'done':
            break
        claim_date = input("Enter claim date (YYYY-MM-DD): ")
        claim_amount = float(input("Enter claim amount: "))
        claims.append((claim_number, claim_date, claim_amount))
    return claims

def calculate_premium(num_cars, extra_liability, glass_coverage, loaner_car):
    total_premium = basic_premium + (num_cars - 1) * basic_premium * (1 - discount)
    total_extra_costs = 0
    if extra_liability == 'Y':
        total_extra_costs += num_cars * extra_liability_cost
    if glass_coverage == 'Y':
        total_extra_costs += num_cars * glass_coverage_cost
    if loaner_car == 'Y':
        total_extra_costs += num_cars * loaner_car_cost
    total_premium += total_extra_costs
    return total_premium

def display_receipt(customer_info, car_info, payment_info, claims, total_premium, total_cost, hst, monthly_payment=None, first_payment_date=None):
    first_name, last_name, address, city, province, postal_code, phone_number = customer_info
    num_cars, extra_liability, glass_coverage, loaner_car = car_info
    payment_method, down_payment = payment_info
    
    print("\nOne Stop Insurance Company")
    print(f"Policy Number: {policy_number}")
    print(f"Customer: {first_name} {last_name}")
    print(f"Address: {address}, {city}, {province}, {postal_code}")
    print(f"Phone: {phone_number}")
    print(f"Number of Cars Insured: {num_cars}")
    print(f"Extra Liability: {extra_liability}")
    print(f"Glass Coverage: {glass_coverage}")
    print(f"Loaner Car: {loaner_car}")
    print(f"Payment Method: {payment_method}")
    print(f"Down Payment: {format_currency(down_payment)}")
    print(f"Total Premium (Pre-Tax): {format_currency(total_premium)}")
    print(f"HST: {format_currency(hst)}")
    print(f"Total Cost: {format_currency(total_cost)}")
    if monthly_payment:
        print(f"Monthly Payment: {format_currency(monthly_payment)}")
        print(f"First Payment Date: {first_payment_date.strftime('%Y-%m-%d')}")
    
    print("\nPrevious Claims")
    print("Claim #  Claim Date        Amount")
    print("---------------------------------")
    for claim in claims:
        print(f"{claim[0]:<7} {claim[1]:<15} {format_currency(claim[2]):<10}")

def main():
    global policy_number

    while True:
        customer_info = get_customer_info()
        car_info = get_car_info()
        payment_info = get_payment_info()
        claims = get_claims()

        num_cars, extra_liability, glass_coverage, loaner_car = car_info
        total_premium = calculate_premium(num_cars, extra_liability, glass_coverage, loaner_car)
        total_cost, hst = calculate_totals(total_premium, total_premium * hst_rate)
        
        if payment_info[0] == 'Full':
            monthly_payment = None
        else:
            down_payment = payment_info[1]
            if payment_info[0] == 'Monthly':
                monthly_payment = (total_cost + processing_fee) / 8
            else:
                monthly_payment = (total_cost - down_payment + processing_fee) / 8
        
        invoice_date = datetime.datetime.now()
        first_payment_date = (invoice_date.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)

        display_receipt(customer_info, car_info, payment_info, claims, total_premium, total_cost, hst, monthly_payment, first_payment_date)
        
        # Simulate saving data with a progress bar
        print("\nSaving policy data", end="")
        for _ in range(3):
            time.sleep(0.5)
            print(".", end="")
        print(" Done!")
        
        # Increase policy number
        policy_number += 1

        # Save updated policy number to Const.dat
        with open('Const.dat', 'w') as f:
            f.write(f"{policy_number}\n869.00\n0.25\n130.00\n86.00\n58.00\n0.15\n39.99")

        another = input("Would you like to enter another customer? (Y/N): ").upper()
        if another != 'Y':
            break

if __name__ == "__main__":
    main()
