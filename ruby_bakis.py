
"""
If you get an error stating matplotlib isn't installed, copy-paste this in Command Window:
python -m pip install -U matplotlib
It will automatically download and install the required package!
"""

def takeInput(grimOk=1, plotOk=1):
    if grimOk == 0:
        grim = input("Are you using a Grimoire? (Y/N) ")
        return grim
    if plotOk == 0:
        plot = input("Do you want a graph of the results? (Y/N) ")
        return plot
    else:
        maxHp = int(input("What is the boss's max HP? (integer) "))
        grim = input("Are you using a Grimoire? (Y/N) ")
        minDamage = int(input("What is the minimum damage you want Baki procs to do? "))
        plot = input("Do you want a graph of the results? (Y/N) ")
        nIterations = 500 # Into how many equally spaced parts do you want the boss's HP to be split?
        return maxHp, grim, minDamage, plot, nIterations

def damageDealt(maxHp, grim, nIterations):
    """
    This function is called to calculate the damage dealt with ruby bakriminel bolts (e).
    it returns a tuple consisting of (hpArr, dmgArr). They are both lists and represent the boss's HP
    for each interval and the damage dealt with ruby procs, respectively.
    """

    hpArr = [(maxHp*i/nIterations) for i in range(0,nIterations)]     # split HP into nIterations equally spaced parts
    dmgArr = [(i*0.2*i/maxHp) for i in hpArr]         # ignore the condition that minimum dmg is 1% of current hp
    for i in range(1,len(dmgArr)):                        # take into account condition that damage is 1% at minimum
        if dmgArr[i] < 0.01*hpArr[i]:
            dmgArr[i] = 0.01*hpArr[i]
        else:
            break

    if grim == 0:
        dmgCap = [10000]*nIterations
        for i in range(nIterations//2):
            dmgCap[i] = 10000*2*hpArr[i]/maxHp
    else:
        dmgCap = [15000]*nIterations
        for i in range(nIterations//2):
            dmgCap[i] = 15000*2*hpArr[i]/maxHp
    for i in range(nIterations):
        if dmgArr[i] > dmgCap[i]:
            dmgArr[i] = dmgCap[i]
        else:
            continue
    return hpArr, dmgArr

test = 0
if test == 1:
    maxHp = 1000000 # Total boss HP
    grim = 0 # Does player have Grim? Yes = 1, No = 0
    minDamage = 3000 # the minimum damage you want Bakis to do
    plot = 0 # Do you want a visual representation of damage dealt for boss's hp? Yes = 1, No = 0
    nIterations = 500 # Into how many equally spaced parts do you want the boss's HP to be split?

else:
    maxHp, grim, minDamage, plot, nIterations = takeInput(grimOk=1, plotOk=1)

    if grim == "Y" or grim == "y":
        grim = 1
    elif grim == "N" or grim == "n":
        grim = 0
    else:
        grim = takeInput(grimOk=0, plotOk=1)

    if plot == "Y" or plot == "y":
        plot = 1
    elif plot == "N" or plot == "n":
        plot = 0
    else:
        plot = takeInput(grimOk=1, plotOk=0)

if plot == 1:
    try:
        import matplotlib.pyplot as plt
    except:
        print("It seems like matplotlib isn't installed on your computer. Please do so by copy-pasting the following line in Command Line:")
        print("python -m pip install -U matplotlib")
        input("Pres any key to exit...")

hp, damage = damageDealt(maxHp, grim,nIterations)

threshHp = 0
threshDamage = 0
for i, b in enumerate(damage):
    if b < minDamage:
        continue
    else:
        threshHp = hp[i]
        threshDamage = b
        break

print("You shouldn't use ruby bakriminel bolts if the boss has less than: " + str(threshHp) + " HP")
print("At this point, you'll do: " + str(threshDamage) + " damage")

if plot == 1:
    bak = plt.plot(hp, damage, label='Ruby proc curve')  # Plot some data on the axes.
    plt.setp(bak, color='r', linewidth=2.0)
    dragon = plt.plot(hp, [3000*1.25]*nIterations, label='Dragonstone proc damage curve')
    plt.setp(dragon, color='m', linewidth=2.0)
    plt.xlabel('Boss remaining HP')  # Add an x-label to the axes.
    plt.ylabel('Bakriminel Proc Damage')  # Add a y-label to the axes.
    plt.title("Bakriminel bolts Damage in function of Boss HP")  # Add a title to the axes.
    plt.grid(True)
    plt.legend()
    plt.show()

input('Press any key to exit...')