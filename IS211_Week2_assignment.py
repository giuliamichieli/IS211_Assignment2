import sys, argparse
import logging, logging.handlers
import urllib.request as request
import csv
from datetime import *

logger = logging.getLogger("assignment2")
logger.setLevel(logging.ERROR)
file_handler = logging.FileHandler('errors.log')
formatter = logging.Formatter('%(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def downloadData(url):
    response = request.urlopen(url)
    return response.read().decode('utf-8').splitlines()

def processData(data):
    global logger
    data = csv.DictReader(data)
    persons = {}
    for row in data:
        id = int(row['id'])
        try:
            birthday = datetime.strptime(row['birthday'], '%d/%m/%Y').date()
            persons[id] = (row['name'],birthday)
        except:
            logger.error('Error processing line #%d for ID #%d' % (id+1,id))
    return persons

def displayPerson(id, personData):
    id = int(id)
    if id not in personData: return "No user found with that id"
    bd=personData[id][1]
    return 'Person '+str(id)+' is '+str(personData[id][0])+' with a birthday of '+str('%s/%s/%s' % (bd.year, str(bd.month).zfill(2), str(bd.day).zfill(2)))

def main(url):
    try:
        csvData = downloadData(url)
    except Exception as e:
        print ("Exception occured: ", e)
        sys.exit()
    personData = processData(csvData)

    getID = input('what id shall I lookup for you? (0, or less to quit) ')
    while getID.isdigit():
        if not(int(getID)):
            break
            sys.exit()
        a = displayPerson(getID, personData)
        print (a)
        getID = input('what id shall I lookup for you? (0, or less to quit) ')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--url',help='URL Required. Usage: python IS211_Week2_assignment.py --url URL_FOR_DATA')
    args = parser.parse_args()
    
    if args.url:
        url=args.url
        #if url.find('http://') < 0: url = 'http://' + url
        main(url)
    else:
        print ('URL Required. Usage: python IS211_Week2_assignment.py --url URL_FOR_DATA')