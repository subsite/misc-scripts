#!/usr/bin/python3
#
# Insert color change to gcode file. Tested with Prusa MK2S
#

import sys
import re

# Check arguments
if len(sys.argv) < 3:
    print("USAGE: color_change.py [change height mm] [path to gcode]")
    print("Example: color_change.py 1.2 logo.gcode # Writes new file logo_ColorChange.gcode to the same dir.")
    sys.exit(1)

# Assign vars
change_height = sys.argv[1]
orig_file = sys.argv[2]
search_str = "G1 Z{}".format(change_height)
outfile_name = orig_file.replace(".gcode", "_ColorChange.gcode")

# Check that height is valid
if not re.match("^\d+.\d+$",change_height):
    exit("ERROR: Height must be float with a decimal point, eg. 1.2")

# Open gcode file
try:
    with open(orig_file) as f:
        orig_content = f.readlines()
except:
    exit("ERROR: File not found.")

# Loop through contents
new_content = []
changed_line = False
for idx, line in enumerate(orig_content):
    line = line.strip()
    new_content.append(line)

    # Insert filament change command
    if line.startswith(search_str) and not changed_line:
        new_content.append("M600 ; filament color change")
        changed_line = idx+1


if changed_line:
    # Comment out next extruder command
    new_content[changed_line+1] = "; {}".format(new_content[changed_line+1])

    # Write new file 
    with open(outfile_name, mode='wt', encoding='utf-8') as output_file:
        output_file.write('\n'.join(new_content))

    try:
        # Try to read generated file
        with open(outfile_name) as f:
            outfile_content = f.readlines()

        print("Filament change inserted at {} mm".format(change_height))
        print("File {}".format(outfile_name))

        # Print relevant section of new file
        for r in range(changed_line-1, changed_line+3):
            print("    {}    {}".format(r+1, outfile_content[r].strip()))

    except:
        exit("ERROR: File not created")
        

else:
    print("ERROR: Height {} not found.".format(change_height))


