from PCANBasic import *
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import ttk
import csv
import sys
import time
import threading
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import os
#setting up of the adapter
global PcanHandle
PcanHandle = PCAN_USBBUS1
global PcanHandle2
PcanHandle2 = PCAN_USBBUS2
global BitrateHigh
BitrateHigh = PCAN_BAUD_500K
global BitrateLow
BitrateLow = PCAN_BAUD_125K
global m_objPCANBasic1
m_objPCANBasic1 = PCANBasic()
m_objPCANBasic1.Initialize(PcanHandle, BitrateHigh)
global m_objPCANBasic2
m_objPCANBasic2 = PCANBasic()
m_objPCANBasic2.Initialize(PcanHandle2, BitrateLow)
#creating tk
win = Tk()
# Set the window title and size
width= win.winfo_screenwidth()
height= win.winfo_screenheight()
win.geometry("%dx%d" % (width, height))
win.title('Dashboard App')

global msgArrayHigh
msgArrayHigh = []
global msgArrayLow
msgArrayLow = []
global highdata
highdata = []
global RPM
RPM = 0
global speed
speed = 0
#functions
Speed_value = StringVar()
RPM_value = StringVar()
def getSpeedSliderValue():
    return Speed_value.get()
def getRPMSliderValue():
    return RPM_value.get()
def SpeedandRpm(event):
    divi = int(getSpeedSliderValue()) / 20
    current = 5 * int(divi)
    speed = 0 + current
    speed1 = int(getSpeedSliderValue())
    draw_speedometer(speed1)
    numv = int(getRPMSliderValue())
    if numv == 0:
        update_value_High('201', '0', '0', '0', '0', str(speed), '0', '0', '0')
    elif numv == 1:
        update_value_High('201', '04', '0', '0', '0', str(speed), '0', '0', '0')
    elif numv == 2:
        update_value_High('201', '08', '0', '0', '0', str(speed), '0', '0', '0')
    elif numv == 3:
        update_value_High('201', '0B', '0', '0', '0', str(speed), '0', '0', '0')
    elif numv == 4:
        update_value_High('201', '0F', '0', '0', '0', str(speed), '0', '0', '0')
    elif numv == 5:
        update_value_High('201', '13', '0', '0', '0', str(speed), '0', '0', '0')
    elif numv == 6:
        update_value_High('201', '17', '0', '0', '0', str(speed), '0', '0', '0')
    rpm = int(getRPMSliderValue())
    draw_rpm_dial(rpm)
def ENG():
    update_value_High('240','40','40','40','40','40','40','40','40')
    update_value_High('420','60','00','00','00','00','00','00','00')
def ENGClear():
    update_value_High('240','FF','FF','FF','FF','FF','FF','FF','FF')
    update_value_High('420','FF','FF','FF','FF','FF','FF','FF','FF')
def warning1():
    update_value_Low('274','04','04','04','04','04','04','04','04')
