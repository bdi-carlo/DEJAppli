# -*- coding: utf-8 -*

def parse():
    fBase = open("compendium_base.txt", "r", encoding = "utf-8")
    fNew = open("compendium.txt", "w")
    ligne = ""

    for line in fBase:
        if (',' in line):
            ligne += line
            fNew.write(ligne)
            ligne = ""

    fBase.close()
    fNew.close()

if __name__ == '__main__':
    parse()
