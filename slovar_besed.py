import json

# množica besed iz besede_iz_sskj2.txt file
vse_besede = set()
with open('besede_iz_sskj2.txt', 'r') as beri:
    for beseda in beri:
        vse_besede.add(beseda[:-1])  # odstranim \n


def hamming_razdalja(s1, s2):
    """Vrne Hammingovo razdaljo med dvema nizoma iste dolžine."""
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))


slovar_1 = dict()
for beseda in vse_besede:
    if beseda not in slovar_1:
        slovar_1[beseda] = []


for beseda in vse_besede:
    # poveže besede ki se razlikujejo v tem da ima ena od njiju črko več ali manj od druge
    # (črke se odstrani ali doda le spredaj ali zadaj)
    if beseda[:-1] in slovar_1:
        slovar_1[beseda[:-1]].append(beseda)
        slovar_1[beseda].append(beseda[:-1])
        print(beseda[:-1], beseda)
    if beseda[1:] in slovar_1:
        slovar_1[beseda[1:]].append(beseda)
        slovar_1[beseda].append(beseda[1:])
        print(beseda[1:], beseda)
    # poveže besede ki se razlikujeta v eni črki, besedi sta iste dolžine
    # pomagam si z funkcijo hamming distance ki bo povezal vse besede kjer funckija vrne 1
    for beseda_1 in slovar_1:
        if len(beseda) == len(beseda_1):
            if hamming_distance(beseda, beseda_1) == 1:
                if beseda not in slovar_1[beseda_1]:
                    slovar_1[beseda_1].append(beseda)
                if beseda_1 not in slovar_1[beseda]:
                    slovar_1[beseda].append(beseda_1)
                print(beseda, beseda_1)

# zapis slovarja v .txt
with open('slovar_besed_ter_sosedov.txt', 'w', encoding='utf8') as pisi:
    pisi.write(json.dumps(slovar_1))


