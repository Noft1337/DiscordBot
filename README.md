# DiscordBot
### A Discord Bot I created in order to play YouTube songs on  Discord 
I mainly made this bot to play One Piece openings and carried on improving it for fun :)
Hope you enjoy it! 

# Requirements
## pip packages
``` 
pynacl
discord
youtube_dl
ffmpeg 
```

## Other requirements
### Chocolatey (Windows only)
In order to run ffmpeg on our machine we need to install it first (obviously)
We install it using the choco package manager.
To install choco run this command on PS with admin priveleges:
```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'));Set-ExecutionPolicy Restricted -Scope Process -Force
```

### Install ffmpeg
####  Windows
On PowerShell:
```
choco install ffmpeg
cp C:\ProgramData\chocolatey\bin\ffmpeg.exe $env:LOCALAPPDATA\Programs\Python\Python39\Scripts
```
#### Linux
```
apt-get install ffmpeg
```
