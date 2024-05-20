#!/bin/env python3
import hashlib
import inspect
import re
import types
import xml.etree.ElementTree as ET

from typing import cast


def sha256sum(filename):
  with open(filename, 'rb') as f:
    return hashlib.file_digest(f, 'sha256').hexdigest()

def __FUNCTION__():
  return cast(types.FrameType, inspect.currentframe()).f_back.f_code.co_name

info_ = {}

def save_info(key, value):
  global info_
  info_[key] = value
  
def handle_SAHARA(node):
  handlers = {
    "File": lambda x: save_info("loader", x.attrib['Path'])
  }
  for child in node:
    if child.tag in handlers:
      handlers[child.tag](child)
    else:
      print(f"{__FUNCTION__()}: Unsupported tag '{child.tag}'")
  

def check_program(node):
  name = node.attrib['filename']
  if not name:
    # TODO: Help needed
    return
  
  global info_
  if "programs" not in info_:
    info_["programs"] = {}
  record_hash = node.attrib['Sha256']
  actual_hash = sha256sum(name)
  if record_hash == actual_hash:
    print(f"{name}: hash ok!")
  else:
    print(f"{name}: hash value {actual_hash} mismatch with recorded value {record_hash}")
  info_["programs"][node.attrib['label']] = name
  #print(node.attrib)
  print(info_)

def handle_Program(node):
  handlers = {
    "program": lambda x: check_program(x)
  }
  for child in node:
    if child.tag in handlers:
      handlers[child.tag](child)
    else:
      print(f"{__FUNCTION__()}: Unsupported tag '{child.tag}'")
  
def handle_root(node):
  handlers = {
    re.compile("BasicInfo"): lambda child: print(child.tag, child.attrib),
    re.compile("SAHARA"): handle_SAHARA,
    re.compile("MEMORY_SIZE"): lambda x: None,
    re.compile("UFS_PROVISION"): lambda x: print(f"Help needed on understanding {x.tag}"),
    re.compile("Program\d+"): handle_Program,
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
