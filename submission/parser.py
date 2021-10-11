"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""
DEBUG = False

# Initial Imports
import sys
from json import loads
from re import sub

# Imports added by Students
from collections.abc import Iterable
from glob import glob
from os import listdir, mkdir
from os.path import isdir, join, dirname, basename
from collections import namedtuple as named_tuple

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return f.endswith('.json')

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


NULL = 'NULL' # The value that None will be in the .dat files
Item = named_tuple('Item', ['id', 'name', 'currently', 'buy_price',
    'first_bid', 'number_of_bids', 'started', 'ends', 'seller', 'description'])
Bid = named_tuple('Bid', ['id', 'time', 'bidder', 'amount', 'bid_on'])
Person = named_tuple('Person', ['id', 'rating', 'location', 'country'])
Category = named_tuple('Category', ['name', 'item'])

def id_gen():
    n = -1
    while True:
        n += 1
        yield n

bid_id = id_gen() # Generate bid ids that will be unique for the current run of the program
category_proxy_id = id_gen()
"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database. Where the keys of the dictionary are the table names and then the value of each
table is a list of tuples representing the records that should be in that table.
"""
people_by_id = {} # Global so that it will apply to all the json files
def parseJson(json_file):
    item_list = []
    bid_list = []
    person_list = []
    category_list = []
    category_proxy_list = []

    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file

        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            item_id = int(item['ItemID'])

            for category in item['Category']:
                category_tuple = Category(
                    category, # Name of the category
                    item_id,
                )

                category_list.append(category_tuple)

            # Load in Bids for this Item
            if item['Bids'] is not None:
                for bid in item['Bids']:
                    bid = bid['Bid']
                    # Handle Bidder (a Person)
                    bidder = bid['Bidder']
                    bidder_id = bidder["UserID"] # Person.id
                    rating = int(bidder['Rating'])

                    location = NULL if not ('Location' in bidder) else bidder['Location']
                    country = NULL if not ('Country' in bidder) else bidder['Country']

                    # If there is a record already in the people_by_id dict,
                    #   then make sure the location or country is not lost
                    #   (because this record may have location or country = NULL)
                    #   when this record takes its place
                    if bidder_id in people_by_id:
                        other_record = people_by_id[bidder_id]

                        if location is NULL:
                            location = other_record.location

                        if country is NULL:
                            country = other_record.country

                    bidder_tuple = Person(
                        bidder_id,
                        rating,
                        location,
                        country
                    )
                    people_by_id[bidder_id] = bidder_tuple

                    # Create bid Tuple
                    bid_tuple = Bid(
                        next(bid_id),
                        transformDttm(bid["Time"]),
                        bidder_id,
                        transformDollar(bid["Amount"]),
                        item_id,
                    )
                    bid_list.append(bid_tuple)

            # Handle Seller (a Person)
            seller = item['Seller']
            seller_id = seller['UserID'] # Person.id

            if not (seller_id in people_by_id):
                seller_tuple = Person(
                    seller_id,
                    seller['Rating'],
                    item['Location'],
                    item['Country'],
                )
                people_by_id[seller_id] =seller_tuple

            # Create the tuple for the current Item
            item_tuple = Item(
                item_id,
                item['Name'],
                transformDollar(item['Currently']),
                NULL if not ('Buy_Price' in item) else transformDollar(item['Buy_Price']),
                transformDollar(item['First_Bid']),
                int(item["Number_of_Bids"]),
                transformDttm(item['Started']),
                transformDttm(item['Ends']),
                seller_id,
                item['Description']
            )

            item_list.append(item_tuple)

        schema = {
            'Item': item_list,
            'Bid': bid_list,
            'Person': person_list,
            'Category': category_list,
        }

        return schema

def flatten(li):
    for el in li:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print('Usage: python parser.py <path to json files>')
        sys.exit(1)

    visited = set()

    file_stack = [fi for fi in flatten([glob(f) for f in argv[1:]])]

    item_list = []
    bid_list = []
    person_list = []
    category_list = []
    category_proxy_list = []

    # loops over all .json files in the argument
    while len(file_stack) > 0:
        f = file_stack.pop()

        if isdir(f):
            for file_or_dir in listdir(f):
                file_stack.append(file_or_dir)
            continue

        # Make sure not to visit the same file twice or visit a file that is not json
        if f in visited or not isJson(f):
            continue

        visited.add(f)

        parsed_json = parseJson(f)
        item_list.extend(parsed_json['Item'])
        bid_list.extend(parsed_json['Bid'])
        person_list.extend(parsed_json['Person'])
        category_list.extend(parsed_json['Category'])

        if DEBUG:
            print("Success parsing " + f)

    # Write the .dat files
    dat_ext = '.dat'

    if DEBUG:
        dat_file_dir = join(dirname(__file__), 'dat_files')
        if not isdir(dat_file_dir):
            mkdir(dat_file_dir)
    else:
        dat_file_dir = '.'

    def write_list_to_file(li, f_path):
        f_name = basename(f_path)

        if DEBUG: print(f'Creating set for {f_name}...')

        li = set(li)

        if DEBUG: print('...done!')

        if DEBUG: print(f'Returning to list for {f_name}...')

        li = [e for e in li]

        if DEBUG:
            print(f'...done!')
            print(f'Constructing string to print for {f_name}...')

        out_str = ''
        for obj in li:
            obj_len = len(obj) - 1

            for i, element in enumerate(obj):
                out_str += str(element)

                if i < obj_len:
                    out_str += columnSeparator

            #out_str = out_str.rstrip(columnSeparator)
            out_str += '\n'

        if DEBUG: print('...done!')

        out_str = out_str.replace('"', '\\"')

        with open(f_path, "w") as f:
            if DEBUG: print(f'Writing to {f_name}...')

            f.write(out_str)

            if DEBUG: print('...done!')

    # Have to do this to debug:
    # Persons have not been added to the person_list yet. They have
    #   only been stored in the people_by_id dict so add them to the
    #   person_list now
    person_list.extend(people_by_id.values())

    # Now write all to files
    write_list_to_file(item_list, join(dat_file_dir, f'Item{dat_ext}'))
    write_list_to_file(bid_list, join(dat_file_dir, f'Bid{dat_ext}'))
    write_list_to_file(person_list, join(dat_file_dir, f'Person{dat_ext}'))
    write_list_to_file(category_list, join(dat_file_dir, f'Category{dat_ext}'))

if __name__ == '__main__':
    main(sys.argv)







