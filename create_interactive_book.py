#***IMPORTANT NOTE: Users should avoid non-directional double quotes (") when writing
#their ".txt" document on their computer, as these characters are omitted in the rtf file.
#They should redact their documents in a word processor that uses directional quotes
#and save the document in ".txt" or ".rtf" format. Also, users should avoid putting any text
#before the first section or after the last section, as this would be lost after splitting the
#document into individual sections. They should instead write separate foreword and afterword
#documents that will not be submitted to the present code. Every section within the document
#should bear a unique name, using a "** Section" section opening tag and closing asterisks (**)
#as exemplified by the following section title header: "** Section Exploration of the Caves **".
#The same section titles, without the opening tags or asterisks, but preceded by "turn to" and
#followed by a period (ex: "turn to Exploration of the Caves.") will be used throughout the
#section texts to refer to the the appropriate section title headers. It must be emphasized that
#the presence of two consecutive asterisks (**) before (within the "** Section" section tag)
#and after the section title header is required in order to locate the section titles within the text.
#Furthermore, a period is needed after a section title reference so as to indicate the end
#of the random index (so that "turn to 1" is not confused by the code with "turn to 11",
#for instance). All of the section title headers (ex: "** Section Exploration of the Caves **")
#and section title references (ex: "turn to Exploration of the Caves.")
#need to be spelled in the exact same way to ensure correct random index substitutions.

import random
import re
import sys

#Retrieving the file name that was passed in the command line. The code
#works equally well with ".txt" and ".rtf" documents.
file_name = sys.argv[1]

with open(file_name, "r") as f:
    whole_text = f.read()

#Splitting "whole_text" at the "** Section" section opening tags.
#Accepted splitting points are: "** Section", "**Section",
#"** section" and "**section" to accommodate for user preferences
#and space omissions. The first element of the list is excluded, as it is an
#empty string in the case of ".txt" files and the RTF prolog in
#".rtf" files. Here is an example section before and after splitting:
#"** Section Exploration of the Caves ** remainder of section text",
#"Exploration of the Caves ** remainder of section text"
section_list = re.split("\*\* Section|\*\*Section|\*\* section|\*\*section", whole_text)[1:]

#A set of duplicate section names will be constructed and the
#users will be notified in the event that more than one section
#bear the same name. As every section (regardless of whether
#or not it has a unique name) will be assigned a random number,
#it is important to avoid duplicates to exclude superfluous
#sections in the final text.
duplicate_sections = set()


