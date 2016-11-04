
import wiringpi as wpi
wpi.wiringPiSetup()

def custom_delay(time) :
    i = 0
    for i in range(0, time//100) :
        wpi.delayMicroseconds(99)
        i += 1
    if time%100>5 :
        wpi.delayMicroseconds(time%100)
        
def transmit(sequence, pin, repeat, high, low, period_t) :
    i = 0
    wpi.pinMode(pin,1)
    for i in range(0,repeat) :
        bin_list = list(sequence)
        for bit in bin_list :
            t0 = wpi.micros()
            wpi.digitalWrite(pin,1)
            if bit == "1" :
                custom_delay(high-(wpi.micros()-t0))
            else:
                custom_delay(low-(wpi.micros()-t0))
            wpi.digitalWrite(pin,0)
            time = wpi.micros()-t0
            if period_t-time > 0 :
                custom_delay(period_t-time)
        wpi.delay(10)
        i += 1
