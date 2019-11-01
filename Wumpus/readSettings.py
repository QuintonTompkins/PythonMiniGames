#Author: Quinton Tompkins

import xml.etree.ElementTree as ET

def getDispWH(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    
    displaySettings = root.find('Display')
    h = int(displaySettings.get("height"))
    w = int(displaySettings.get('width'))
    
    return w , h