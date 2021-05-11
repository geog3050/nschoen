##Question 1
mystr = input('enter a string:')
letter = input('enter a letter:')
if (letter in mystr):
    print("Yes")
else:
    print("No")
    
##Question 2
def examineList(myList):
    myList.sort()
    return myList[-2]

##Question 3
def duplicates(myList):
    for value in myList:
        if myList.count(value) > 1:
            print("The list provided contains duplicate values.")
    else:
        print("The list provided does not contain duplicate values.")