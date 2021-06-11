import random

######################################################################################################

# The year at the start of the simulation period (preceding the first year that the user has to
# allocate government spending)
START_YEAR = 2011

# The number of years the user has to allocate government spending
YEARS_SIMULATED = 4

# The number of categories of government expenditure
NUM_CATEGORIES = 3

# The minimum percentage of expenditure required for security
MIN_SECURITY_EXPENDITURE = 25

######################################################################################################

# Singapore GDP per capita (PPP) from 2011 to 2015
ACTUAL_GDP = [80052, 82065, 83002, 84423, 86975]

# Rows correspond to years 2012 to 2015
# Columns correspond to (unscaled) percentage of spending on
#   social development
#   infrastructure-&-research
#   security
ACTUAL_EXPENDITURES = [
    [45, 20, 31],
    [46, 18, 32],
    [48, 18, 30],
    [47, 22, 27]
]

######################################################################################################


def main():
    printInstructions()
    scaledExpenditures = scaleExpenditures(ACTUAL_EXPENDITURES)
    # This boolean indicates whether or not the simulator needs to restart because of insufficient
    # security expenditure
    restartSimulation = True
    while restartSimulation:
        restartSimulation = False
        currGDP = ACTUAL_GDP[0]
        print("In {}, the GDP per capita (PPP) was ${}.".format(START_YEAR, currGDP))
        printSectionDivider()
        for i in range(YEARS_SIMULATED):
            print("The year is " + str(START_YEAR + i + 1) + ".")
            print("Please enter your allocations towards 1) Social Development, 2) Infrastructure & Research, and "
                "3) Security, according to the format described in the instructions above:")
            expenditures = getExpendituresFromUser()
            currGDP, gdpGain = calculateNewGDP(currGDP, expenditures, scaledExpenditures[i], i)
            if currGDP == 0:
                print("\n\nInsufficient spending on defense led to an invasion by a foreign power. "
                        "Please try again.")
                printSectionDivider()
                restartSimulation = True
                break
            print("\n")
            printResponseToUser(gdpGain, currGDP)
    printFinalMessage(currGDP)
    

def printInstructions():
    print("\n")
    printSectionDivider()
    print(
        "\nWelcome to the economic policy simulator!\n"
        "You will steer the Singapore economy through the years from " + str(START_YEAR) +
        " through " + str(START_YEAR + YEARS_SIMULATED) + " "
        "by allocating budget funds across three categories:\n\n"

        "I. Social development (education and healthcare)\n"
        "II. Infrastructure and research\n"
        "III. Security (including police and military)\n\n"

        "For each year, enter the percentage of available funds that you wish to "
        "allocate to each of these categories. For example, you may enter \"40 30 30\" "
        "or \"90 5 5\". Please ensure that these percentages sum to 100.\n\n"

        "Your objective is to maximize the GDP per capita (PPP) of the city in " +
        str(START_YEAR + YEARS_SIMULATED) + ".\n\n"

        "You can assume that other necessary expenditures, such as welfare programs and "
        "national debt repayments, are being taken care of automatically.\n\n"

        "Be careful not to spend too little on security. Doing so may leave the city-state "
        "vulnerable to attack from a foreign power.\n"
    )
    printSectionDivider()


# Scales the actual (optimal) allocations so that values in each year sum to 100
def scaleExpenditures(expenditures):
    scaledExpenditures = []
    for expendituresThisYear in expenditures:
        sumForYear = sum(expendituresThisYear)
        scaledExpendituresThisYear =[val / sumForYear * 100 for val in expendituresThisYear]
        scaledExpenditures.append(scaledExpendituresThisYear)
    return scaledExpenditures


def getExpendituresFromUser():
    errorMsg = "Invalid input. Please try again."
    while True:
        expendituresString = input("Enter spending here: ")
        # pctStrings is a list of strings representing integer percentages
        pctStrings = expendituresString.split()
        if len(pctStrings) != NUM_CATEGORIES:
            print(errorMsg)
            continue
        invalidValue = False
        for pct in pctStrings:
            if not pct.isnumeric() or int(pct) > 100 or int(pct) < 0:
                invalidValue = True
                break
        if invalidValue:
            print(errorMsg)
            continue
        expenditures = [int(pct) for pct in pctStrings]
        if sum(expenditures) != 100:
            print("Percentages do not sum to 100. Please try again.")
            continue
        break
    return expenditures


def calculateNewGDP(currGDP, expenditures, actualExpenditures, i):
    # Return a newGDP of 0 and gdpGain of -currGDP if security expenditure is less than the
    # minimum required
    if expenditures[2] < MIN_SECURITY_EXPENDITURE:
        return 0, -currGDP
    maxGain = ACTUAL_GDP[i + 1] - currGDP
    pctOfMaxGain = 0
    for c in range(NUM_CATEGORIES):
        pctOfMaxGain += min(expenditures[c],  actualExpenditures[c])
    gdpGain = pctOfMaxGain / 100 * maxGain
    # The "+ 3" below is to resolve a rounding issue, that leads to the maximum
    # possible GDP attainable in this simulator being $3 less than the actual value
    # in 2015
    newGDP = currGDP + gdpGain + 3
    return newGDP, gdpGain


def printResponseToUser(gdpGain, currGDP):
    responses = ["Congratulations", "Good choices", "Nice work", "Well done"]
    print(responses[random.randrange(len(responses))] + "! " + "GDP per capita (PPP) has risen by $" + 
        str(round(gdpGain)) + ".")
    print("GDP per capita (PPP) is now $" + str(round(currGDP)) + ".")


def printFinalMessage(currGDP):
    printSectionDivider()
    print("The city's final GDP per capita (PPP) is ${}, which is ${} away from the "
        "maximum possible value of ${}.\n\n".format(
            str(round(currGDP)), 
            str(round(ACTUAL_GDP[-1] - currGDP)),
            str(ACTUAL_GDP[-1])
        )
    )


def printSectionDivider():
    print("..........................................................")


if __name__ == "__main__":
    main()