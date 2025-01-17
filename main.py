"""

Author: Aaron Ballesteros
Student ID: 011019047
Start Date: 4/1/2023
Last Modified: 4/14/2023
Class: Data Structures and Algorithms II
School: Western Governors University

Description:
The goal is to solve the logistical challenges of the Western Governors University Parcel Service (WGUPS) by
optimizing delivery routes under specific constraints such as delivery deadlines, package requirements, and truck capacity.
The main challenge we are solving is to meet delivery deadlines within a minimal total distance but also to build an application
that can adapt to real-time logistical changes.

"""

import csv
import datetime
import time
import re

from console import Colors


def log_truck_metrics_with_date(truck, truck_num):
    """
    This function calculates and formats the metrics for a given truck.

    Parameters:
    truck (Trucks): The truck object for which the metrics are to be calculated.
    truck_num (int): The number of the truck.

    Time Complexity: O(1) - Constant time complexity.

    Returns:
    A formatted string of the truck's metrics.

    """

    # Calculate the drive time in hours
    # 1 hour = 3600 seconds
    drive_time = truck.time.total_seconds() / 3600 - truck.depart_time.total_seconds() / 3600

    # Use a recent date as the base date for Departure and Return Time
    # Replace with the actual recent date you want to use
    base_date = datetime.datetime(2024, 4, 1).date()

    # Add the base date to the departure and return time and format them to include date and time information
    departure_datetime = datetime.datetime.combine(base_date, datetime.datetime.min.time()) + truck.depart_time
    return_datetime = datetime.datetime.combine(base_date, datetime.datetime.min.time()) + truck.time
    departure_time_str = departure_datetime.strftime('%Y-%m-%d %H:%M:%S')
    return_time_str = return_datetime.strftime('%Y-%m-%d %H:%M:%S')

    # Create a formatted string with the truck metrics
    metrics_str = (
        f"\n{Colors.BOLD_ORANGE}Truck #{truck_num} metrics:\n"
        f"———————————————————————————————————————————————{Colors.END}\n"
        f"Departure Time: {departure_time_str}\n"
        f"Return Time: {return_time_str}\n"
        f"Drive Time: {drive_time:.2f} hours\n"
        f"Total Distance: {truck.miles:.1f} miles\n"
    )
    return metrics_str


class ChainingHashTable:
    """
    ,------------------------------------------------------------------------------------------------,
    |                                HASH TABLE WITH CHAINS CLASS                                    |
    |                                Time Complexity: O(1) - O(n)                                    |
    '------------------------------------------------------------------------------------------------'

    Description: This class represents a hash table with chaining implementation, allowing
                 the storage of key-value pairs. In cases of hash collisions, the colliding
                 items are stored in a linked list.
    Methods:
        1. __init__: Initializes the hash table with an initial capacity.
        2. print_table: Prints the hash table.
        3. insert: Inserts an item into the hash table.
        4. search: Searches for an item based on the key.
        5. remove: Removes an item from the hash table based on the key.

    Time Complexity:
        - __init__: O(n).
        - print_table: O(n + m).
        - insert: O(1) average and O(n) worst case.
        - search: O(1) average and O(n) worst case.
        - remove: O(1) average and O(n) worst case.

    Attributes:
    table : a list of lists that will be used to store the keys and values of the hash table

    """

    def __init__(self, init_capacity=40):
        """
        Constructs all the necessary attributes for the hash table object.
        """
        # Initialize an empty list to hold the hash table's buckets
        self.table = []
        # Create a number of empty buckets equal to the initial capacity
        for i in range(init_capacity):
            self.table.append([])

    def print_table(self):
        """
        Prints the hash table.
        """
        # Print the header for the hash table
        print(f"\n\n{Colors.BOLD}{Colors.ORANGE}Hash Table"
              f"\n——————————————————————————————————————————————————————————————————————————————————————————————————————"
              f"————————————————————————————————————————————————————————————————————————————————————————————————————————{Colors.END}")

        # Iterate over each bucket in the hash table
        for i in range(len(self.table)):
            bucket = self.table[i]
            if bucket:  # Only print the bucket if it's not empty
                print(", ".join(str(key_value[1]) for key_value in bucket))

    def insert(self, key, item):
        """
        Inserts a key-value pair into the hash table.
        """
        # Calculate the bucket index by hashing the key and taking the modulus of the hash table's length
        bucket = hash(key) % len(self.table)
        # Get the bucket list at the calculated index
        bucket_list = self.table[bucket]
        # Check if the key already exists in the bucket list
        for key_value in bucket_list:
            if key_value[0] == key:
                # If the key exists, update its value and return True
                key_value[1] = item
                return True
        # If the key does not exist, append a new key-value pair to the bucket list and return True
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    def search(self, key):
        """
        Searches for a key in the hash table and returns its corresponding value.
        """
        # Calculate the bucket index by hashing the key and taking the modulus of the hash table's length
        bucket = hash(key) % len(self.table)
        # Get the bucket list at the calculated index
        bucket_list = self.table[bucket]
        # Check if the key exists in the bucket list
        for key_value in bucket_list:
            if key_value[0] == key:
                # If the key exists, return its value
                return key_value[1]
        # If the key does not exist, return None
        return None

    def remove(self, key):
        """
        Removes a key and its corresponding value from the hash table.
        """
        # Calculate the bucket index by hashing the key and taking the modulus of the hash table's length
        bucket = hash(key) % len(self.table)
        # Get the bucket list at the calculated index
        bucket_list = self.table[bucket]
        # Check if the key exists in the bucket list
        for key_value in bucket_list:
            if key_value[0] == key:
                # If the key exists, remove the key-value pair from the bucket list and return True
                bucket_list.remove(key_value)
                return True
        # If the key does not exist, return False
        return False


