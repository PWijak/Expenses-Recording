
from tkinter import * # * will imported only main file, not included sub-file
from tkinter import ttk, messagebox # messagebox is pop-up error message
import csv
from datetime import datetime #import current time stamp

## GUI Structure ##
#GUI
  #Tab1 (T1)
	#Frame1 (F1)
	  #Label1 (L1)
	#Element1 (E1)
  #Tab2

# grid ใช้กับ column, row ==> ใช้กับ pack ไม่ได้
# pack ใช้วางจากบนลงล่าง
# place ใช้ในการปรับระยะ x,y


GUI = Tk()
GUI.title('Expenses Recording')
GUI.geometry('650x750+500+30')



############### Create Menu Bar ########################
menubar = Menu(GUI) #Menu is from import *
GUI.config(menu=menubar)

# File menu
filemenu = Menu(menubar,tearoff=0) #tearoff = 0 is off pop-up dialog
menubar.add_cascade(label='File',menu=filemenu) # Define : File menu name
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to Googlesheet')

# Help menu

def About():
	messagebox.showinfo('About','Created by P.Wijak')

helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu) # Define : Help menu name
helpmenu.add_command(label='About Information',command = About) #command is calling function About

# Help menu
def Donate():
	messagebox.showinfo('About','If you would like to donate, please contact me\n \t   Thank you')

donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu) # Define : Help menu name
donatemenu.add_command(label='Donate Information',command = Donate) #command is calling function About
########################################################


#Create Tabs : Notebook
Tab = ttk.Notebook(GUI)
T1 = Frame(Tab) #Can add width and heigh
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand = 1) #fill = both ; extend x and y axis | expand = 1 ;extend screen and using with fill function

#Add photo into the tab
t1_icon = PhotoImage(file='t1_expense.png') #.subsample(2) ใช้การย่อรูป 2 เท่า ใช้กับ .png ได้เท่านั้น
t2_listicon = PhotoImage(file='t2_expenselist.png')

#Tab with picture
Tab.add(T1, text=f'{"Add Expense" : ^{50}}', image=t1_icon,compound='top') 
Tab.add(T2, text=f'{"Expense list" : ^{50}}', image=t2_listicon,compound='top')
#text = f'{}' ; f-string ^ 50 is move the name to middle and space is 50
#compound is control picture where it should be
F1 = Frame(T1)
F1.pack()
#F1.place(x=20,y=50)

days = {'Mon' : 'จันทร์',
	'Tue' : 'อังคาร',
	'Wed' : 'พุธ',
	'Thu' : 'พฤหัส',
	'Fri' : 'ศุกร์',
	'Sat' : 'เสาร์',
	'Sun' : 'อาทิตย์'}