def warning3():
    update_value_Low('274', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF')
def warning2():
    update_value_Low('274', '08', '08', '08', '08', '08', '08', '08', '08')
def warning4():
    update_value_Low('274', '10', '10', '10', '10', '10', '10', '10', '10')
def wclear():
    update_value_Low('274', '00', '00', '00', '00', '00', '00', '00', '00')
def sound1():
    update_value_Low('401','04','04','04','04','04','04','04','04')
def sclear():
    update_value_Low('401', '00', '00', '00', '00', '00', '00', '00', '00')
def sound2():
    update_value_Low('401', '00', '04', '20', '24', '0C', '08', '00', '00')
def ABS():
    update_value_High('212', '98', '00', '20', '80', '01', '00', '00', '00')
def ABSClear():
    update_value_High('212', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF', 'FF')

def R1():
    update_value_Low('28F', 'FF', '00', '00', '00', '00', '00', '00', '00')

def R2():
    update_value_Low('28F', 'FF', 'FF', '00', '00', '00', '00', '00', '00')
def RClear():
    update_value_Low('28F', '00', '00', '00', '00', '00', '00', '00', '00')

def Radio():

    text = str(input1.get())
    # A CAN message is configured
    msg = TPCANMsg()
    msg2 = TPCANMsg()
    msg2.ID = 0x291
    msg.ID = 0x290  # text
    msg.MSGTYPE = PCAN_MESSAGE_STANDARD
    msg2.MSGTYPE = PCAN_MESSAGE_STANDARD
    msg.LEN = 8
    msg2.LEN = 8
    int_array = []
    char_array = list(text)
    if ((len(char_array)) <= 12 ):
        for i in range(12 - (len(char_array))):
            char_array.append(20)
            ++i
    for i in range(12):
        if char_array[i] == 20:
            temp = 20
            temp2 = format(temp, 'X')
            int_array.insert(i, temp2)
            ++i
            continue
        else:
            temp = char_array[i]
            temp1 = ord(temp)
            temp2 = format(temp1, 'X')
            int_array.insert(i, temp2)
            ++i
    msg.DATA[0] = 133
    msg2.DATA[1] = int(int_array[0], 16)
    msg2.DATA[2] = int(int_array[1], 16)
    msg2.DATA[3] = int(int_array[2], 16)
    msg2.DATA[4] = int(int_array[3], 16)
    msg2.DATA[5] = int(int_array[4], 16)
    msg2.DATA[0] = 192
    msg.DATA[1] = int(int_array[5], 16)
    msg.DATA[2] = int(int_array[6], 16)
    msg.DATA[3] = int(int_array[7], 16)
    msg.DATA[4] = int(int_array[8], 16)
    msg.DATA[5] = int(int_array[9], 16)
    msg.DATA[6] = int(int_array[10], 16)
    msg.DATA[7] = int(int_array[11], 16)
    for j in range(1000):
        m_objPCANBasic2.Write(PCAN_USBBUS2, msg2)
        m_objPCANBasic2.Write(PCAN_USBBUS2, msg)
        ++j

def SendMessageHigh():
    # A CAN message is configured
    msg = TPCANMsg()
    msg.ID = int(CANID_input.get(),16)
    msg.MSGTYPE = PCAN_MESSAGE_STANDARD
    msg.LEN = 8
    msg.DATA[0] = int(Data0.get(),16)
    msg.DATA[1] = int(Data1.get(),16)
    msg.DATA[2] = int(Data2.get(),16)
    msg.DATA[3] = int(Data3.get(),16)
    msg.DATA[4] = int(Data4.get(),16)
    msg.DATA[5] = int(Data5.get(),16)
    msg.DATA[6] = int(Data6.get(),16)
    msg.DATA[7] = int(Data7.get(),16)
    for k in range(1000):
        m_objPCANBasic1.Write(PCAN_USBBUS1, msg)
        ++k


def SendMessageLow():
    # A CAN message is configured
    msg = TPCANMsg()
    msg.ID = int(CANID_input.get(),16)
    msg.MSGTYPE = PCAN_MESSAGE_STANDARD
    msg.LEN = 8
    msg.DATA[0] = int(Data0.get(),16)
    msg.DATA[1] = int(Data1.get(),16)
    msg.DATA[2] = int(Data2.get(),16)
    msg.DATA[3] = int(Data3.get(),16)
    msg.DATA[4] = int(Data4.get(),16)
    msg.DATA[5] = int(Data5.get(),16)
    msg.DATA[6] = int(Data6.get(),16)
    msg.DATA[7] = int(Data7.get(),16)
    for l in range(1000):
        m_objPCANBasic2.Write(PCAN_USBBUS2, msg)
        ++l

data_dir = os.path.join(os.path.dirname(__file__), 'data')
def writecsv():
    canid = CANID_input.get()
    data0 = Data0.get()
    data1 = Data1.get()
    data2 = Data2.get()
    data3 = Data3.get()
    data4 = Data4.get()
    data5 = Data5.get()
    data6 = Data6.get()
    data7 = Data7.get()
    data = [[Name.get(),dropdown.get(),canid,data0,data1,data2,data3,data4,data5,data6,data7]]
    csv_path = os.path.join(data_dir, 'names.csv')
    with open(csv_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    update_names()

def readcsv():
    csv_path = os.path.join(data_dir, 'names.csv')
    with open(csv_path, 'r') as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader if row['name'] == dropdown2.get()]
        row = rows[0]
        speed = row['speed']
        if speed == 'High':
            msg = TPCANMsg()
            msg.ID = int(str(row['canid']),16)
            msg.MSGTYPE = PCAN_MESSAGE_STANDARD
            msg.LEN = 8
            msg.DATA[0] = int(str(row['data0']),16)
            msg.DATA[1] = int(str(row['data1']),16)
            msg.DATA[2] = int(str(row['data2']),16)
            msg.DATA[3] = int(str(row['data3']),16)
            msg.DATA[4] = int(str(row['data4']),16)
            msg.DATA[5] = int(str(row['data5']),16)
            msg.DATA[6] = int(str(row['data6']),16)
            msg.DATA[7] = int(str(row['data7']),16)
            for l in range(5000):
                m_objPCANBasic1.Write(PCAN_USBBUS1, msg)
                ++l
        elif speed == 'Low':
            msg2 = TPCANMsg()
            msg2.ID = int(str(row['canid']),16)
            msg2.MSGTYPE = PCAN_MESSAGE_STANDARD
            msg2.LEN = 8
            msg2.DATA[0] = int(str(row['data0']),16)
            msg2.DATA[1] = int(str(row['data1']),16)
            msg2.DATA[2] = int(str(row['data2']),16)
            msg2.DATA[3] = int(str(row['data3']),16)
            msg2.DATA[4] = int(str(row['data4']),16)
            msg2.DATA[5] = int(str(row['data5']),16)
            msg2.DATA[6] = int(str(row['data6']),16)
            msg2.DATA[7] = int(str(row['data7']),16)
            for i in range(1000):
                m_objPCANBasic2.Write(PCAN_USBBUS2, msg2)
                ++i

def inData0():
    current = int(Data0.get(), 16)
    current += 1
    Data0.delete(0, END)
    Data0.insert(0, hex(current)[2:].upper())


def deData0():
    current = int(Data0.get(), 16)
    current -= 1
    Data0.delete(0, END)
    Data0.insert(0, hex(current)[2:].upper())


def inData1():
    current = int(Data1.get(), 16)
    current += 1
    Data1.delete(0, END)
    Data1.insert(0, hex(current)[2:].upper())


def deData1():
    current = int(Data1.get(), 16)
    current -= 1
    Data1.delete(0, END)
    Data1.insert(0, hex(current)[2:].upper())


def inData2():
    current = int(Data2.get(), 16)
    current += 1
    Data2.delete(0, END)
    Data2.insert(0, hex(current)[2:].upper())


def deData2():
    current = int(Data2.get(), 16)
    current -= 1
    Data2.delete(0, END)
    Data2.insert(0, hex(current)[2:].upper())


def inData3():
    current = int(Data3.get(), 16)
    current += 1
    Data3.delete(0, END)
    Data3.insert(0, hex(current)[2:].upper())


def deData3():
    current = int(Data3.get(), 16)
    current -= 1
    Data3.delete(0, END)
    Data3.insert(0, hex(current)[2:].upper())


def inData4():
    current = int(Data4.get(), 16)
    current += 1
    Data4.delete(0, END)
    Data4.insert(0, hex(current)[2:].upper())


def deData4():
    current = int(Data4.get(), 16)
    current -= 1
    Data4.delete(0, END)
    Data4.insert(0, hex(current)[2:].upper())


def inData5():
    current = int(Data5.get(), 16)
    current += 1
    Data5.delete(0, END)
    Data5.insert(0, hex(current)[2:].upper())


def deData5():
    current = int(Data5.get(), 16)
    current -= 1
    Data5.delete(0, END)
    Data5.insert(0, hex(current)[2:].upper())


def inData6():
    current = int(Data6.get(), 16)
    current += 1
    Data6.delete(0, END)
    Data6.insert(0, hex(current)[2:].upper())


def deData6():
    current = int(Data6.get(), 16)
    current -= 1
    Data6.delete(0, END)
    Data6.insert(0, hex(current)[2:].upper())


def inData7():
    current = int(Data7.get(), 16)
    current += 1
    Data7.delete(0, END)
    Data7.insert(0, hex(current)[2:].upper())


def deData7():
    current = int(Data7.get(), 16)
    current -= 1
    Data7.delete(0, END)
    Data7.insert(0, hex(current)[2:].upper())

class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.lock = threading.Lock()

    def write(self, string):
        with self.lock:
            self.text_widget.insert(END, string)
            self.text_widget.see(END)

    def flush(self):
        self.text_widget.update_idletasks()
def update_value_High(CANID,DATA0,DATA1,DATA3,DATA2,DATA4,DATA5,DATA6,DATA7):
    found = False
    csv_path = os.path.join(data_dir, 'HighCAN.csv')
    temp_file = os.path.join(data_dir,'temp.csv')
    with open(csv_path, 'r') as file, open(temp_file, 'w', newline='') as temp:
        reader = csv.DictReader(file)
        writer = csv.DictWriter(temp, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if row['CANID'] == CANID:
                found = True
                row['DATA0'] = DATA0
                row['DATA1'] = DATA1
                row['DATA2'] = DATA2
                row['DATA3'] = DATA3
                row['DATA4'] = DATA4
                row['DATA5'] = DATA5
                row['DATA6'] = DATA6
                row['DATA7'] = DATA7
            writer.writerow(row)
    if found:
        with open(temp_file, 'r') as temp, open(csv_path, 'w', newline='') as file:
            file.write(temp.read())
    else:
        return False
def update_value_Low(CANID,DATA0,DATA1,DATA2,DATA3,DATA4,DATA5,DATA6,DATA7):
    found = False
    csv_path = os.path.join(data_dir, 'LowCAN.csv')
    temp_file = os.path.join(data_dir,'temp1.csv')
    with open(csv_path, 'r') as file, open(temp_file, 'w', newline='') as temp:
        reader = csv.DictReader(file)
        writer = csv.DictWriter(temp, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if row['CANID'] == CANID:
                found = True
                row['DATA0'] = DATA0
                row['DATA1'] = DATA1
                row['DATA2'] = DATA2
                row['DATA3'] = DATA3
                row['DATA4'] = DATA4
                row['DATA5'] = DATA5
                row['DATA6'] = DATA6
                row['DATA7'] = DATA7
            writer.writerow(row)
    if found:
        with open(temp_file, 'r') as temp, open(csv_path, 'w', newline='') as file:
            file.write(temp.read())
    else:
        return False
def sendHigh(output_box):
    while True:
        csv_path = os.path.join(data_dir, 'HighCAN.csv')
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            headers = next(reader)
            for row in reader:
                msg = TPCANMsg()
                msg.ID = int(row['CANID'],16)
                msg.MSGTYPE = PCAN_MESSAGE_STANDARD
                msg.LEN = 8
                msg.DATA[0] = int(str(row['DATA0']), 16)
                msg.DATA[1] = int(str(row['DATA1']), 16)
                msg.DATA[2] = int(str(row['DATA2']), 16)
                msg.DATA[3] = int(str(row['DATA3']), 16)
                msg.DATA[4] = int(str(row['DATA4']), 16)
                msg.DATA[5] = int(str(row['DATA5']), 16)
                msg.DATA[6] = int(str(row['DATA6']), 16)
                msg.DATA[7] = int(str(row['DATA7']), 16)
                result = m_objPCANBasic1.Write(PCAN_USBBUS1, msg)
                if (result != PCAN_ERROR_OK):
                    result = m_objPCANBasic1.GetErrorText(result)
                    print(result)
                    time.sleep(0.05)
                else:
                    output_box.insert(END,str(list(row.values())) + '\n')
                    m_objPCANBasic1.Reset(PcanHandle)
                    time.sleep(0.02)
def sendLow(output_box):
    while True:
        csv_path = os.path.join(data_dir, 'LowCAN.csv')
        with open(csv_path, 'r') as file1:
            reader1 = csv.reader(file1)
            headers = next(reader1)
            for row1 in reader1:
                # A CAN message is configured
                msg1 = TPCANMsg()
                msg1.ID = int(row1[0], 16)
                msg1.MSGTYPE = PCAN_MESSAGE_STANDARD
                msg1.LEN = 8
                msg1.DATA[0] = int(row1[1], 16)
                msg1.DATA[1] = int(row1[2], 16)
                msg1.DATA[2] = int(row1[3], 16)
                msg1.DATA[3] = int(row1[4], 16)
                msg1.DATA[4] = int(row1[5], 16)
                msg1.DATA[5] = int(row1[6], 16)
                msg1.DATA[6] = int(row1[7], 16)
                msg1.DATA[7] = int(row1[8], 16)
                result = m_objPCANBasic2.Write(PCAN_USBBUS2, msg1)
                if (result != PCAN_ERROR_OK):
                    result = m_objPCANBasic1.GetErrorText(result)
                    print(result)
                    time.sleep(0.05)
                else:
                    output_box.insert(END, str(row1) + '\n')
                    m_objPCANBasic2.Reset(PcanHandle2)
                    time.sleep(0.05)
def update_names():
    options.clear()
    csv_path = os.path.join(data_dir, 'names.csv')
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            options.append(row[0])
        dropdown2['values'] = options



def draw_rpm_dial(rpm):
    ax2.clear()

    # Draw the outer circle
    circle2 = plt.Circle((0.5, 0.5), 0.45, transform=ax2.transAxes, edgecolor="blue", facecolor="black", zorder=1)
    ax2.add_patch(circle2)

    # Draw ticks and labels
    for i in range(0, 7):
        angle = (240 - i * 35) * np.pi / 180
        x1, y1 = 0.5 + 0.4 * np.cos(angle), 0.5 + 0.4 * np.sin(angle)
        x2, y2 = 0.5 + 0.35 * np.cos(angle), 0.5 + 0.35 * np.sin(angle)
        ax2.plot([x1, x2], [y1, y2], 'w-')
        x_label, y_label = 0.5 + 0.28 * np.cos(angle), 0.5 + 0.28 * np.sin(angle)
        ax2.text(x_label, y_label, str(i), fontsize=12, ha='center', va='center',color='white')

    # Draw needle
    angle = (240 - rpm * 35) * np.pi / 180
    x, y = 0.5 + 0.3 * np.cos(angle), 0.5 + 0.3 * np.sin(angle)
    ax2.plot([0.5, x], [0.5, y], 'r-', linewidth=2)
    ax2.add_patch(plt.Circle((0.5, 0.5), 0.02, color='red'))
    ax2.text(0.5, 0.15, 'RPM', fontsize=16, ha='center', va='center', color='white')
    # Remove borders and ticks
    ax2.axis('equal')
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.axis('off')
    canvas2.draw()

def draw_speedometer(speed):
    ax.clear()

    # Draw the outer circle
    circle = plt.Circle((0.5, 0.5), 0.45, transform=ax.transAxes, edgecolor="blue", facecolor="black", zorder=1)
    ax.add_patch(circle)

    # Draw ticks and labels
    for i in range(0, 241, 20):
        angle = (240 - i) * np.pi / 180
        x1, y1 = 0.5 + 0.4 * np.cos(angle), 0.5 + 0.4 * np.sin(angle)
        x2, y2 = 0.5 + 0.35 * np.cos(angle), 0.5 + 0.35 * np.sin(angle)
        ax.plot([x1, x2], [y1, y2], 'w-')
        x_label, y_label = 0.5 + 0.32 * np.cos(angle), 0.5 + 0.32 * np.sin(angle)
        ax.text(x_label, y_label, str(i), fontsize=8, ha='center', va='center',color='white')

    # Draw needle
    angle = (240 - speed) * np.pi / 180
    x, y = 0.5 + 0.3 * np.cos(angle), 0.5 + 0.3 * np.sin(angle)
    ax.plot([0.5, x], [0.5, y], 'r-', linewidth=2)
    ax.add_patch(plt.Circle((0.5, 0.5), 0.02, color='red'))
    ax.text(0.5, 0.15, 'KM/H', fontsize=16, ha='center', va='center', color='white')

    # Remove borders and ticks
    ax.axis('equal')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    canvas1.draw()


##########################################################################
style = ttk.Style()
style.configure("Black.TFrame", background="Black")
tab_control = ttk.Notebook(win)

tab1 = ttk.Frame(tab_control,style="Black.TFrame")
tab2 = ttk.Frame(tab_control,style="Black.TFrame")

tab_control.add(tab1, text='Dashboard')
tab_control.add(tab2, text='Reverse Engineering')

def validate_data(text):
    if len(text) > 2:
        return False
    return True
def validate_CANID(text):
    if len(text) > 3:
        return False
    return True
group9 = LabelFrame(tab2, text='Self Reverse Engineering', width=500, height=200)
group9.place(x=60, y=30)
validate_command1 = group9.register(validate_data)
validate_command2 = group9.register(validate_CANID)
CANid = Label(group9, text="CAN ID (hex):")
CANid.place(x=10, y=10)
CANID_input = Entry(group9, width=10,validate='key',validatecommand=(validate_command2, '%P'))
CANID_input.insert(END, '000')
CANID_input.place(x=10, y=30)
Data_Label = Label(group9, text="Data (hex):")
Data_Label.place(x=110, y=10)
Data0 = Entry(group9, width=5,validate='key',validatecommand=(validate_command1, '%P'))
Data0.insert(END, '0')
Data0.place(x=110, y=30)
Data0in = Button(group9, text="+", command=inData0)
Data0in.place(x=110,y=50)
Data0de = Button(group9, text="-", command=deData0)
Data0de.place(x=130,y=50)
Data1 = Entry(group9, width=5,validate='key',validatecommand=(validate_command1, '%P'))
Data1.insert(END, '0')
Data1.place(x=150, y=30)
Data1in = Button(group9, text="+", command=inData1)
Data1in.place(x=150,y=50)
Data1de = Button(group9, text="-", command=deData1)
Data1de.place(x=170,y=50)
Data2 = Entry(group9, width=5,validate='key',validatecommand=(validate_command1, '%P'))
Data2.insert(END, '0')
Data2.place(x=190, y=30)
Data2in = Button(group9, text="+", command=inData2)
Data2in.place(x=190,y=50)
Data2de = Button(group9, text="-", command=deData2)
Data2de.place(x=210,y=50)
Data3 = Entry(group9, width=5,validate='key',validatecommand=(validate_command1, '%P'))
Data3.insert(END, '0')
Data3.place(x=230, y=30)
Data3in = Button(group9, text="+", command=inData3)
Data3in.place(x=230,y=50)
Data3de = Button(group9, text="-", command=deData3)
Data3de.place(x=250,y=50)
Data4 = Entry(group9, width=5,validate='key',validatecommand=(validate_command1, '%P'))
Data4.insert(END, '0')
Data4.place(x=270, y=30)
Data4in = Button(group9, text="+", command=inData4)
Data4in.place(x=270,y=50)
Data4de = Button(group9, text="-", command=deData4)
Data4de.place(x=290,y=50)
Data5 = Entry(group9, width=5,validate='key',validatecommand=(validate_command1, '%P'))
Data5.insert(END, '0')
Data5.place(x=310, y=30)
Data5in = Button(group9, text="+", command=inData5)
Data5in.place(x=310,y=50)
Data5de = Button(group9, text="-", command=deData5)
Data5de.place(x=330,y=50)
Data6 = Entry(group9, width=5,validate='key',validatecommand=(validate_command1, '%P'))
Data6.insert(END, '0')
Data6.place(x=350, y=30)
Data6in = Button(group9, text="+", command=inData6)
Data6in.place(x=350,y=50)
Data6de = Button(group9, text="-", command=deData6)
Data6de.place(x=370,y=50)
Data7 = Entry(group9, width=5,validate='key',validatecommand=(validate_command1, '%P'))
Data7.insert(END, '0')
Data7.place(x=390, y=30)
Data7in = Button(group9, text="+", command=inData7)
Data7in.place(x=390,y=50)
Data7de = Button(group9, text="-", command=deData7)
Data7de.place(x=410,y=50)
lowsend = Button(group9, text="send Low", width=7, command=SendMessageLow)
lowsend.place(x=330, y=80)
highsend = Button(group9, text="send High", width=7, command=SendMessageHigh)
highsend.place(x=390, y=80)
NameLabel = Label(group9,text='Enter Name:')
NameLabel.place(x=180, y=120)
Name = Entry(group9, width=10)
Name.place(x=250, y=120)
options = ['High','Low']
dropdown = Combobox(group9)
dropdown['values'] = options
dropdown.configure(width=5)
dropdown.place(x=315,y=115)
Save = Button(group9, text="Save",command=writecsv)
Save.place(x=390, y=115)

group10 = LabelFrame(tab2, text='Sending your own messages', width=300, height=200)
group10.place(x=600, y=30)
options = []
dropdown2 = Combobox(group10)
update_names()
dropdown2['values'] = options
dropdown2.configure(width=10)
dropdown2.place(x=95,y=30)
Send = Button(group10, text="Send",command=readcsv)
Send.place(x=95, y=80)


group11 = LabelFrame(tab1, text='console output', width=300, height=200)
group11.place(x=1200, y=610)
output_box = Text(group11)
output_box.config(state=NORMAL, font=("Courier", 12), width=60, height=10, foreground='white', background='black')
scrollbar = Scrollbar(group11)
scrollbar.pack(side=RIGHT,fill=Y)
output_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=output_box.yview)
output_box.pack()
sys.stdout = StdoutRedirector(output_box)
sys.stderr = StdoutRedirector(output_box)


tab_control.pack(expand=1, fill="both")
enginepath = os.path.join(data_dir, 'engine.png')
engineimg = PhotoImage(file=enginepath)
enginebtn = Button(tab1, image=engineimg,bd=0, command=ENG)
enginebtn.place(x=60, y=50)

ABSpath = os.path.join(data_dir, 'ABS.png')
ABSimg = PhotoImage(file=ABSpath)
ABSbtn = Button(tab1, image=ABSimg,bd=0, command=ABS)
ABSbtn.place(x=60, y=160)

radio1path = os.path.join(data_dir, 'radio1.png')
radio1img = PhotoImage(file=radio1path)
radio1btn = Button(tab1, image=radio1img,bd=0, command=R1)
radio1btn.place(x=60, y=280)

radio2path = os.path.join(data_dir, 'radio2.png')
radio2img = PhotoImage(file=radio2path)
radio2btn = Button(tab1, image=radio2img,bd=0, command=R2)
radio2btn.place(x=60, y=380)

def validate_text(text):
    if len(text) > 12:
        return False
    return True
validate_command3 = tab1.register(validate_text)
Label1 = Label(tab1,text='Enter Text',font=('COWBOYS', 18),bg='black',foreground='white')
Label1.place(x=840, y=600)
input1 = Entry(tab1,validate='key', validatecommand=(validate_command3, '%P'),width=11,font=('COWBOYS', 36),bg='#ff8534')
input1.place(x=750, y=640)
submitpath = os.path.join(data_dir, 'submit.png')
submitimg = PhotoImage(file=submitpath)
RadioSubmit = Button(tab1, image=submitimg, bd=0, command=Radio)
RadioSubmit.place(x=800, y=710)

waring1path = os.path.join(data_dir, 'warning1.png')
waring1img = PhotoImage(file=waring1path)
warning1btn = Button(tab1, image=waring1img,bd=0, command=warning1)
warning1btn.place(x=1650, y=20)
waring2path = os.path.join(data_dir, 'warning2.png')
waring2img = PhotoImage(file=waring2path)
warning2btn = Button(tab1, image=waring2img,bd=0, command=warning2)
warning2btn.place(x=1650, y=85)
waring3path = os.path.join(data_dir, 'warning3.png')
waring3img = PhotoImage(file=waring3path)
warning3btn = Button(tab1, image=waring3img,bd=0, command=warning3)
warning3btn.place(x=1650, y=150)
waring4path = os.path.join(data_dir, 'warning4.png')
waring4img = PhotoImage(file=waring4path)
warning4btn = Button(tab1, image=waring4img,bd=0, command=warning4)
warning4btn.place(x=1650, y=215)

sound1path = os.path.join(data_dir, 'sound1.png')
sound1img = PhotoImage(file=sound1path)
sound1btn = Button(tab1, image=sound1img,bd=0, command=sound1)
sound1btn.place(x=1680, y=300)
sound2path = os.path.join(data_dir, 'sound2.png')
sound2img = PhotoImage(file=sound2path)
sound2btn = Button(tab1, image=sound2img,bd=0, command=sound2)
sound2btn.place(x=1680, y=380)

engineresetpath = os.path.join(data_dir, 'enginereset.png')
engineresetimg = PhotoImage(file=engineresetpath)
engineresetbtn = Button(tab1, image=engineresetimg,bd=0, command=ENGClear)
engineresetbtn.place(x=125, y=613)

absresetpath = os.path.join(data_dir, 'absreset.png')
absresetimg = PhotoImage(file=absresetpath)
absresetbtn = Button(tab1, image=absresetimg,bd=0, command=ABSClear)
absresetbtn.place(x=260, y=690)

soundresetpath = os.path.join(data_dir, 'hornreset.png')
soundresetimg = PhotoImage(file=soundresetpath)
soundresetbtn = Button(tab1, image=soundresetimg,bd=0, command=sclear)
soundresetbtn.place(x=30, y=690)

radioresetpath = os.path.join(data_dir, 'radioreset.png')
radioresetimg = PhotoImage(file=radioresetpath)
radioresetbtn = Button(tab1, image=radioresetimg,bd=0, command=RClear)
radioresetbtn.place(x=260, y=760)

warningresetpath = os.path.join(data_dir, 'warningreset.png')
warningresetimg = PhotoImage(file=warningresetpath)
warningresetbtn = Button(tab1, image=warningresetimg,bd=0, command=wclear)
warningresetbtn.place(x=30, y=760)



fig, ax = plt.subplots(figsize=(4, 4),facecolor='black')
canvas1 = FigureCanvasTkAgg(fig, master=tab1)
canvas1.get_tk_widget().place(x=1000,y=40)
slider = Scale(tab1, from_=0, to=240, resolution=20, length=300, orient=HORIZONTAL, command=SpeedandRpm, variable=Speed_value, tickinterval=20, fg='white', bg='black')
slider.place(x=1050,y=440)
draw_speedometer(0)
fig2, ax2 = plt.subplots(figsize=(4, 4),facecolor='black')
canvas2 = FigureCanvasTkAgg(fig2, master=tab1)
canvas2.get_tk_widget().place(x=550,y=40)
slider2 = Scale(tab1, from_=0, to=6, orient=HORIZONTAL,command=SpeedandRpm,variable=RPM_value, resolution=1, length=300,tickinterval=1, fg='white', bg='black')
slider2.place(x=600,y=440)
draw_rpm_dial(0)


thread1 = threading.Thread(target=sendHigh,args=(output_box,))
thread1.start()
thread2 = threading.Thread(target=sendLow, args=(output_box,))
thread2.start()
win.mainloop()