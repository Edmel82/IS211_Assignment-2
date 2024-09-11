
import argparse
import urllib.request
import logging
import datetime


#This function should let you enter an url and return it later.
def downloadData(url):
    with urllib.request.urlopen(url) as response:
        web_data = response.read().decode('utf-8')

    return web_data

#This function should process the data from the url and convert it to an object.
def processData(filecontent):
    person_dict = {}
    for data_line in filecontent.split("\n"):
        if len(data_line) == 0:
            continue

        identifier, name, birthday = data_line.split(",")
        if identifier == "id":
            continue

        id_int = int(identifier)
        try:
            person_birthday = datetime.datetime.strptime(birthday, "%d/%m/%Y")
            person_dict[id_int] = (name, person_birthday)
        except ValueError as e:
            error_msg = "The ID provided could not be processed #{} for ID #{}.".format(data_line, id_int)
            logging.basicConfig(filename="error.log", level=logging.ERROR)
            logger = logging.getLogger("assignment2")
            logger.error(error_msg)

    return person_dict

#This function should take the input (id) and return name and birthday.
def displayPerson(id, personData):
    if id in personData:
        name = personData[id][0]
        birthdate = datetime.datetime.strftime(personData[id][1], "%Y-%m-%d")
        print(f"Person # {id} is {name} with a birthday of {birthdate}")
    else:
        print ("No user found with that ID")


def main(url):
    print(f"Please provide URL = {url}...")
    data = downloadData(url)
    results_dict = processData(data)


    while True:
        id = int(input("Please enter ID to lookup: "))
        if id <= 0:
           break
        else:
           displayPerson(id, results_dict)



if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