def create_book():
    #The list "random_indices" doesn’t include section 1 nor the
    #last section (as these sections will be added manually, in order
    #to ensure that they are located at the start and end of the document,
    #respectively). The numbering then starts at 2, and ends at
    #the penultimate section. The list is then shuffled prior to assignment
    #of the random indices to the sections. This will ensure that contiguous
    #sections within a story arc are not physically close (on the same page)
    #in the final rtf document, thus maintaining the element of surprise.
    random_indices = list(range(2, len(section_list)))
    random.shuffle(random_indices)
    #The list of lists "list_section_randomindex" is initialized with
    #the first section, along with its assigned index of 1 (and not
    #a random index from the "random_indices" list).
    list_section_randomindex = [[section_list[0], 1]]
    #The list "list_of_previous_indices" will keep track of the 10 last
    #random indices accessed by the Python code while it is assigning
    #the random indices, to make sure that they are properly spaced out.
    list_of_previous_indices = []
    #The counter "taken_directly_from_random_indices" keeps track of
    #how many random indices (from the "random_indices" list) were
    #assigned to section entries without necessarily meeting the
    #spacing criteria (see below).
    taken_directly_from_random_indices = 0
    def check_previous_random_indices(list_section_randomindex, random_indices,
    list_of_previous_indices, section_list, i, j):
        #For any given random index that is to be assigned to a new section,
        #the code returns "True" if it is distant from the last 10 accessed
        #sections by at least a thirtieth of the total amount of sections
        #(rounded up). The "round(len(sections_list)/30)" was selected as a threshold
        #based on a test document constituted of 300 sections of varying length,
        #which was deemed representative of typical interactive books. In such
        #a test document, the threshold would be of 10 (300/30=10) and would ensure
        #that two contiguous sections would not appear on the same page,
        #nor one page and the next (assuming a maximum of five sections per page).
        for k in range(len(list_of_previous_indices)):
            if abs(j-list_of_previous_indices[k]) <= round(len(section_list)/30):
                return False, list_section_randomindex, random_indices
            elif (k == len(list_of_previous_indices)-1
            and abs(j-list_of_previous_indices[k]) > round(len(section_list)/30)):
                list_section_randomindex.append([section_list[i], j])
                #Once a random index from the "random_indices" list has been
                #selected, it is removed from the list to avoid using it again,
                #which would result in more than one section with the same index.
                random_indices.pop(random_indices.index(j))
                return True, list_section_randomindex, random_indices

    for i in range(1, len(section_list)-1):
        list_of_previous_indices.append(list_section_randomindex[i-1][1])
        #The list "list_of_previous_indices" is kept at a maximum length
        #of 10, by removing the oldest accessed entry, in order to avoid
        #excessive computation.
        if len(list_of_previous_indices) > 10:
            list_of_previous_indices.pop(0)
        for j in random_indices:
            meets_spacing_criteria, list_section_randomindex, random_indices = (
            check_previous_random_indices(list_section_randomindex, random_indices,
            list_of_previous_indices, section_list, i, j))
            #Only one random index must be assigned per section, so it is
            #important to break out of the "for j in random_indices" loop
            #when an index has met the spacing criteria and has been assigned
            #to a section. Otherwise, all of the random indices meeting the
            #criteria would be selected (and the list would be shortened
            #following "random_indices.pop(random_indices.index(j))").
            if meets_spacing_criteria == True:
                break
            #The counter "taken_directly_from_random_indices" keeps track of
            #how many random indices (from the "random_indices" list) were
            #assigned to section entries without necessarily meeting the
            #spacing criteria.
            elif random_indices != [] and j == random_indices[-1] and meets_spacing_criteria == False:
                list_section_randomindex.append([section_list[i], random_indices[0]])
                random_indices.pop(0)
                taken_directly_from_random_indices+=1

    #The last section is added to "list_section_randomindex list" list,
    #along with its index (equal to the total amount of sections).
    list_section_randomindex.append([section_list[-1], len(section_list)])
    #To facilitate indexing during the contiguity check, the list of lists
    #"list_section_randomindex" is split in two before sorting "list_section_randomindex"
    #based on the random indices. This will allow to find the position of a section
    #in the original document from its random_index, in order to determine the
    #index of the farthest section reached "index_farthest_section_reached"
    #during the contiguity check.
    list_sections = [element[0] for element in list_section_randomindex]
    list_randomindex = [element[1] for element in list_section_randomindex]
    #The list "sorted_list_section_randomindex" is sorted according to the random indices.
    #This will assemble the sections in the order in which they will appear in the final
    #document. Another list of the sorted random indices "sorted_list_randomindex" is
    #populated to facilitate indexing during the contiguity check, as above.
    sorted_list_section_randomindex = sorted(list_section_randomindex, key=lambda x:x[1])
    sorted_list_randomindex = [element[1] for element in sorted_list_section_randomindex]

    #The function "create_book()" will be run in a while loop untill all random indices
    #that are assigned meet the spacing criteria.
    percent_taken_directly_from_random_indices = taken_directly_from_random_indices/len(section_list)*100
    if percent_taken_directly_from_random_indices == 0:
        global loop_on
        loop_on = False
        return sorted_list_section_randomindex, sorted_list_randomindex, list_sections, list_randomindex

loop_on = True
while loop_on:
    try:
        sorted_list_section_randomindex, sorted_list_randomindex, list_sections, list_randomindex = create_book()
    except:
        pass

#The rich text format (RTF) document string is assembled by stitching together every section from the
#list "sorted_list_section_randomindex" (sorted by random index). The RTF command "\par\par\pard" is
#added in between sections to add a new line.
interactive_rtf = ""
for section in sorted_list_section_randomindex:
    interactive_rtf += section[0] + r"\par\par\pard"

