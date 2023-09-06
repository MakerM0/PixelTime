'''
    RX8111 RTC drive
 
    Author: M0dular
    Date:   2023-8-5
    Ver:    0.1.0
 
    https://oshwhub.com/kakaka
'''



from micropython import const
from math import log2
from gc import collect
# bus address 
RX8111_ADDR = const(0x32)

# Basic time and calendar register 
RX8111_SEC = const(0x10)
RX8111_MIN = const(0x11)
RX8111_HOUR = const(0x12)
RX8111_WEEK = const(0x13)
RX8111_DAY = const(0x14)
RX8111_MONTH = const(0x15)
RX8111_YEAR = const(0x16)
RX8111_MIN_ALARM = const(0x17)
RX8111_HOUR_ALARM = const(0x18)
RX8111_WEEK_DAY_ALARM = const(0x19)
RX8111_TIMER_COUNTER0 = const(0x1A)
RX8111_TIMER_COUNTER1 = const(0x1B)
RX8111_TIMER_COUNTER2 = const(0x1C)
RX8111_EXTENREG = const(0x1D)
RX8111_FLAGREG = const(0x1E)
RX8111_CTRLREG = const(0x1F)

RX8111_TIMESTAMP_1_1000S = const(0x20)
RX8111_TIMESTAMP_1_100S = const(0x21)
RX8111_TIMESTAMP_SEC = const(0x22)
RX8111_TIMESTAMP_MIN = const(0x23)
RX8111_TIMESTAMP_HOUR = const(0x24)
RX8111_TIMESTAMP_WEEK = const(0x25)
RX8111_TIMESTAMP_DAY = const(0x26)
RX8111_TIMESTAMP_MONTHS = const(0x27)
RX8111_TIMESTAMP_YEAR = const(0x28)
RX8111_STATUS_STAMP = const(0x29)

RX8111_EVIN_SETTING = const(0x2B)
RX8111_SEC_ALARM = const(0x2C)
RX8111_TIMER_CONTROL = const(0x2D)
RX8111_CMD_TRIG_CTRL = const(0x2E)
RX8111_COMMAND_TRIGGER = const(0x2F)

RX8111_PWR_SWITCH_CTRL = const(0x32)
RX8111_STATUS_MONITOR = const(0x33)
RX8111_TIME_STAMP_BUF_CTRL = const(0x34)
RX8111_TIME_STAMP_TRIG_CTRL = const(0x35)
RX8111_TIME_STAMP_DATA_STATUS = const(0x36)

'''
RX8111_EXT_TSEL0 BIT(0)
RX8111_EXT_TSEL1 BIT(1)
RX8111_EXT_ECP BIT(2)
RX8111_EXT_WADA BIT(3)
RX8111_EXT_TE BIT(4)
RX8111_EXT_USEL BIT(5)
RX8111_EXT_FSEL0 BIT(6)
RX8111_EXT_FSEL1 BIT(7)

RX8111_FLAG_FSTOPF BIT(0)
RX8111_FLAG_VLF BIT(1)
RX8111_FLAG_EVF BIT(2)
RX8111_FLAG_AF BIT(3)
RX8111_FLAG_TF BIT(4)
RX8111_FLAG_UF BIT(5)
RX8111_FLAG_PORF BIT(7)
'''
RX8111_CTRL_STOP =const(0)
'''
RX8111_CTRL_EIE BIT(2)
RX8111_CTRL_AIE BIT(3)
RX8111_CTRL_TIE BIT(4)
RX8111_CTRL_UIE BIT(5)

RX8111_EVIN_EOVEN BIT(1)
RX8111_EVIN_EPRUP_SEL0 BIT(2)
RX8111_EVIN_EPRUP_SEL1 BIT(3)
RX8111_EVIN_EPRDW_SEL BIT(4)
RX8111_EVIN_ET0 BIT(5)
RX8111_EVIN_ET1 BIT(6)
RX8111_EVIN_EHL BIT(7)

RX8111_TIMER_CTRL_TSTP BIT(0)
RX8111_TIMER_CTRL_TMPIN BIT(1)
RX8111_TIMER_CTRL_TBKE BIT(2)
RX8111_TIMER_CTRL_TBKON BIT(3)

RX8111_CMD_TRIG_DUMMY0 BIT(0)
RX8111_CMD_TRIG_DUMMY1 BIT(1)
RX8111_CMD_TRIG_DUMMY2 BIT(2)
RX8111_CMD_TRIG_DUMMY3 BIT(3)
RX8111_CMD_TRIG_DUMMY4 BIT(4)
RX8111_CMD_TRIG_DUMMY5 BIT(5)
RX8111_CMD_TRIG_DUMMY6 BIT(6)
RX8111_CMD_TRIG_DUMMY7 BIT(7)

RX8111_PSC_SMP_TSEL0 BIT(0)
RX8111_PSC_SMP_TSEL1 BIT(1)
RX8111_PSC_SMP_SWSEL0 BIT(2)
RX8111_PSC_SMP_SWSEL1 BIT(3)
RX8111_PSC_SMP_INIEN BIT(6)
RX8111_PSC_SMP_CHGEN BIT(7)

RX8111_PSC_SMP_CHGEN BIT(7)

RX8111_STAT_M_FVLOW BIT(1)
RX8111_STAT_M_FVCMP BIT(3)
RX8111_STAT_M_EVINMON BIT(6)
# Insert and Defined ALARM_AE 
RX8111_ALARM_AE BIT(7)

'''

