import xml.etree.ElementTree as xml
import csv


''' 
METROPOLIS OSM Parser
Author: Lucas Hornung
A tool used to convert an OpenStreetMap OSM file into multiple files that can be used with the METROPOLIS dynamic traffic simulator
'''

class OSM_Parser:
    crossings_file = None
    crossings_writer = None

    links_file = None
    links_writer = None

    osm_file = None



    def __init__(self, osm_file_path):
        print("Hello world")

        self.osm_file = osm_file_path

        self.crossings_file = open('crossings.tsv', 'wt')
        self.crossings_writer = csv.writer(self.crossings_file, delimiter='\t')
        self.crossings_writer.writerow(['id', 'name', 'x', 'y'])

        self.links_file = open('links.tsv', 'wt')
        self.links_writer = csv.writer(self.links_file, delimiter='\t')
        self.links_writer.writerow(
            ['id', 'name', 'lanes', 'speed', 'capacity', 'function', 'origin',
             'destination'])


    def parse_file(self):
        return self.osm_parse(self.osm_file, self.crossings_writer, self.links_writer)

    #OSM Parser
    def osm_parse(self, path, crossings_path, links_path):
        f = xml.parse(path).getroot()
        count = 0

        for i in f:
            if i.tag == "node":
                self.write_node(i, crossings_path)

                count += 1

            if i.tag == "way":
                self.write_way(i, links_path)

                count += 1

        return count

    #Writes node to tsv file
    def write_node(self, element, tsv_writer):
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
    def write_way(self, element, links_writer):
        if element.tag != "way":
            return
        else:
            # TODO: Generate a unique ID
            id = element.attrib['id']

            # TODO: change name to actual name
            name = element.attrib['id']

            OD_list = []
            #TODO: Estimate speed if not provided
            speed = 50
            oneway = False
            #TODO: Determine which function to use
            function = 1
            #TODO: Estimate number of lanes
            lanes = 1
            #TODO: Find capacity

            for sub in element:
                if sub.tag == "nd":
                    OD_list.append(sub.attrib['ref'])

                if sub.tag == "tag":
                    if sub.attrib['k'] == 'maxspeed':
                        speed = sub.attrib['v']

                    elif sub.attrib['k'] == 'oneway' and sub.attrib['v'] == 'yes':
                        oneway = True

                    elif sub.attrib['k'] == 'lanes':
                        lanes = sub.attrib['v']

                    elif  (sub.attrib['k'] == "name" or sub.attrib['k'] == 'addr:street'):
                        name = sub.attrib['v']

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
    pars = OSM_Parser('map(2).osm')

    print(' ')
    print("Total: " + str(pars.parse_file()) + " elements")
