#!/usr/bin/env python

import sys # Used for stdin and stdout
import csv # Used for parsing input and output lines

# Used for parsing date values from input strings
from datetime import datetime

# A relatively straight forward reducer program.
# It will input 2 tokens from the mapper and then output a line
# that contains the author ID and the hour during which the
# author is the most active on the forum.  If the author
# is equally active during multiple hours then those hours
# will be printed each on different lines.
def reducer():
    # The csv reader to input tab delimited lines
    reader = csv.reader(sys.stdin, delimiter='\t')
    # The csv writer to output tab delimited lines
    writer = csv.writer(sys.stdout, delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL)
    
    # A dictionary which will associate an author ID with the hours during which
    # the author is active on the forum
    user_hour_cnt = dict()
    
    # Iterate over each line from the input
    for line in reader:
        # Implement an error handler in case anything goes wrong
        try:
            # The number of expected tokens is 2
            if len(line) == 2:
                # The 2 expected tokens from the mapper are the
                # author ID and the date the post was added to the forum
                author_id, added_date = line
            
                # The author ID should be converted from a string to an integer
                author_id  = int(author_id)

                # Try to parse the added date field as a proper date,
                # implementing an error handler in the event something
                # goes wrong.
                try:
                    # The input time has superfluous information after the
                    # period, which should be discarded in order to
                    # correctly parse the date
                    dot_index  = added_date.index('.')
                    added_date = added_date[:dot_index]
                    # Now, attempt to parse the date string and retrieve the hour field
                    # which is a value between 0 to 23
                    hour       = datetime.strptime(added_date, '%Y-%m-%d %H:%M:%S').hour
                # If an error was caught, then move on to the next line, nothing to see here
                except:
                    continue
                
                # Check to see if the author is not already in the dictionary
                if author_id not in user_hour_cnt:
                    # If the author is new, then create a new list to store
                    # the hours of activity
                    user_hour_cnt[author_id] = [0 for i in xrange(24)]
                # Implement the hour of activity for the hour
                user_hour_cnt[author_id][hour] += 1
                
        except:
            continue
        
    # Finally, after all the user activity hours have been recorded, the reducer
    # can iterate through each author's list to see during which hour the author
    # was most active
    for user in user_hour_cnt:
        # Initialize the count to 0
        max_cnt      = 0
        # Create a list to store one or more hours of maximum activity
        # for the author
        max_cnt_list = list()
        # Loop through 24 hours to find the hour(s) of maximum activity
        for hour in xrange(24):
            # If an hour of maximum activity has been found which is
            # greater than the previous one, then set it as the
            # hour of maximum activity and create a new list with
            # this hour as the single hour.  All hours which have
            # been previously recorded, are no longer peak hours
            # for this author
            if user_hour_cnt[user][hour] > max_cnt:
                max_cnt = user_hour_cnt[user][hour]
                max_cnt_list = [hour]
            # If an equivalent hour has been recorde then add it to the list
            elif user_hour_cnt[user][hour] == max_cnt:
                max_cnt_list += [hour]
        # Iterate through the list of peak hours for the current author
        # and output each item in that list to its own line
        for max_hour in max_cnt_list:
            output = [user, max_hour]
            writer.writerow(output)
    # All done!

def main():
    reducer()
    
if __name__ == '__main__':
    main()
