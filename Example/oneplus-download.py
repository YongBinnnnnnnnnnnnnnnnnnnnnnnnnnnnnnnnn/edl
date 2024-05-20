#!/bin/env python3
import inspect
import re
import types
import xml.etree.ElementTree as ET
from typing import cast

def __FUNCTION__():
  return cast(types.FrameType, inspect.currentframe()).f_back.f_code.co_name

def handle_SAHARA(node):
  handlers = {
  }
  for child in node:
    if child.tag in handlers:
      handlers[child.tag]()
    else:
      print(f"{__FUNCTION__()}: Unsupported tag '{child.tag}'")
  

def handle_root(node):
  handlers = {
    re.compile("BasicInfo"): lambda child: print(child.tag, child.attrib),
    re.compile("SAHARA"): handle_SAHARA,
    re.compile("MEMORY_SIZE"): lambda x: None
  }
  for child in node:
    supported = False
    for tag_regex, handler in handlers.items():    
      if tag_regex.fullmatch(child.tag):
        handler(child)
        supported = True
    if not supported:
      print(f"{__FUNCTION__()}: Unsupported tag '{child.tag}'")


tree = ET.parse('settings.xml')
root = tree.getroot()
assert root.tag == 'Setting'
handle_root(root)