# Initialize HashTable
packageHash = ChainingHashTable()


class Packages:
    """
    A class used to represent a Package.

    Time Complexity: O(n) - O(1)
    Constructor and Basic Operations: O(1)
    Batch Operations: O(n)

    Methods:
    - __init__(): Constructs all the necessary attributes for the package object.
    - __str__(): Returns a string representation of the package.
    - Status_update(time_change): Updates the status of the package based on the current time.
    """

    def __init__(self, ID, street, city, state, zip, deadline, weight, notes, status='At Hub', departureTime=None,
                 deliveryTime=None, truckID=None):
        """
        Constructs all the necessary attributes for the package object.
        """
        self.deliveryTime = deliveryTime
        self.departureTime = departureTime
        self.ID = ID
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = status
        self.truckID = truckID

    def __str__(self):
        """
        Returns a string representation of the package.

        Returns:
        str : a string representation of the package
        """
        return (
                f"{Colors.BOLD_ORANGE}ID:{Colors.END} %s \t "
                f"{Colors.BOLD_ORANGE}Address:{Colors.END} %-20s \t "
                f"{Colors.BOLD_ORANGE}City:{Colors.END} %s \t "
                f"{Colors.BOLD_ORANGE}State:{Colors.END} %s \t "
                f"{Colors.BOLD_ORANGE}Zip:{Colors.END} %s \t "
                f"{Colors.BOLD_ORANGE}Deadline:{Colors.END} %s \t "
                f"{Colors.BOLD_ORANGE}Weight:{Colors.END} %s \t "
                f"{Colors.BOLD_ORANGE}Status:{Colors.END} %s \t "
                f"{Colors.BOLD_ORANGE}Departure Time:{Colors.END} %s \t "
                f"{Colors.BOLD_ORANGE}Delivery Time:{Colors.END} %s" %
                (self.ID, self.street, self.city, self.state, self.zip, self.deadline, self.weight, self.status,
                 self.departureTime, self.deliveryTime))

    def status_update(self, time_change):
        """
        This method updates the status of a package based on the current time.

        Parameters:
        time_change : The current time.
        """
        # If the delivery time of the package is None, set the status to "At the hub"
        if self.deliveryTime is None:
            self.status = "At the hub"
        # If the current time is before the departure time of the package, set the status to "At the hub"
        elif time_change < self.departureTime:
            self.status = "At the hub"
        # If the current time is before the delivery time of the package, set the status to "En route"
        elif time_change < self.deliveryTime:
            self.status = "En route"
        # If the current time is after the delivery time of the package, set the status to "Delivered"
        else:
            self.status = "Delivered"
        # If the package ID is 9, update the street and zip code based on the current time
        if self.ID == 9:
            if time_change > datetime.timedelta(hours=10, minutes=20):
                self.street = "410 S State St"
                self.zip = "84111"
            else:
                self.street = "300 State St"
                self.zip = "84103"


# Load CSV data
# AddressCSV is a list of lists where each sublist represents a row in the CSV file
address_csv = list(csv.reader(open("./data/addressCSV.csv")))
# DistanceCSV is a list of lists where each sublist represents a row in the CSV file
distance_csv = list(csv.reader(open("./data/distanceCSV.csv")))


def load_package_data(filename):
    """
    This function loads package data from a CSV file and stores it in a hash table.

    Time Complexity: O(n)

    Parameters:
    filename : The name of the CSV file containing the package data.
    """
    # Open the CSV file
    with open(filename) as packages:
        # Create a CSV reader object
        packageInfo = csv.reader(packages, delimiter=',')
        # Skip the header row
        next(packageInfo)
        # Iterate over each row in the CSV file
        for package in packageInfo:
            # Extract the package details from the row
            pID = int(package[0])
            pStreet = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pNotes = package[7]
            pStatus = "At the Hub"
            # Create a Packages object with the extracted details
            p = Packages(pID, pStreet, pCity, pState, pZip, pDeadline, pWeight, pNotes, pStatus)
            # Insert the Packages an object into the hash table
            packageHash.insert(pID, p)


