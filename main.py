import xml.etree.ElementTree as xml
import csv


''' 
METROPOLIS OSM Parser
Author: Lucas Hornung
A tool used to convert an OpenStreetMap OSM file into multiple files that can be used with the METROPOLIS dynamic traffic simulator
'''

class Parser:

    def __init__(self):
        print("Hello world")

#OSM file parser
def osm_parse(path, crossings_path, links_path):
    f = xml.parse(path).getroot()
    count = 0

    for i in f:


        if i.tag == "node":
            write_node(i, crossings_path)

            count += 1

        if i.tag == "way":
            write_way(i, links_path)

            count += 1

    return count

#Writes node to tsv file
def write_node(element, tsv_writer):
    if element.tag != "node":
        return
    else:
        id = element.attrib['id']

        name = element.attrib['id']
        #Parse through node tags
        for sub in element:
            if sub.tag == "tag" and (sub.attrib['k'] == "name" or sub.attrib['k'] == 'addr:street'):

                name = sub.attrib['v']
                break



        # TODO: change coordinates to relative coordinates
        x = element.attrib['lon']
        y = element.attrib['lat']

        tsv_writer.writerow([id, name, x, y])
        return

#Writes way to tsv file
def write_way(element, tsv_writer):
    if element.tag != "way":
        return
    else:
        id = element.attrib['id']

        # TODO: change name to actual name
        name = element.attrib['id']

        OD_list = []
        #TODO: Estimate speed if not provided
        speed = 50
        oneway = False
        #TODO: Determine which funtion to use
        function = 1
        #TODO: Estimate number of lanes
        lanes = 1

        for sub in element:
            if sub.tag == "nd":
                OD_list.append(sub.attrib['ref'])

            if sub.tag == "tag":
                if sub.attrib['k'] == 'maxspeed':
                    speed = sub.attrib['v']

                elif sub.attrib['k'] == 'oneway' and sub.attrib['v'] == 'yes':
                    oneway = True

        node_count = 0

        for i in range(len(OD_list)-1):

            new_id = int(id, 10) * 1000 + node_count

            #Link: ['id', 'name', 'lanes', 'speed', 'capacity', 'function', 'origin', 'destination']
            links_writer.writerow(
                [new_id, name, lanes, speed, ' ', function, OD_list[i], OD_list[i+1]])

            node_count+=1

            if node_count > 999:
                break


        return

if __name__ == '__main__':
    pars = Parser()

    with open('crossings.tsv', 'wt') as crossings_file :
        with open('links.tsv', 'wt') as links_file:
            crossings_writer = csv.writer(crossings_file, delimiter='\t')
            crossings_writer.writerow(['id', 'name', 'x', 'y'])

            links_writer = csv.writer(links_file, delimiter='\t')
            links_writer.writerow(['id', 'name', 'lanes', 'speed', 'capacity', 'function', 'origin', 'destination'])

            osm = osm_parse('map(2).osm', crossings_writer, links_writer)