#The section title headers (ex: "Exploration of the Caves **") are sliced from the individual
#sections based on the indices of occurences of two adjoining asterisks (**) in the section headers.
#The section title headers are first replaced with their random indices, and then the random indices
#are substituted for the section title references (ex: "turn to Exploration of the Caves.") within
#the section paragraphs themselves.
for section in sorted_list_section_randomindex:
    index_asterisks = re.search("\*\*", section[0])
    section_title = section[0][:index_asterisks.start()].strip()
    section_title_with_stars = section[0][:index_asterisks.start()+2]
    #The section title headers will have a slightly larger font size (\fs28 results in a font size of 14),
    #and will be centered (\qc) and boldfaced (\b index \b0). Also, the RTF command "\keepn" ensures
    #that the section title headers will not appear on separate pages from the start of the section paragraph.
    if interactive_rtf.count(section_title + " **") + interactive_rtf.count(section_title + "**") > 1:
        duplicate_sections.add(section_title)
    interactive_rtf = (interactive_rtf.replace(section_title_with_stars,
    r"{\par \fs28 \keepn \qc \b " + str(section[1]) + r"\b0 }\par \pard \fs24")
    .replace(section_title + ".", r"\b " +  str(section[1]) + r"\b0."))

#Instances of one or more spaces are replaced with a single space to exclude superfluous spaces,
#and the directional quotes are replaced with their RTF escapes.
interactive_rtf = ((re.sub('[" "]+', " ", interactive_rtf)).replace("‘", "\\'91")
.replace("’", "\\'92").replace('“', "\\'93").replace('”', "\\'94"))

#The RTF document is written to file, preceded by a simple RTF prolog and followed by a closing
#curly bracket.
with open(file_name[:-4] + " interactive_book.rtf", "w") as g:
    g.write(r"{\rtf1 \ansi \deff0 {\fonttbl {\f0 Ubuntu;}} \f0 \fs24 \par " + interactive_rtf + "}")


#The list "interactive_book_resplit" is created by splitting the string "interactive_rtf"
#along the section dividers "\par\par\pard" (additional escapes needed with re.split),
#excluding the last element (an empty string, as there is no text after the last section divider).
interactive_book_resplit = re.split(r"\\par\\par\\pard", interactive_rtf)[:-1]

#the function "check_contiguity()" will travel along the contiguous sections of the document,
#and try to reach the last section. It starts at the first section (current_node = 1) and the
#value of current_node will be updated to reflect the progression of the function in reaching
#the last section. Of note, the random indices of the sections accessed during this process
#will be pararllelled to their corresponding index within the unsorted list "list_randomindex".
#The value of "index_farthest_section_reached" (initialized at 0), will be updated to the highest
#index of the unsorted list "list_randomindex" before returning. Upon reaching the final
#section index, "contiguity_success" will be set to "True" before returning. The list "past nodes"
#(initialized with the first section index), keeps track of the sections visited during the
#contiguity check. It will prevent endless loops from taking place and force the algorithm
#forward.
current_node = 1
contiguity_success = False
past_nodes = [1]
index_farthest_section_reached = 0
def check_contiguity(current_node, past_nodes, list_randomindex, index_farthest_section_reached):
    force_next = False
    #A list of all instances of "turn to" followed by a random index (in boldface) will
    #be populated and the digits will be extracted in order to parallell them with the unsorted
    #list "list_randomindex" and update the value of the variable "index_farthest_section_reached",
    #until the final section is reached, upon which the contiguity_success variable is set to "True".
    for i in range(len(sorted_list_randomindex)):
        list_of_turn_to = (re.findall(r"turn to \\b \d+\\b",
        interactive_book_resplit[sorted_list_randomindex.index(current_node)]))
        for j in range(len(list_of_turn_to)):
            turn_to_randomindex = int(re.search(r"\d+", list_of_turn_to[j])[0])
            if sorted_list_randomindex[i] == turn_to_randomindex:
                next_list_of_turn_to = (re.findall(r"turn to \\b \d+\\b",
                interactive_book_resplit[sorted_list_randomindex.index(turn_to_randomindex)]))
                if turn_to_randomindex == len(sorted_list_randomindex):
                    return current_node, turn_to_randomindex, index_farthest_section_reached

                #If a given index is repeated in the list "past_nodes", the variable
                #"force_next" is set to "True", which forces the algorithm to choose a
                #different path (list_of_turn_to[j+1] instead of list_of_turn_to[j],
                #unless there are no other available "turn_to" options).
                for node in past_nodes:
                    if past_nodes.count(node) > 1:
                        force_next = True

                if (next_list_of_turn_to != [] and next_list_of_turn_to != [r"turn to \b 1\b"]
                and force_next == False):
                    current_node = turn_to_randomindex
                    past_nodes.append(current_node)
                    potential_index = list_randomindex.index(sorted_list_randomindex[i])
                    if potential_index > index_farthest_section_reached:
                        index_farthest_section_reached = potential_index
                    return current_node, turn_to_randomindex, index_farthest_section_reached
                elif (next_list_of_turn_to != [] and next_list_of_turn_to != [r"turn to \b 1\b"]
                and force_next == True and j < len(list_of_turn_to)-1):
                    current_node = int(re.search(r"\d+", list_of_turn_to[j+1])[0])
                    past_nodes.append(current_node)
                    potential_index = list_randomindex.index(sorted_list_randomindex[i])
                    if potential_index > index_farthest_section_reached:
                        index_farthest_section_reached = potential_index
                    return current_node, turn_to_randomindex, index_farthest_section_reached
                elif (next_list_of_turn_to != [] and next_list_of_turn_to != [r"turn to \b 1\b"]
                and force_next == True and j == len(list_of_turn_to)-1):
                    current_node = int(re.search(r"\d+", list_of_turn_to[j])[0])
                    past_nodes.append(current_node)
                    potential_index = list_randomindex.index(sorted_list_randomindex[i])
                    if potential_index > index_farthest_section_reached:
                        index_farthest_section_reached = potential_index
                    return current_node, turn_to_randomindex, index_farthest_section_reached
    return current_node, None, index_farthest_section_reached

