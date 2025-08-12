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
    print(f'"{entity}: oh, hello! are you my interviewer today?"')
            #adding into the story about what is happening
    print(f'"{name} uh, yes, i will be interviewing you today, uh, can you tell me..."')
    explain = input("your name? what are you? are you hostile or dangerous? maybe its time to end this interview? (name/you/danger/exit)")
            #makes the user able to split into paths and questions
    if 'name' in explain:
        entity = 'Pom'
        print(f'"{entity}: oh, my name is Pom, i am not aware of my SCP number though, i have not got one yet"')
            #changing the entity's name now that it has been learnt
    elif 'you' in explain:
        print(f'"{entity}: hmm, well i guess i am a blob of sentient biomass, it is quite fun i guess, being able to rearange my form as i see fit"')
        print(f'"{entity}: my core gives me form, it is inside of my torso, and is what allows me to take form, small spherical thing"')
            #giving information that could be useful later
    elif 'danger' in explain:
        print(f'"{entity}: oh, i am very dangerous, I can mimic any element on the periodic table, including radioactive ones"')
            #giving information that could be useful later
    elif 'exit' in explain:
        print(f'"{name}: I think it is around time to wrap up this interview, thank you {entity} have a good day"')
        print(f'"{entity}: oh, i do not think i will be doing that, you see, i have no intention of being locked up"')
        print(f'"[the gigacounter in the room suddenly starts beeping incredibly quickly, {entity} is mimicking radium, causing you to pass out from radiation sickness]"')
        print("[you awake groggily, the lights are out and you feel like you're having an intense hangover, you crawl your way outside and lock the blastdoor shut, your headache subsides]")