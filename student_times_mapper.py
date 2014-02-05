#!/usr/bin/env python

import sys # Used for stdin and stdout
import csv # Used for parsing input and output lines

# The mapper program - This is a very straight forward program
# which extracts the author ID and the date the post was added
# from the input data file (in this example 'forum_node.tsv')
def mapper():
    # The csv reader to input tab delimited lines
    reader = csv.reader(sys.stdin, delimiter='\t')
    # The csv writer to output tab delimited lines
    writer = csv.writer(sys.stdout, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
    
    # Iterate over each line
    for line in reader:
        # Implement an error handler just in case something goes wrong
        try:
            # The number of expected tokens in an input line is 19
            if len(line) == 19:
                # Take in all the 19 variables from the input line
                node, title, tagnames, author_id, body, node_type, parent_id, abs_parent_id, added_at, score, state_string, last_edited_id, last_activity_by_id, last_activity_at, active_revision_id, extra, extra_ref_id, extra_count, marked = line
                # Store the 2 desired tokens, the author ID and added date, and input
                # them into a list
                output = [ author_id, added_at ]
                # Write that list out as a line to be sent to the reducer
                writer.writerow(output)
            
        # Catch all errors in one statement.  Just continue on to the next line.
        except:
            continue

def main():
    mapper()
    
if __name__ == '__main__':
    main()