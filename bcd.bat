@echo off
set bcdstore=C:\boot\bcd
bcdedit.exe /create {ramdiskoptions} /d "Retire Utility"
bcdedit.exe /set {ramdiskoptions} ramdisksdidevice partition=c:
bcdedit.exe /set {ramdiskoptions} ramdisksdipath \temponekey\media\boot\boot.sdi
bcdedit.exe -create /d "Retire Utility" /application OSLOADER
for /f "tokens=3" %%A in ('bcdedit.exe -create /d "OnekeyUEFI" /application OSLOADER') do set guid1=%%A
bcdedit.exe /set %guid1% device ramdisk=[C:]\temponekey\winpe.wim,{ramdiskoptions}
bcdedit.exe /set %guid1% path \windows\system32\boot\winload.efi
bcdedit.exe /set %guid1% osdevice ramdisk=[C:]\temponekey\winpe.wim,{ramdiskoptions}
bcdedit.exe /set %guid1% systemroot \Windows
bcdedit.exe /set %guid1% winpe yes
bcdedit.exe /set %guid1% detecthal yes
bcdedit.exe /displayorder %guid1% /addlast
bcdedit.exe /default %guid1%
bcdedit.exe /timeout 0