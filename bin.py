#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# KILL THE NET

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from prettytable import PrettyTable
from sys import argv

# Suppress InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def _check_(cc):
    T = PrettyTable()
    try:
        # Make the API request while ignoring SSL verification
        r = requests.get(f"https://api.apilayer.com/bincheck/{cc}",
                         headers={
                             "apikey": "AZ9aDUWXLehBAuad3xOvc0s0wtZRFplZ"
                         },
                         verify=False)  # Disable SSL verification

        # Raise an HTTP error if the status code is not 200
        r.raise_for_status()

        # Parse the JSON response
        data = r.json()

        # Check if the response contains valid data
        if not data:
            print(f"No valid data returned for BIN {cc}.")
            return

        # Extract fields from the response based on your provided structure
        bank_name = data.get("bank_name", "N/A")
        bin_number = data.get("bin", "N/A")
        country = data.get("country", "N/A")
        scheme = data.get("scheme", "N/A")
        card_type = data.get("type", "N/A")
        url = data.get("url", "N/A")

        # Set up the PrettyTable
        T.field_names = [
            'CARD NUM', 'CARD SCHEME', 'CARD TYPE', 'CARD COUNTRY', 
            'BANK NAME', 'CARD URL'
        ]
        T.add_row([
            bin_number,
            scheme,
            card_type,
            country,
            bank_name,
            url
        ])

        print(T)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except Exception as e:
        print(f"Error processing the BIN data: {e}")


if __name__ == '__main__':
    while True:
        try:
            if len(argv) == 2:
                if len(argv[1]) >= 6:
                    _check_(argv[1])
                    break
                else:
                    cc = input("[•] PLEASE PUT THE FIRST 6 DIGITS OF YOUR CARD > ").replace(" ", "")
                    if len(cc) >= 6:
                        _check_(cc)
                        break
            else:
                cc = input("[•] PLEASE PUT THE FIRST 6 DIGITS OF YOUR CARD > ").replace(" ", "")
                if len(cc) >= 6:
                    _check_(cc)
        except KeyboardInterrupt:
            print("\nGOODBYE!")
            exit()
        except EOFError:
            print("\nGOODBYE!")
            exit()