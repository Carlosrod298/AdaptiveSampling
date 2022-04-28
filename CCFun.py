
# Zigbee
Ism = 21000     #uA State machine
Isn = 17000     #uA read sensors
It  = 22000     #uA transmision
Ir  = 24000     #uA reception
Igs = 17000     #uA go to sleep
Isl = 20        #uA Sleep Mode
#  times
smT = 7     #ms state machine time
snT = 5     #ms read sensors
txT = 12    #ms tx time
rxT = 20.0  #ms rx time
gsT = 2     #ms go to sleep time
TimesUpdate = 2


def Compsuption(StVal):
    if(StVal>30):
        StVal = 30
    if (StVal < 1):
        StVal = 1
    #sleep Time
    slT = ((60000 - (TimesUpdate * smT) - snT) * StVal) - (txT + rxT + gsT)
    CurrentAvg = ((TimesUpdate * smT * Ism * StVal) + (Isn * snT * StVal) + (It * txT) + (Ir * rxT * StVal) + (
                Isl * slT) + (Igs * gsT)) / (60000 * StVal)
    return CurrentAvg

def MaxCompsuption():
    # Zigbee
    slT = ((60000 - (TimesUpdate * smT) - snT) ) - (txT + rxT)
    return float(((TimesUpdate*smT*Ism)+(Isn*snT)+(It*txT)+(Ir*rxT)+(Isl*slT))/(60000))