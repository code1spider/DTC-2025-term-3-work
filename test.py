import sys
name = input("what is your name? ")
print(f'"Guard: hello {name} you are to interview the new SCP in the containment cell"')
#asking for name, which will later be used in game
print('"Guard: remember, we dont know much about this SCP, so you are on your own, here is the keycard"')
choice1 = input("head to interview SCP or decide this is above your paygrade and leave? (interview/leave)")
#giving the user the choice between two endings
if 'leave' in choice1:
    print("ending 1/? not my job!")
    print("you decided to abandon your duty, so a class D personel was let into the cell instead, minutes later there was a containment breach in the entire sector, but what would you care? its not like thats your job")
    sys.exit()
    #the above code is an ending, the end of the code stops further code from being run, while the input adds filler for the ending
else:
    entity = '???'
    #defining the SCP's name, which will be used later. Set to ??? as the user doesn't know its name yet
    print("you head to the containment cell, the door opens and closes behind you")
    print("the SCP seems to wait patently, she is humanoid, but made of a pink goo like substance")

    #test
    
    