def Save(event = None): #event = None คือการ set ค่า defalut เป็น None
	expense = v_expense.get() #.get() คือดึงค่าจาก v_expense = StringVar()
	price = v_price.get()
	piece = v_piece.get()

	if expense == '':
		#print('ไม่มีข้อมูล กรุณากรอกข้อมูลใหม่')
		print('No Data')
		messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่ายให้ครบ')
		v_expense.set('') #Clear expense to ' '
		v_price.set('') #Clear price to ' '
		v_piece.set('')
		#E1.focus() # Move cluster to expense fill
		return

	elif price == '':
		messagebox.showwarning('Error','กรุณากรอกข้อมูลราคาให้ครบ')
		v_expense.set('') #Clear expense to ' '
		v_price.set('') #Clear price to ' '
		v_piece.set('')
		#E1.focus()
		return

	elif piece == '':
		messagebox.showwarning('Error','กรุณากรอกข้อมูลจำนวนให้ครบ')
		v_expense.set('') #Clear expense to ' '
		v_price.set('') #Clear price to ' '
		v_piece.set('')
		#E1.focus()
		return


	try :
		overall = float(price)*int(piece)
 
		#Clear
		v_expense.set('') #Clear expense to ' '
		v_price.set('') #Clear price to ' '
		v_piece.set('')
		
		#Time setting
		dt = datetime.now() # Time Stamp
		today = dt.strftime('%a') #days['Mon'] = 'จันทร์'
		date_time = dt.strftime('%Y-%m-%d   %H:%M:%S') # Show Date and Time Stamp
		date_time = days[today]+'-'+date_time

		print(' Date : {} \n รายการ: {} \n ราคา: {} บาท \n จำนวน: {} ชิ้น\n รวมทั้งหมด: {} บาท\n บันทึกแล้ว'.format(date_time,expense,price,piece,overall))
		text = ' Date : {} \n รายการ: {} \n ราคา: {} บาท \n จำนวน: {} ชิ้น\n รวมทั้งหมด: {} บาท\n บันทึกแล้ว'.format(date_time,expense,price,piece,overall)
		#text = text + 'จำนวน ...'
		v_result.set(text) #Show result

		#บันทึกข้อมูลลง csv
		with open('Expense data.csv','a',encoding='utf-8',newline='')  as f: #'a' เพิ่มข้อมูลจากข้อมูลเก่า (Append), 'w' คือจะ save ทับค่าเก่า
														#utf-8 คือสามารถ save เป็นภาษาไทยได้
														#with คือสั่งเปิดไฟล์แล้วปิดอัตโนมัติ
														#newline = '' ทำให้ข้อมูลไม่มีบรรทัดว่าง
			fw = csv.writer(f) #สร้างฟังก์ชั่นสำหรับเขียนข้อมูล
			data = [date_time,expense,price,piece,overall]
			fw.writerow(data)

		#ทำให้ เคอเซอร์ กลับไปที่ E1
		E1.focus()
		update_table()
		

	except Exception as e:
		#print('ERROR: {}'.format(e)) 
		print('ERROR:',e) #Show error as e
		#messagebox.showerror('Error','คุณกรอกข้อมูลผิด กรุณากรอกข้อมูลใหม่ ') # the first coma is topic pop-up     
		messagebox.showwarning('Error','คุณกรอกข้อมูลผิด กรุณากรอกข้อมูลใหม่ ')
		#messagebox.showinfo('Error','คุณกรอกข้อมูลผิด กรุณากรอกข้อมูลใหม่ ')

		#Clear data
		v_expense.set('') #Clear expense to ' '
		v_price.set('') #Clear price to ' '
		v_piece.set('')


#ทำให้สามารถกดปุ่ม Enter ได้
GUI.bind('<Return>',Save)  #ต้องเพิ่มใน def Save เป็น Save(event =None) ด้วย
					#GUI.bind เป็นการเช็คว่ามีการกดปุ่ม return หรือไม่
	
FONT1 = (None,20) # None is Front, 20 is size

#---------Image------------
main_icon = PhotoImage(file='icon_money.png')
logo = Label(F1,image=main_icon)
logo.pack()

#------text1 : รายการค่าใช้จ่าย---------
L = ttk.Label(F1,text = 'รายการค่าใช้จ่าย',font = FONT1).pack()

v_expense = StringVar() # StringVar() ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font = FONT1)
E1.pack()
#--------------------

#------text2 : ราคา---------
L = ttk.Label(F1,text = 'ราคา (บาท)',font = FONT1).pack()

v_price= StringVar() # StringVar() ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1,textvariable=v_price,font = FONT1)
E2.pack()
#--------------------

#------text3 : จำนวน---------
L = ttk.Label(F1,text = 'จำนวน (ชิ้น)',font = FONT1).pack()

v_piece= StringVar() # StringVar() ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1,textvariable=v_piece,font = FONT1)
E3.pack()
#--------------------

b1_icon = PhotoImage(file='b_save.png')

B2 = ttk.Button(F1,text=f'{"Save": >{15}}', command=Save,image=b1_icon,compound='left')
B2.pack(pady=20, ipadx=50,ipady=20)