# Load package data
load_package_data('./data/packageCSV.csv')


class Trucks:
    """
    A class used to represent a Truck.

    Time Complexity: O(1) - Constant time complexity.

    Attributes:
    speed : The speed of the truck in miles per hour.
    miles : The total miles that the truck has traveled.
    current_location : The current location of the truck.
    time : The current time for the truck.
    depart_time : The departure time of the truck from the hub.
    packages : The list of package IDs that the truck is carrying.

    Methods:
    __init__(self, speed, miles, currentLocation, departTime, packages):
        Constructs all the necessary attributes for the truck object.
    """

    def __init__(self, speed, miles, currentLocation, departTime, packages):
        """
        Constructs all the necessary attributes for the truck object.
        """
        self.speed = speed
        self.miles = miles
        self.current_location = currentLocation
        self.time = departTime
        self.depart_time = departTime
        self.packages = packages


def assign_packages_to_truck(truck, truck_id):
    """
    This function assigns a truck ID to each package loaded on the truck.
    It also updates the package in the hash table to reflect the new truck ID assignment.

    Time Complexity: O(n)

    Parameters:
    truck : The truck object that is delivering the packages.
    truck_id : The ID of the truck.
    """
    # Iterate over each package in the truck's packages
    for package_id in truck.packages:
        # Search for the package in the hash table using the package ID
        package = packageHash.search(package_id)
        # If the package is found, assign the truck ID to the package
        if package:
            package.truckID = truck_id  # Assign the truck ID to the package
            # Update the package in the hash table to reflect the new truck ID assignment
            packageHash.insert(package_id, package)


def addresses(address):
    """
    This function finds the index of a given address in a global 2D list.

    Time Complexity: O(1) Best Case, O(n x m) Worst Case

    Parameters:
    address : The address to be searched for in the global 2D list.

    Returns:
    The index of the address in the global 2D list. If the address is not found, it returns None.
    """
    # Iterate over each row in the global 2D list
    for row in address_csv:
        # If the address is found in the row, return its index
        if address in row[2]:
            return int(row[0])
    # If the address is not found in any row, the function returns None
    return None


def distance_between(addy1, addy2):
    """
    This function calculates the distance between two addresses based on the address IDs. It
    retrieves the distance from the distanceCSV list using the address IDs as indices. If the
    distance is empty, it retrieves the distance from the reverse direction. It returns the
    distance as a float.

    Time Complexity: O(1)
    This function calculates the distance between two addresses based on their indices in a global 2D list.

    Parameters:
    addy1 : The index of the first address in the global 2D list.
    addy2 : The index of the second address in the global 2D list.

    Returns:
    float : The distance between the two addresses. If the distance is not found in the global 2D list, it returns 0.0.
    """

    # Try to get the distance from the global 2D list using addy1 and addy2 as indices
    distance = distance_csv[addy1][addy2]

    # If the distance is not found (i.e., if the corresponding element in DistanceCSV is an empty string),
    # try to get the distance using addy2 and addy1 as indices
    if distance == '':
        distance = distance_csv[addy2][addy1]

    # Return the distance as a float
    return float(distance)


