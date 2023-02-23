import subprocess
import linecache
import os
import shutil
import tkinter
import customtkinter
import threading
import ctypes
from tkinter import filedialog
from tkinter import messagebox as mb
def call():
    res = mb.askquestion('Preparing done', 
                         'Do you want to restart now to continue?')
      
    if res == 'yes' :
    	os.system("shutdown /r /t 0")
def run():
	try:
		temp.configure(text="Preparing")
		gho = ghobrowse2.cget("text")
		newpath = r'C:\\temp1' 
		if not os.path.exists(newpath):
		    os.makedirs(newpath)
		newpath = r'C:\\temponekey' 
		if not os.path.exists(newpath):
		    os.makedirs(newpath)
		else:
			diskfile1 = open("dism1.bat", "w+")
			dism1 = "DISM /unmount-wim /MountDir:c:\\temponekey /discard" 
			diskfile1.write("@echo off\n" + dism1+ "\n" + "dism /cleanup-wim")
			diskfile1.close()
			subprocess.run(["dism1.bat"])
			shutil.rmtree(newpath)

		shutil.copyfile("winpe.wim", "C:\\temp1\\winpe.wim")
		diskfile1 = open("dism1.bat", "w+")
		dism = "DISM /Mount-Wim /WimFile:C:\\temp1\\winpe.wim /index:1 /MountDir:c:\\temponekey"
		diskfile1.write("@echo off\n" + dism)
		diskfile1.close()
		subprocess.run(["dism1.bat"])

		output = open('shell_output.txt', 'w+') 
		subprocess.run('powershell Get-Disk -Partition (Get-Partition -DriveLetter C)', shell=True, stdout=output) 
		diskindex = linecache.getline(r"shell_output.txt", 5)[0]
		output2 = open('shell_output2.txt', 'w+') 
		subprocess.run('powershell Get-Partition -DriveLetter C', shell=True, stdout=output2) 
		partindex = linecache.getline(r"shell_output2.txt", 7)[0]
		diskindex = int(diskindex) +1
		partindex = int(partindex) -1
		gho2 = str(diskindex) + ":" + str(partindex)
		output.close()

		ghodir = gho[0]
		output = open('shell_output.txt', 'w+') 
		subprocess.run('powershell Get-Disk -Partition (Get-Partition -DriveLetter ' + ghodir + ")", shell=True, stdout=output) 
		disk2index = linecache.getline(r"shell_output.txt", 5)[0]
		output2 = open('shell_output2.txt', 'w+') 
		subprocess.run('powershell Get-Partition -DriveLetter '+ ghodir + ")", shell=True, stdout=output2) 
		part2index = linecache.getline(r"shell_output2.txt", 7)[0]
		output.close()
		part2index = int(part2index) -1
		diskfile2 = open("C:\\temponekey\\Windows\\System32\\disk.txt", "w+")
		diskfile2.write("sel disk " + str(disk2index) + "\n" + "sel vol " + str(part2index) + "\n" + "assign letter=Z\n" + "sel disk " + str(int(diskindex -1)) + "\n" "sel vol " + str(int(partindex - 1)) + "\n" + "assign letter=C")
		diskfile2.close() 
		diskfile = open("C:\\temponekey\\Windows\\System32\\startnet.cmd", "w+")
		diskfile.write("@echo off\n" + "wpeinit\n" + "diskpart /s disk.txt\n" "ghost.exe -clone,mode=pload,src=" + "\"" + str(gho.replace(ghodir, "Z"))+ "\"" +":1" + ",dst=" + str(gho2) + " -batch -sure\n" + "bcdboot C:\\Windows\n" + "bcdedit.exe /delete {current}\n" + "wpeutil reboot") 
		diskfile.close() 
		shutil.copyfile("ghost.exe", "C:\\temponekey\\Windows\\System32\\ghost.exe")
		diskfile = open("dism1.bat", "w+")
		dism = "DISM /unmount-wim /MountDir:c:\\temponekey /commit"
		diskfile.write("@echo off\n" + dism+ "\n" + "dism /cleanup-wim")
		diskfile.close()
		subprocess.run(["dism1.bat"])
		shutil.copyfile("C:\\temp1\\winpe.wim", "C:\\temponekey\\winpe.wim")
		shutil.copytree("Media", "C:\\temponekey\\Media") 
		shutil.rmtree("C:\\temp1")
		subprocess.run(["bcd.bat"])
		temp.configure(text="Done!")
		call()
	except:
		temp.configure(text="An error occurred")
		ctypes.windll.user32.MessageBoxW(0, "An error occurred", "GhoToWIM", 0)
def choosegho():
  ghostdir = filedialog.askopenfilename(filetypes=[('Norton Ghost (*.gho)', '*.gho')], defaultextension='.gho')
  ghobrowse2.configure(text=ghostdir) 
def checkadmin():
	try:
		admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
	except:
		admin = False
	if not admin:
		ctypes.windll.shell32.ShellExecuteW(None,u"runas",sys.executable,__file__,None,1)
		sys.exit()
def start():
  threading.Thread(target=run).start()

checkadmin()
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")
app = customtkinter.CTk()
app.geometry("400x300")
app.title("OnekeyUEFI")
ghobrowse = customtkinter.CTkButton(app, text="Choose GHO file", command=choosegho)
ghobrowse.pack(padx=10, pady=10)
ghobrowse2 = customtkinter.CTkLabel(app, text="")
ghobrowse2.pack(padx=10, pady=10)
temp = customtkinter.CTkLabel(app, text="")
temp.pack(padx=10, pady=10)
start = customtkinter.CTkButton(app, text="Start", command=start)
start.pack(padx=10, pady=10)
temp = customtkinter.CTkLabel(app, text="Made with ♥ by Random Tech Channel")
temp.pack(padx=10, pady=10)
app.mainloop()