#Show the result on the screen
v_result = StringVar()
v_result.set('-------ผลลัพธ์--------')
result = ttk.Label(F1, textvariable=v_result, font=FONT1, foreground='green')
#result = ttk.Label(F1, textvariable=v_result, font=FONT1, fg='green') >> Using with normal label
result.pack(pady=20)


#############  TAB2  ###################

def read_csv(): #Function with 'with'
	
	#global rs #Define global variable

	with open('Expense data.csv',newline='',encoding='utf-8') as f: #mode = 'a' or 'w' ใช้กับ wirter , utf-8 read ภาษาไทย
		fr = csv.reader(f) #fr is file reader
		data = list(fr) #Transform data address to list for able to read the data as list
		# print(data)
		# print(data[0][0])
		# for a,b,c,d,e in data: 
		# 	print(b)			#Can show list which you interest in the sub list
	return data #We need get data to continous to use

	# Function without 'with' (When user open the file, the program will error)
	# f = open('savedata.csv',newline='',encoding='utf-8')
	# fr = csv.reader(f)
	# f.close() #Must close the file before run again

# read_csv()
# rs = read_csv()
# print(rs)

#Table
L = ttk.Label(T2,text = 'ตารางแสดงผลลัพธ์ทั้งหมด',font = FONT1).pack(pady = 20)

header = ['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2, columns=header, show='headings',height=20) # show headings is main topic as tabs | height is number of the list
resulttable.pack()
#Show table without header and fixed size

### Manual header defination
# resulttable.heading(header[0],text='header[0]')
# resulttable.heading(header[1],text='header[1]')
# resulttable.heading(header[2],text='header[2]')
# resulttable.heading(header[3],text='header[3]')
# resulttable.heading(header[4],text='header[4]')

### For loop header defination
# for i in range(len(header)):
# 	resulttable.heading(header[i],text='header[i]')

### Run data in list
for hd in header:
	resulttable.heading(hd,text=hd)

headerwidth = [150,170,80,80,80] #The unit is pixcel

# resulttable.column('วัน-เวลา',width = 10) #Define and set format the header

# for i in range(len(header)):
# 	print(header[i], headerwidth[i])

# zip(header,headerwidth) #จับคู่กันข้อมูลกัน
# list(zip(header,headerwidth))

# enumerate() #จับคู่กันเป็นการเรียงอันดับ
# for i,d in enumerate(zip(header,headerwidth)):
# 	print(i,d)

for hd,W in zip(header, headerwidth): #zip = จับคู่กันข้อมูลกัน
	resulttable.column(hd,width=W)


# def update_record():
# 	getdata = read_csv()
# 	v_allrecord.set('') #Reset a new data
# 	text = ''
# 	for d in getdata:
# 		txt = '{}---{}---{}---{}---{}\n'.format(d[0],d[1],d[2],d[3],d[4]) #Call each lists
# 		text = text + txt

# 	v_allrecord.set(text)

# # Put data in the table
# v_allrecord = StringVar()
# v_allrecord.set('----------All Record----------')
# Allrecord = ttk.Label(T2,textvariable=v_allrecord,font=(None,15),foreground='green')
# Allrecord.pack()

######################################################
# การหยอดข้อมูล
# resulttable.insert('','end',value=['จันทร์','น้ำดื่ม',30,5,150]) #value ต้องมีจำนวนข้อมูลเท่ากับ header / 'end' = จะเรียงจากข้อมูลมาก่อนไปยังล่าสุด แต่ 0 จะเรียงจากล่าสุดไปยังก่อนหน้านี้
# resulttable.insert('',0,value=['จันทร์','น้ำดื่ม',30,5,150]) 

def update_table():

	# for c in resulttable.get_children():
	# 	resulttable.delete(c)
	resulttable.delete(*resulttable.get_children()) # Delete data previous data | * is stand for for-loop
	
	getdata = read_csv()
	for dt in getdata:
		resulttable.insert('',0,value=dt) #'' = ตัวแรกสุด



update_table()
#print('GET CHILD:',resulttable.get_children())

# update_record()
GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()
