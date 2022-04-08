import random
import re
import sys
from spellchecker import SpellChecker

#Retrieving the file name that was passed in the command line. The code
#works equally well with ".txt" and ".rtf" documents.
file_name = sys.argv[1]

#The sentence titles will be spellchecked using the SpellChecker module.
spell = SpellChecker()


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

problematic_sections = []
for i in range(len(section_list)):
    #The if statement appends sections to the "problematic_sections" list if there are
    #issues with the index at which asterisks are found within the section. For example, if
    #there were asterisks before the end of the usual section tag (ex: if the first section begins
    #with the section tag typo "**Sectoon" and the closing asterisks of that section were omitted),
    #"index_asterisks.start()" would then be lower than 2.  Alternatively, if such a typo
    #("** Sectoon" instead of "** Section") was observed elsewhere than in the first section,
    #that section would therefore not have been split, and the asterisks would occur much farther
    #than would be normally expected in a section title ("index_asterisks.start()" would then
    #be greater than 250). Similarly, the asterisks could also have been omitted altogether in
    #a given section, resulting in the asterisks from the following section being indexed.
    index_asterisks = re.search("\*\*", section_list[i])
    if index_asterisks == None or index_asterisks.start() < 2 or index_asterisks.start() > 250:
        problematic_sections.append(section_list[i])
    #If there is more than one instance of two adjoining asterisks (**) in a given section,
    #that section will be included in "problematic_sections", as it may be that the section
    #splitting did not proceed as planned, for example because of a typo in the section tag.
    elif re.findall("\*\*", section_list[i]).count("**") > 1:
        problematic_sections.append(section_list[i])
    #If a section does not present any of the abovementioned issues, its title (ex: "Exploration of the Caves **")
    #is extracted by slicing the section using the index at which two adjoining asterisks (**) are observed.
    #The titles are then split into individual words and spellchecked. If unknown words are
    #detected, ("spell.unknown(section_title_words)" isn't an empty set), the section is added
    #to the list "problematic_sections", as typos would lead to issues in substituting the
    #random indices for the section titles. All of the section title headers
    #(ex: "** Section Exploration of the Caves **") and section title references within the section text
    #(ex: "turn to Exploration of the Caves.") need to be spelled in the exact same way to ensure
    #correct random index substitutions.
    else:
        section_title = section_list[i][:index_asterisks.start()].strip()
        section_title_words = re.split(r"\W+", section_title)
        if spell.unknown(section_title_words) != set():
            problematic_sections.append(section_list[i])

#A text document sharing the file name with the addition of "_section_typos" is generated,
#listing all of the sections in the list "problematic_sections" for which issues have
#been detected. It is up to the user to inspect this document and address these issues
#before proceeding with the next Python code "create_interactive_book.py" to get best results.
with open(file_name[:-4] + "_section_typos.txt", "a+") as g:
    g.write("""LIST OF SECTIONS WITH MISSING ASTERISKS, MISSPELLED SECTION TAGS OR MISSPELLED
    SECTION TITLES (WITH “=” DIVIDERS IN BETWEEN EVERY SPLIT SECTIONS):\n""" + 60*"=" + "\n")
    for section in problematic_sections:
        g.write(section + 60*"=" + "\n")