#The function "check_contiguity()" is called 999 times, or until it returns a value of
#"contiguity_success" equaling "True", meaning that the final section has been reached.
#Also, the length of the list "past_nodes" is kept at a maximum of 5 entries within
#the "check_contiguity()" function by removing the oldest section accessed. This ensures
#that some level of flexibility, as it will at times be necessary to return to a previous
#node in order to move forward in the story arc towards the last section.
for i in range(999):
    current_node, turn_to_randomindex, index_farthest_section_reached = (check_contiguity(current_node,
    past_nodes, list_randomindex, index_farthest_section_reached))
    if len(past_nodes)>4:
        past_nodes.pop(0)
    elif turn_to_randomindex == len(sorted_list_randomindex):
        contiguity_success = True
        print("\nYour interactive document entitled “""" + file_name[:-4] + """ interactive_book.rtf”
has been created and it has been successfully tested for contiguity
(being able to go from the first to the very last entry without interruption).\n""")
        break

#If the last section hasn't been reached after the 999 "check_contiguity()" function calls,
#("contiguity_success" will still be at its default "False" value), the text of the
#farthest section in the unsorted list "list_sections" indexed at "index_farthest_section_reached"
#will be provided. The section will be truncated if it contains more than 251 characters for brevity.
#It should be noted that the code was tested on documents containing up to 1000 sections, and
#was able to reach the ending within 999 "check_contiguity()" function calls in all cases.
if contiguity_success == False and len(list_sections[index_farthest_section_reached]) > 250:
    print("""\nThere seems to be a contiguity problem with your interactive
storyline. The Python code wasn't able to contiguously travel from the first
to the last section. The farthest section that was contiguously reached in
your original unsorted manuscript was:\n\n"""
+ list_sections[index_farthest_section_reached][:250] + "[...]\n")
elif contiguity_success == False and len(list_sections[index_farthest_section_reached]) <= 250:
    print("""\nThere seems to be a contiguity problem with your interactive
storyline. The Python code wasn't able to contiguously travel from the first
to the last section. The farthest section that was contiguously reached in
your original unsorted manuscript was:\n\n"""
+ list_sections[index_farthest_section_reached] + "\n")

#If there are duplicate section titles, they will be reported to the user.
if duplicate_sections != set():
    print("Some duplicate section titles were found throughout the text:")
    for duplicate in duplicate_sections:
        print("• " + duplicate)
    print("")
