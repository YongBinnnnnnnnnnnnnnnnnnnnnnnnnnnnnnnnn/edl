#!/bin/env python3
import xml.etree.ElementTree as ET
tree = ET.parse('settings.xml')
root = tree.getroot()
assert root.tag == 'Setting'
print(root.tag)
for child in root:
  if child.tag == "BasicInfo":
    print(child.tag, child.attrib)
