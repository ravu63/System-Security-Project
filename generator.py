import shelve

var = shelve.open('LOL', 'c')

age= int(input(("Enter your age:")))
name = input("Enter your name")

pawns_dict = {}
pawns_dict = var['Pawns']

var['Pawns'].append(age)
var['Pawns'].append(age)

var['Pawns'] = pawns_dict
var.close()




if age == 10:
    var = shelve.open('LOL', 'w')
    pawns_dict = {}
    pawns_dict = var['Pawns']
    kok = input("KOK:")
    var['Pawns'].append(kok)
    var['Pawns'] = pawns_dict
    var.close()