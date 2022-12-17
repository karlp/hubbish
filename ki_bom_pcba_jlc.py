"""
    @package
    Generates a BOM suiting JLC's guideline's for PCBA.

    Output: CSV (comma-separated)
    Grouped By: Value, Footprint
    Sorted By: Ref
    Fields: MPN, refs, qty, notes, alt#, alt#2, lcsc#, digikey#, mouser#

    Command line:
    python "pathToFile/thisfile" "%I" "%O.csv"
"""
import sys
import os
print([(x,os.environ[x]) for x in os.environ if x.startswith("KI")])
print(os.environ["PYTHONPATH"])
# Import the KiCad python helper module and the csv formatter
#   
sys.path.append("/usr/share/kicad/plugins")
import kicad_netlist_reader
import kicad_utils
import csv

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])

# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    f = kicad_utils.open_file_writeUTF8(sys.argv[2], 'w')
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout

# Create a new csv writer object to use as the output formatter
out = csv.writer(f, delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)

# Output a set of rows for a header providing general information
out.writerow(['Comment', 'Designator', 'Footprint', 'JLCPCB Part #'])

# Get all of the components in groups of matching parts + values
# (see ky_generic_netlist_reader.py)
grouped = net.groupComponents()

# Output all of the component information
for group in grouped:
    refs = []

    # Add the reference of every component in the group and keep a reference
    # to the component so that the other data can be filled in once per group
    for component in group:
        if component.getField("DNP") == "1":
            print(f"skipping DNP {c.getRef()}:{c.getValue()}") 
            continue
        refs.append(component.getRef())
        c = component

    out.writerow([
        c.getValue(),
        ','.join(refs),
        c.getFootprint(),
        c.getField("lcsc#"),
    ])


out.writerow([]) #blank line separator
#out.writerow(['Source:', net.getSource()])
#out.writerow(['Date:', net.getDate()])
#out.writerow(['Tool:', net.getTool()])
#out.writerow( ['Generator:', sys.argv[0]] )
# This doesn't accoutn for DNP skipping, so just ignore it.
#out.writerow(['Component Count:', len(net.components)])
