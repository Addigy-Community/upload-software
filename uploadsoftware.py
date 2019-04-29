#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Create custom software by specifying a directory containing core files.

"""
import sys
import json
import os
import tarfile
import addytool

cs_root = os.path.abspath(sys.argv[1])

def create_downloads():
    """Uploads files and returns IDs

    Files are uploaded directly, whereas non-files are uploaded as .tar.gz files
    """
    file_upload = addytool.endpoint.FileUpload()
    ignored_files = [
        ".DS_Store",
        "installation_script.sh",
        "removal_script.sh",
        "condition_script.sh",
        "base_identifier.txt",
        "identifier.txt",
        "version.txt"
        ]
    file_ids = []
    for file_ in os.listdir(cs_root):
        if file_ not in ignored_files:
            target_file = cs_root + "/" + file_
            if os.path.isfile(target_file):
                uploaded_file = json.loads(file_upload.post(target_file))
                file_ids.append(uploaded_file)
            else:
                o_cwd = os.getcwd()
                os.chdir(cs_root)
                output_filename = target_file + ".tar.gz"
                with tarfile.open(output_filename, "w:gz") as tar:
                    tar.add(target_file, arcname=os.path.basename(target_file))
                uploaded_file = json.loads(file_upload.post(output_filename))
                os.remove(output_filename)
                os.chdir(o_cwd)
                file_ids.append(uploaded_file)
    return file_ids

def read_file(target_file):
    file_to_read = cs_root + "/" + target_file
    if os.path.isfile(file_to_read):
        with open(file_to_read) as file_:
            f_ = file_.read()
        return f_
    return ""

def determine_identifier():
    __identifier = "identifier.txt"
    abspath_identifier = cs_root + "/" + "identifier.txt"
    if os.path.isfile(abspath_identifier):
        pass
    else:
        __identifier = "base_identifier.txt"
    return __identifier

def determine_if_update(identifier):
    if identifier == "base_identifier.txt":
        return False
    return True

def create_identifier(new_identifier):
    file_to_write = cs_root + "/" + "identifier.txt"
    with open(file_to_write, 'w') as file_:
        file_.write(new_identifier)

def create_installation_script():
    pass

def create_custom_software():
    custom_software = addytool.endpoint.CustomSoftware()
    identifier = determine_identifier()

    new_software = custom_software.post(\
        identifier=read_file(identifier).rstrip('\n'), \
        version=read_file("version.txt").rstrip('\n'), \
        update=determine_if_update(identifier),\
        downloads=create_downloads(), \
        installation_script=read_file("installation_script.sh"), \
        conditional_script=read_file("condition_script.sh"), \
        removal_script=read_file("removal_script.sh") \
        )

    if identifier == "base_identifier.txt":
        create_identifier(new_software['identifier'])

create_custom_software()