class RX8111(object):
    def __init__(self,i2c):
        self.i2c = i2c
        self.tb = bytearray(1)
        self.rb = bytearray(1)
        self.buf = bytearray(7)
        self.DT = [0] * 7
        # if RX8111_ADDR in self.i2c.scan():
        #     print('RTC: rx8111 find at address: 0x%x ' %(RX8111_ADDR))
        # else:
        #     print('RTC: rx8111 not found at address: 0x%x ' %(RX8111_ADDR))
        # collect() # 

    # set reg
    def	setReg(self, reg, dat):
        self.tb[0] = dat
        self.i2c.writeto_mem(RX8111_ADDR, reg, self.tb)

    # get reg
    def	getReg(self, reg):
        self.i2c.readfrom_mem_into(RX8111_ADDR, reg, self.rb)
        return self.rb[0]


    # 将二进制编码的十进制数转换为普通十进制数
    def _bcd2dec(self, bcd) :
        """Convert binary coded decimal (BCD) format to decimal"""
        return (((bcd & 0xf0) >> 4) * 10 + (bcd & 0x0f))

    # 将十进制编码的二进制数转换为普通十进制数
    def _dec2bcd(self, dec):
        """Convert decimal to binary coded decimal (BCD) format"""
        tens, units = divmod(dec, 10)
        return (tens << 4) + units

    def WeekToBdc(self, val) :
        return 0x01 << val
 

    def WeekToNum(self, val) :
        return int(log2(val))

    
 
    def setBit(self, reg,  bit_addr):
        
        data = self.getReg(reg)
        data |= (0x01 << bit_addr)

        self.setReg(reg, data)
 

    def clearBit(self, reg,  bit_addr):
         
        data = self.getReg(reg)
        data &= ~(0x01 << bit_addr)

        self.setReg(reg, data)
 
    def datetime(self,DT=None):
        '''
            DT: year,month,day,hour,minute,second,weekday
            在Python的time.localtime()函数中，stars from Monday (0) and ends on Sunday (6)。所以星期从0开始计数，0代表星期一。
            而rx8111是从星期日开始计数，0代表星期日
            Sunday    0 0 0 0 0 0 0 1 01 h
            Monday    0 0 0 0 0 0 1 0 02 h
            Tuesday   0 0 0 0 0 1 0 0 04 h
            Wednesday 0 0 0 0 1 0 0 0 08 h
            Thursday  0 0 0 1 0 0 0 0 10 h
            Friday    0 0 1 0 0 0 0 0 20 h
            Saturday  0 1 0 0 0 0 0 0 40 h
        '''
        if DT==None:
            self.i2c.readfrom_mem_into(RX8111_ADDR, RX8111_SEC, self.buf)
            
            self.DT[0] = self._bcd2dec(self.buf[6]) + 2000 # year
            self.DT[1] = self._bcd2dec(self.buf[5]& 0x1F)# month
            self.DT[2] = self._bcd2dec(self.buf[4] & 0x3F)#  day            

            self.DT[3] = self._bcd2dec(self.buf[2] & 0x3F)#  hour
            self.DT[4] = self._bcd2dec(self.buf[1]& 0x7F)# minute
            self.DT[5] = self._bcd2dec(self.buf[0]& 0x7F)# second
            
            self.DT[6] = self.WeekToNum(self.buf[3]) # week day

            return tuple(self.DT)
        else:
            self.setBit(RX8111_CTRLREG, RX8111_CTRL_STOP)
            self.setReg(RX8111_FLAGREG, 0x00)
            
            self.buf[6] = self._dec2bcd(DT[0]%100)   # year
            self.buf[5] = self._dec2bcd(DT[1]%13)    # month
            self.buf[4] = self._dec2bcd(DT[2]%32)    # day
            
            self.buf[2] = self._dec2bcd(DT[3]%24)    # hour
            self.buf[1] = self._dec2bcd(DT[4]%60)    # minute
            self.buf[0] = self._dec2bcd(DT[5]%60)    # second
            
            self.buf[3] = self.WeekToBdc((DT[6]+1)%7)     # week day
            
            self.i2c.writeto_mem(RX8111_ADDR, RX8111_SEC, self.buf) 

            self.clearBit(RX8111_CTRLREG, RX8111_CTRL_STOP)



 

if __name__ == "__main__":
    from machine import I2C, Pin
    import time
    print('rx8111 test')
    i2c = I2C(0, scl=Pin(7), sda=Pin(8), freq=400000)
    rtc = RX8111(i2c)
    rtc.datetime((2023,8,5,16,25,59,6))
    while True:
        print(rtc.datetime())
        time.sleep(1.0)


