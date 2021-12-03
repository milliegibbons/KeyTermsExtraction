meetings = [('Boris Johnson', 'meets with', 'the Queen'),
            ('Joe Biden', 'meets with', 'his cabinet'),
            ('administration', 'meets with', 'tech giants'),
            ('the Queen', 'meets with', 'the Prime Minister'),
            ('Joe Biden', 'meets with', 'Russian President')]

query = [meetings[x][2] for x in range(0,len(meetings)) if (meetings[x][0]) == 'Joe Biden']
print(query)

#query = [# participant2 for tuples in meetings if p1=='the Queen']
#query += [# participant1 for tuples in meetings if p2=='the Queen']

query = [meetings[x][2] for x in range(0,len(meetings)) if (meetings[x][0]) == 'the Queen']
query += [meetings[x][0] for x in range(0,len(meetings)) if (meetings[x][2]) == 'the Queen']

print(query)

import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Beware the Jabberwock, my son! The jaws that bite, the claws that catch! " +
          "Beware the Jubjub bird, and shun The frumious Bandersnatch!")

rows = []
rows.append(["Word", "Position", "Lowercase", "Lemma", "POS", "Alphanumeric", "Stopword"])
for token in doc:
    rows.append([token.text, str(token.i), token.lower_, token.lemma_,
                 token.pos_, str(token.is_alpha), str(token.is_stop)])

columns = zip(*rows)
column_widths = [max(len(item) for item in col) for col in columns]
for row in rows:
    print(''.join(' {:{width}} '.format(row[i], width=column_widths[i])
                  for i in range(0, len(row))))




doc = nlp("On Friday, board members meet with senior managers " +
          "to discuss future development of the company.")

for chunk in doc.noun_chunks:
    # here you return the noun phrase, its head (main) noun, the dependency relation linking
    # this noun to its own head in the parse tree, and the head of the noun in the parse tree
    print('\t'.join([chunk.text, chunk.root.text, chunk.root.dep_,
            chunk.root.head.text]))



    # the token itself, the dependency relation for the token,
# the head to which the token is linked, the head's PoS,
# the list of all dependents of the token (token.children)

for token in doc:
    print(token.text, token.dep_, token.head.text, token.head.pos_,
                                [child for child in token.children])


for token in doc:
    if token.lemma_=="meet" and token.pos_=="VERB" and token.dep_=="ROOT":
        action = token.text
        children = [child for child in token.children]
        participant1 = ""
        participant2 = ""
        for child1 in children:
            if child1.dep_=="nsubj":
                participant1 = " ".join([attr.text for
                                         attr in child1.children]) + " " + child1.text
            elif child1.text=="with":
                action += " " + child1.text
                child1_children = [child for child in child1.children]
                for child2 in child1_children:
                    if child2.pos_ == "NOUN":
                        participant2 = " ".join([attr.text for
                                             attr in child2.children]) + " " + child2.text
print (f"Participant1 = {participant1}")
print (f"Action = {action}")
print (f"Participant2 = {participant2}")


sentences = ["On Friday, board members meet with senior managers " +
             "to discuss future development of the company.",
             "Boris Johnson met with the Queen last week.",
             "Joe Biden meets the Queen at Buckingham Palace.",
             "The two leaders also posed for photographs and " +
             "the President talked to reporters."]

def extract_information(doc):
    action=""
    participant1 = ""
    participant2 = ""
    for token in doc:
        if token.lemma_=="meet" and token.pos_=="VERB" and token.dep_=="ROOT":
            # check that the token's lemma is "meet", its PoS is VERB and
           # it's the ROOT of the whole sentence (i.e., the main verb)
            action = token.text
            children = [child for child in token.children]
            for child1 in children:
                if child1.dep_=="nsubj":# check that child1 is a subject (i.e., it's related to the verb with the 'nsubj' relation)
                    participant1 = " ".join([attr.text for
                                             attr in child1.children]) + " " + child1.text
                elif child1.text=="with": # i.e., if the verb attaches "with" (as in "meet with")
                    action += " " + child1.text
                    child1_children = [child for child in child1.children]
                    for child2 in child1_children:
                        if child2.pos_ == "NOUN" or child2.pos_ == "PROPN":

                         # check that child2 is either a common noun (NOUN, e.g., "members")
                        # or a proper noun (PROPN, e.g., "Joe")
                            participant2 = " ".join([attr.text for
                                                 attr in child2.children]) + " " + child2.text
                elif child1.dep_=="dobj" and (child1.pos_ == "NOUN"
                                              or child1.pos_ == "PROPN"):
                # check if child1 is a direct object (the dependency relation is 'dobj')
                # and it is either a common or a proper noun
                    participant2 = " ".join([attr.text for
                                             attr in child1.children]) + " " + child1.text
    print (f"Participant1 = {participant1}")
    print (f"Action = {action}")
    print (f"Participant2 = {participant2}")

for sent in sentences:
    print(f"\nSentence = {sent}")
    doc = nlp(sent)
    extract_information(doc)