def truck_deliver_packages(truck, truck_num):
    """
    ,------------------------------------------------------------------------------------------------,
    |                                TRUCK DELIVERY ALGORITHM FUNCTION                               |
    |                                     Time Complexity: O(n^2)                                    |
    '------------------------------------------------------------------------------------------------'

    Description: This function simulates the delivery process for a truck. It takes a truck object and
                    truck number as input. It initializes an empty list for en route packages and an
                    empty list for status logs. It adds the packages from the truck object to the in_transit
                    list. It then enters a loop until all packages are delivered. In each iteration, it
                    finds the next package to deliver based on the current location and the distance to
                    each package's street address. It updates the status logs and truck attributes
                    accordingly. Once all packages are delivered, it calculates the distance to return to
                    the hub and updates the status logs and truck attributes. It returns the status logs.

    Parameters:
    truck : The truck object that is delivering the packages.
    truck_num : The number of the truck.

    Returns:
    A list of status logs for the truck.
    """

    # Initialize a list to hold the packages that are in transit
    in_transit = []

    # Initialize a list to hold the status logs for the truck
    status_logs = []

    # Add a header to the status_logs
    header = f"{Colors.BOLD}{Colors.LIGHT_ORANGE}Truck\tStatus\t\tTime\t\t\t\tMiles\t\tAddress or Package #{Colors.END}"
    status_logs.append(header)

    # Move all packages from the truck to the in_transit list
    for packageID in truck.packages:
        package = packageHash.search(packageID)
        in_transit.append(package)
    truck.packages.clear()

    # While there are packages in transit, deliver the packages
    while len(in_transit) > 0:
        nextAddy = 2000
        nextPackage = None
        for package in in_transit:
            if package.ID in [25, 6]:
                nextPackage = package
                nextAddy = distance_between(addresses(truck.current_location), addresses(package.street))
                break
            if distance_between(addresses(truck.current_location), addresses(package.street)) <= nextAddy:
                nextAddy = distance_between(addresses(truck.current_location), addresses(package.street))
                nextPackage = package

        # Calculate the time and log the status when the truck stops at the delivery location
        hours = int(truck.time.total_seconds() // 3600)
        minutes = int((truck.time.total_seconds() % 3600) // 60)
        seconds = int(truck.time.total_seconds() % 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        statusStops = (f"  {Colors.BOLD}{Colors.BRIGHT_WHITE}{truck_num}{Colors.YELLOW}  \tStopped"
                       f"{Colors.END}  \t{Colors.BOLD}{time_str:<20}{Colors.END}"
                       f"{truck.miles:<10.1f}  {nextPackage.street:<30}{Colors.END}")
        status_logs.append(statusStops)

        # Deliver the package and update the truck's location, time, and miles
        truck.packages.append(nextPackage.ID)
        in_transit.remove(nextPackage)
        truck.miles += nextAddy
        truck.current_location = nextPackage.street
        truck.time += datetime.timedelta(hours=nextAddy / 18)
        nextPackage.deliveryTime = truck.time
        nextPackage.departureTime = truck.depart_time

        # Log the status when the package is delivered
        statusDelivered = (f"  {Colors.BOLD}{Colors.BRIGHT_WHITE}{truck_num}{Colors.END}  "
                           f"\t{Colors.GREEN}{Colors.BOLD}Delivered{Colors.END}  "
                           f"\t{Colors.BOLD}{time_str:<20}{Colors.END}"
                           f"\t\t\tPackage {nextPackage.ID:<10}{Colors.END}")
        status_logs.append(statusDelivered)

    # Calculate the return distance and time, and update the truck's miles and time
    return_distance = distance_between(addresses(truck.current_location), addresses("4001 South 700 East"))
    truck.miles += return_distance
    truck.time += datetime.timedelta(hours=return_distance / 18)

    # Calculate the time and log the status when the truck arrives back at the hub
    hours = int(truck.time.total_seconds() // 3600)
    minutes = int((truck.time.total_seconds() % 3600) // 60)
    seconds = int(truck.time.total_seconds() % 60)
    time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    statusHub = (f"  {Colors.BOLD}{Colors.BRIGHT_WHITE}{truck_num}{Colors.LIGHT_RED}  \tReturn"
                 f"{Colors.END}  \t{Colors.BOLD}{time_str:<20}{Colors.END}"
                 f"{truck.miles:<10.1f}  4001 South 700 East (hub){Colors.END}\n\n\n")
    status_logs.append(statusHub)

    # Return the status logs for the truck
    return status_logs


'''
     ,------------------------------------------------------------------------------------------------,
     |                                     USER INTERFACE SECTION                                     |
     |                            UI / UX Design and Program Initialization                           |
     '------------------------------------------------------------------------------------------------' 
'''


def format_datetime(dt):
    """
    This function takes a datetime object or a timedelta object and returns a formatted string representation of it.
    If the input is None, it returns a placeholder string "N/A".
    If the input is not a datetime or timedelta object, it returns a string "Invalid type".

    Time Complexity: O(1) - Constant time complexity.

    Parameters:
    dt : datetime.datetime or datetime.timedelta or None
        The datetime or timedelta object to be formatted.

    Returns:
    str
        A formatted string representation of the datetime or timedelta object, or a placeholder string if the input is None, or a string "Invalid type" if the input is not a datetime or timedelta object.
    """
    if dt is None:
        return "N/A"
    elif isinstance(dt, datetime.datetime):
        # Format the datetime object as a string in the format 'YYYY-MM-DD HH:MM:SS'
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(dt, datetime.timedelta):
        # Convert the timedelta object to a string in the format 'HH:MM:SS'
        return str(dt)
    else:
        return "Invalid type"


def print_headers_once(column_widths, parameters, printed_headers):
    """
    This function prints the headers for the package details table, but only once.
    It checks if the headers have been printed before, and if not, it prints them and marks them as printed.

    Time Complexity: O(n) - Constant time complexity.

    Parameters:
    column_widths : A dictionary mapping each parameter to its column width.
    parameters : A list of parameters for which headers are to be printed.
    printed_headers : A list used to track if headers have been printed. If the list is empty, headers are printed.
    """
    # Check if headers have been printed before
    if not printed_headers:
        # Define the headers with appropriate formatting
        headers = {
            'ID': f'\n\n\n\n {Colors.BOLD}{Colors.ORANGE}ID',
            'Address': '\t\tAddress',
            'City': '\tCity',
            'State': '\tState',
            'Zip Code': '\tZip Code',
            'Deadline': '\tDeadline',
            'Weight': '\tWeight',
            'Status': '\t\tStatus',
            'Truck ID': '\tTruck',
            'Departure Time': '\tDeparted',
            'Delivery Time': '\tDelivered'
        }
        # Create a row of headers with appropriate spacing
        header_row = "".join(headers[param].ljust(column_widths[param]) for param in parameters)
        # Print the row of headers
        print(header_row)
        # Print a line of dashes under the headers
        print("—" * sum(column_widths.values()))
        # Mark headers as printed
        printed_headers.append(True)


def print_package_details(package, detail='all', printed_headers=None, detail_titles=None):
    """
    This function prints the details of a package. The details include the package's ID, address, city, state, zip code,
    deadline, weight, status, departure time, delivery time, and truck ID. The user can choose to view a specific detail
    or all details. The details are printed in a tabular format with headers.

    Time Complexity: O(1) - O(n)

    Parameters:
    package : The package object whose details are to be printed.
    detail : The specific detail to be printed. If 'all', all details are printed. (default is 'all')
    printed_headers : A list used to track if headers have been printed. If the list is empty, headers are printed. (default is None)
    detail_titles : A dictionary mapping detail codes to detail titles. (default is None)
    """
    # Check if printed_headers is None, if so, initialize it as an empty list
    if printed_headers is None:
        printed_headers = []
    # Check if detail_titles is None, if so, initialize it with default values
    if detail_titles is None:
        detail_titles = {
            'a': 'Address',
            'b': 'City',
            'c': 'Zip Code',
            'd': 'State',
            'e': 'Deadline',
            'f': 'Weight',
            'g': 'Status',
            'h': 'Departure Time',
            'i': 'Delivery Time',
            'j': 'Truck ID',
            'k': 'All'
        }

    # Define package details with conditional styling for the 'Status'
    # If the status is "Delivered", it will be displayed in green, if it's "En route", it will be displayed in yellow
    status_styling = {
        "At the hub": f"\t{Colors.BOLD}{Colors.LIGHT_RED}Central Hub{Colors.END}",
        "Delivered": f"\t{Colors.BOLD}{Colors.LIGHT_GREEN}{package.status}{Colors.END}",
        "En route": f"\t{Colors.BOLD}{Colors.LIGHT_YELLOW}{package.status}{Colors.END}",
    }
    status = status_styling.get(package.status, package.status)

    # Define the details dictionary with the package attributes
    # The values are formatted with appropriate padding and color for better readability
    # If the status is "En route", color the delivery time detail yellow
    delivery_time_styling = {
        "At the hub": f"\t\t\t{Colors.LIGHT_RED}{Colors.BOLD}{str(package.deliveryTime) if package.deliveryTime else 'N/A'}{Colors.END}",
        "Delivered": f"\t\t\t{Colors.BOLD}{Colors.LIGHT_GREEN}{str(package.deliveryTime) if package.deliveryTime else 'N/A'}{Colors.END}",
        "En route": f"\t\t\t{Colors.LIGHT_YELLOW}{Colors.BOLD}{str(package.deliveryTime) if package.deliveryTime else 'N/A'}{Colors.END}",
    }
    delivery_time = delivery_time_styling.get(package.status,
                                              f"\t\t\t{Colors.BOLD}{str(package.deliveryTime) if package.deliveryTime else 'N/A'}{Colors.END}")

    # Add an additional tab if the length of the delivery time string is less than or equal to time length and the status is either "En route" or "At the hub"
    if len(str(package.deliveryTime)) <= len("0:00:00") and (
            package.status == "En route" or package.status == "At the hub" or package.status == "Delivered"):
        delivery_time = f"{delivery_time}\t"

    # Define truck ID details with conditional styling
    # If the truck ID is None, it will be displayed in red, otherwise, it will be displayed in different colors based on its value
    truck_id_styling = {
        1: f"\t\t\t{Colors.BOLD}{Colors.LIGHT_ORANGE}{str(package.truckID)}{Colors.END}",
        2: f"\t\t\t{Colors.BOLD}{Colors.LIGHT_BLUE}{str(package.truckID)}{Colors.END}",
        3: f"\t\t\t{Colors.BOLD}{Colors.LIGHT_PURPLE}{str(package.truckID)}{Colors.END}",
    }
    truck_id = truck_id_styling.get(package.truckID, f"\t\t\t{Colors.BOLD}{Colors.LIGHT_RED}N/A{Colors.END}")

    # Define the details dictionary with the package attributes
    # The values are formatted with appropriate padding and color for better readability
    details = {
        'ID': f" {Colors.BOLD}{Colors.BRIGHT_WHITE}{str(package.ID)}{Colors.END}",
        'Address': f"\t\t{package.street}",
        'City': f"\t{package.city}",
        'State': f"\t{package.state}",
        'Zip Code': f"\t{package.zip}",
        'Deadline': f"\t{package.deadline}",
        'Weight': f"\t{str(package.weight)}kg",
        'Status': f"\t{status}",
        'Departure Time': f"\t\t{Colors.BOLD}{str(package.departureTime) if package.departureTime else 'N/A'}{Colors.END}",
        'Delivery Time': delivery_time,
        'Truck ID': truck_id
    }

    # Define the column widths for each parameter
    column_widths = {
        'ID': 10,
        'Address': 50,
        'City': 20,
        'State': 5,
        'Zip Code': 10,
        'Deadline': 10,
        'Weight': 7,
        'Status': 15,
        'Departure Time': 20,
        'Delivery Time': 20,
        'Truck ID': 40
    }

    # Define the column widths for selected details
    selected_details_column_widths = {
        'ID': 10,
        'Address': 35,
        'City': 35,
        'State': 35,
        'Zip Code': 35,
        'Deadline': 35,
        'Weight': 35,
        'Status': 35,
        'Departure Time': 35,
        'Delivery Time': 35,
        'Truck ID': 35
    }

    # Define the parameter list
    parameters = ['ID', 'Address', 'City', 'State', 'Zip Code', 'Deadline', 'Weight', 'Status', 'Departure Time',
                  'Delivery Time', 'Truck ID']

    # If the detail is 'k', print all details
    if detail == 'k':
        print_headers_once(column_widths, parameters, printed_headers)  # Print headers if not yet printed
        value_row = "".join(details[param].ljust(column_widths[param]) for param in parameters)
        print(value_row)
    else:
        # If the detail is not 'k', print only the selected detail
        if not printed_headers:
            header_id = "ID".ljust(selected_details_column_widths['ID'])
            header_detail = detail_titles[detail].ljust(selected_details_column_widths[detail_titles[detail]])
            header = f"{Colors.BOLD}{Colors.ORANGE}\n\n\n{header_id}\t\t\t{header_detail}"
            print(header)
            print(f"{Colors.BOLD}{Colors.ORANGE}—" * (
                    selected_details_column_widths['ID'] + selected_details_column_widths[detail_titles[detail]]))
            printed_headers.append(True)

        # Format the detail value and print it
        detail_value = "{:<{}}".format(details[detail_titles[detail]],
                                       selected_details_column_widths[detail_titles[detail]])
        print(
            f"{Colors.BOLD}{Colors.BRIGHT_WHITE}Package #{str(package.ID).ljust(selected_details_column_widths['ID'])}{Colors.END}"
            f"{detail_value}")


def get_user_input(prompt, validation_func, error_message):
    """
    This function prompts the user for input, validates the input, and returns it.

    Time Complexity: O(1) - Constant time complexity.

    Parameters:
    prompt : The message displayed to the user when asking for input.
    validation_func : A function that takes a string and returns a boolean. This function is used to validate the user's input.
    error_message : The message displayed to the user when their input is invalid.

    Returns:
    The user's input if it is valid. If the user's input is invalid, the function will continue to ask for input until valid input is provided.
    """
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        else:
            print(error_message)


def lookup_package_status():
    """
    This function allows the user to look up the status of packages at a specific time.
    The user can choose to view the status of a specific package or all packages.
    The user can also choose to view a specific detail of the package(s) or all details.
    The details include the package's address, city, zip code, state, deadline, weight,
    status, departure time, delivery time, and truck ID.

    Time Complexity: O(n)

    Returns:
    None
    """

    # Ask the user to input the time in 24-hour format to view the package statuses for.
    # The input is validated using a regular expression to ensure it matches the HH:MM format.
    user_time_str = get_user_input(
        f"\n{Colors.BOLD}{Colors.ORANGE}Please input the time in 24-hour [HH:MM] format you wish to "
        f"view the package statuses for, e.g., enter 14:30 for 2:30 PM:{Colors.END} \n> ",
        lambda x: re.match(r'^([01]\d|2[0-3]):([0-5]\d)$', x),
        f"{Colors.BOLD}{Colors.LIGHT_RED}Invalid time format. Please try again.{Colors.END}"
    )
    # Convert the user input time to a datetime.timedelta object
    (h, m) = map(int, user_time_str.split(":"))
    time_change = datetime.timedelta(hours=h, minutes=m)

    # Ask the user to enter the package ID they wish to view, or press Enter to view all packages.
    # The input is validated to ensure it is either empty or a valid package ID (1-40).
    package_id_input = get_user_input(
        f"\n\n{Colors.BOLD}{Colors.ORANGE}Please enter the package ID you wish to view, "
        f"or press Enter to view all packages: {Colors.END}\n> ",
        lambda x: x == '' or (x.isdigit() and 1 <= int(x) <= 40),
        f"{Colors.BOLD}{Colors.LIGHT_RED}Invalid package ID. Please try again.{Colors.END}"
    )
    # Convert the user input package ID to an integer, or get a list of all 40 package IDs if the user input is empty
    package_ids = [int(package_id_input)] if package_id_input else range(1, 41)

    # Ask the user to select the parameter they want to view.
    # The input is validated to ensure it is a valid option (a-j or k for all).
    detail_input = get_user_input(
        f"\n\n{Colors.BOLD}{Colors.ORANGE}Select the parameter you want to view:{Colors.END}\n"
        f"{Colors.BOLD}{Colors.BRIGHT_WHITE}a{Colors.END} - Address\n"
        f"{Colors.BOLD}{Colors.BRIGHT_WHITE}b{Colors.END} - City\n"
        f"{Colors.BOLD}{Colors.BRIGHT_WHITE}c{Colors.END} - Zip Code\n"
        f"{Colors.BOLD}{Colors.BRIGHT_WHITE}d{Colors.END} - State\n"
        f"{Colors.BOLD}{Colors.BRIGHT_WHITE}e{Colors.END} - Deadline\n"
        f"{Colors.BOLD}{Colors.BRIGHT_WHITE}f{Colors.END} - Weight\n"
        f"{Colors.BOLD}{Colors.BRIGHT_WHITE}g{Colors.END} - Status\n"
        f"{Colors.BOLD}{Colors.BRIGHT_WHITE}h{Colors.END} - Departure Time\n"
        f"{Colors.BOLD}{Colors.BRIGHT_WHITE}i{Colors.END} - Delivery Time\n"
        f"{Colors.BOLD}{Colors.BRIGHT_WHITE}j{Colors.END} - Truck ID\n"
        f"{Colors.BOLD}{Colors.BRIGHT_WHITE}k{Colors.END} - All\n> ",
        lambda x: x in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'],
        f"{Colors.BOLD}{Colors.LIGHT_RED}Invalid option. Please try again.{Colors.END}"
    )

    # Initialize an empty list to track if headers have been printed
    printed_headers = []

    # For each package ID, get the package from the hash table, update its status, and print its details
    for package_id in package_ids:
        package = packageHash.search(package_id)
        if package:
            package.status_update(time_change)
            print_package_details(package, detail=detail_input, printed_headers=printed_headers)


def main():
    """
     ,------------------------------------------------------------------------------------------------,
     |                                        MAIN FUNCTION                                           |
     |                                 Time Complexity: O(1) - O(n)                                   |
     '------------------------------------------------------------------------------------------------'

    1. Prints the title of the program.
     a. Prints the hash table of packages before the delivery simulation. (optional)
    2. Initializes three truck objects with specific attributes such as speed, miles, current location, departure time, and a list of package IDs.
    3. Initializes status logs for each truck by calling the `truckDeliverPackages` function.
    4. Assigns truck IDs to each package loaded on the truck.
    5. Calculates the corrected total time in hours.
    6. Calculates the total distance and total packages delivered.
    7. Prints the total metrics including total distance, total time spent, and total packages delivered.
    8. Enters a main program loop which provides a user interface for starting the delivery simulation, looking up package status, and quitting the program.

    The delivery simulation includes the following steps:
    - Prints the beginning of the delivery simulation.
    - Prints the delivery logs for each truck which includes the status of each stop, the status of each delivered package, and the status when the truck arrives back at the hub.
    - Prints a message indicating the completion of the delivery for all trucks.
    - Calculates the corrected total time in hours.
    - Calculates the total distance and total packages delivered.
    - Prints the total metrics including total distance, total time spent, and total packages delivered.

    The package status lookup includes the following steps:
    - Asks the user to input the time in 24-hour format to view the package statuses for.
    - Asks the user to enter the package ID they wish to view, or press Enter to view all packages.
    - Asks the user to select the parameter they want to view.
    - Prints the selected details of the package(s) at the specified time.

    If the user chooses to quit, the program will exit.
    """
    # Print the program title and author information
    print(f"{Colors.END}{Colors.BOLD_ORANGE}\n\nWestern Governors University Parcel Service{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BRIGHT_WHITE}C950 - Data Structures and Algorithms II{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BRIGHT_WHITE}Author:{Colors.END} Aaron Ballesteros")
    print(f"{Colors.BOLD}{Colors.BRIGHT_WHITE}Student ID:{Colors.END} 011019047")

    '''
    Uncomment to print the hash table of packages before the delivery simulation
    '''
    # packageHash.print_table()

    # Initialize each truck and load the packages onto the trucks with their respective package IDs and departure times.
    # Truck 1 is designated for early departure without any delayed packages. It focuses on packages with specific group requirements and those that can be delivered earliest in the morning.
    truck1 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=8),
                    # Grouped packages: Ensuring packages #14, #15, #16, #19, #20, and #13 are together as required.
                    # Package #37 is included for optimal route planning, and #38 and #36 are specific to Truck 2 but are adjusted here for illustrative purposes.
                    [1, 29, 7, 30, 8, 34, 40, 14, 15, 16, 19, 20, 13, 37, 38, 36])

    # Truck 2 departs after 9:05 AM to accommodate delayed packages. It carries packages with specific time constraints and those designated for Truck 2.
    truck2 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=9, minutes=5),
                    # Delayed packages: #6, #28, #32, #33 are not available until 9:05 AM.
                    # Truck-specific packages: #3, #18 as required.
                    # Package #9: Included here to be delivered after the address correction at 10:20 AM.
                    # Remaining packages fill the truck for efficiency and to ensure delivery within deadlines.
                    [3, 18, 6, 28, 32, 33, 25, 12, 9, 22, 24, 11, 10, 5, 4, 21])

    # Truck 3 is used for the remaining packages, ensuring no overloading and compliance with delivery deadlines. Includes the package needing address correction.
    truck3 = Trucks(18, 0.0, "4001 South 700 East", datetime.timedelta(hours=11),
                    # This truck fills with the remaining packages to ensure all packages are allocated and delivered.
                    [2, 17, 23, 26, 27, 31, 35, 39])

    # Initialize status logs for each truck
    status_logs_truck1 = truck_deliver_packages(truck1, 1)
    truck2.depart_time = min(truck1.time, truck2.time)
    status_logs_truck2 = truck_deliver_packages(truck2, 2)
    status_logs_truck3 = truck_deliver_packages(truck3, 3)

    # Assign truck IDs after initializing trucks and before the delivery simulation
    assign_packages_to_truck(truck1, 1)
    assign_packages_to_truck(truck2, 2)
    assign_packages_to_truck(truck3, 3)

    # Calculate and display total metrics immediately after simulation
    total_time_corrected = sum(
        (truck.time.total_seconds() - truck.depart_time.total_seconds()) for truck in [truck1, truck2, truck3]) / 3600
    total_distance = sum(truck.miles for truck in [truck1, truck2, truck3])
    total_packages_delivered = sum(len(truck.packages) for truck in [truck1, truck2, truck3])

    # Print total metrics of all trucks after the delivery simulation
    print(f"\n\n{Colors.BOLD_ORANGE}Total Delivery Metrics:{Colors.END}")
    print(f"Total Distance: {Colors.BRIGHT_WHITE}{Colors.BOLD}{total_distance:.1f} miles{Colors.END}")
    print(f"Total Time Spent: {Colors.BRIGHT_WHITE}{Colors.BOLD}{total_time_corrected:.2f} hours{Colors.END}")
    print(f"Total Packages Delivered: {Colors.BRIGHT_WHITE}{Colors.BOLD}{total_packages_delivered}{Colors.END}")

    # Main program loop
    while True:
        # Display the menu to the user and get the user's choice
        user_choice = input(
            f"\n\n\n{Colors.BOLD_ORANGE}What would you like to do?{Colors.END}"
            f"\n\t{Colors.BOLD}{Colors.BRIGHT_WHITE}d{Colors.END} - Begin Delivery Simulation"
            f"\n\t{Colors.BOLD}{Colors.BRIGHT_WHITE}l{Colors.END} - Lookup Package Status"
            f"\n\t{Colors.BOLD}{Colors.BRIGHT_WHITE}q{Colors.END} - Quit\n> ")

        # If the user chooses to quit, exit the program
        if user_choice.lower() == 'q':
            break

        # If the user chooses to begin the delivery simulation
        elif user_choice.lower() == 'd':

            # Print a message indicating the beginning of the delivery simulation
            print(f"{Colors.BOLD}{Colors.LIGHT_YELLOW}\n\n\nBeginning delivery simulation...\n\n\n{Colors.END}")

            # Print Delivery Logs (statusStops, statusDelivered, statusHub)
            # for each truck with a delay of 1 second between each log
            time.sleep(1)
            print(log_truck_metrics_with_date(truck1, 1))
            print("\n".join(status_logs_truck1))
            time.sleep(1)  # Add a delay to simulate the delivery process
            print(log_truck_metrics_with_date(truck2, 2))
            print("\n".join(status_logs_truck2))
            time.sleep(1)  # Add a delay to simulate the delivery process
            print(log_truck_metrics_with_date(truck3, 3))
            print("\n".join(status_logs_truck3))

            # Print a message indicating the completion of the delivery for all trucks
            print(f"\n{Colors.BOLD}{Colors.LIGHT_GREEN}Delivery complete for all trucks!{Colors.END}\n")

            # Print total metrics after the delivery simulation
            time.sleep(1)
            print(f"\n\n{Colors.BOLD_ORANGE}Total metrics:\n"
                  f"———————————————————————————————————————————————{Colors.END}")
            print(f"Total Distance: {total_distance:.1f} miles")
            print(f"Total Time Spent: {total_time_corrected:.2f} hours")
            print("Total Packages Delivered: ", total_packages_delivered)

        # If the user chooses to look up package status
        elif user_choice.lower() == 'l':
            lookup_package_status()
        else:
            # If the user enters an invalid choice, display an error message
            print(f"{Colors.BOLD}{Colors.LIGHT_RED}Invalid choice. Please try again.{Colors.END}")


if __name__ == "__main__":
    main()
