# upload-software

`uploadsoftware.py` leverages `addytool` to load custom software to Addigy.

## Directory Requirements
`uploadsoftware.py` takes one argument: a directory containing a few essential files. Those files include the following:

- base_identifier.txt (required for initial upload)
- identifier.txt (optional, created automatically after initial upload and used to determinine if an update)
- installation_script.sh (optional)
- condition_script.sh (optional)
- removal_script.sh (optional)
- version.txt (optional)

## Installation File Handling
Any files living in the target directory that are not one of the above (or `.DS_Store`) will be automatically loaded up to Addigy and included in the custom software as a download. Non-files will be converted to tar.gz files before being uploaded. 

## To Do
- Files that are converted to tar.gz format should be automatically extracted before the installation script, and the extracted versions should be removed upon completion of the installation script in order to save space on the device.
- Docstrings should be added.
- This was made in haste and is sloppy. Style improvements should be made.
