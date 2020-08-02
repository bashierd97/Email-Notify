# System Notification System

An email notifcation system notifying user's about info about their system.

## REQUIREMENTS PRIOR TO RUNNING THE SCRIPT 

**PLEASE DO THESE BEFORE YOU EDIT & RUN THE SCRIPT**

First thing's first, we need to create a test **GMAIL** email and configure it for development. The script will use this and send emails from it. It doesn't matter what you name it, it's essentially just a *fake* email that'll send you notifications. 

- [Create a new Gmail account here](https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp)
  - *No need to enter a phone number nor a backup email, remember this is just a throwaway account*
  - I named mine bdahman.test@gmail.com
- [Turn Less Secure App Access to ON](https://myaccount.google.com/lesssecureapps)

Following that, we need to register for an account to be able to use our weather API and get an API key.

- Register for an openweathermap account [HERE](https://home.openweathermap.org/users/sign_up)
  - Once registered, confirm your email (they should send you a confirmation email)
  - Click the section **API Keys** and copy your key
  - Open up 'info.txt' and replace [API KEY HERE (Will be 32 Characters)] with your key.
  
From there we can start filling up our own values inside info.txt

Make sure to **NOT** insert any quotations in any of the values in info.txt, as they're not strings. The script will just read the lines and insert them directly. Ignore the lines beginning with '#' those are just comments.

- Replace API Key
- Replace City Name
- Replace Sender Email Address (AKA your throwaway email address)
- Replace Sender Email Password (AKA your throwaway email password)
- Replace Reciever Email Address (AKA your REAL email address, that you want all notifications to go to)

*Should like this once complete: (**NOTE**: some values may be fake, please do not copy)*

#ENTER YOUR WEATHER API KEY HERE <br />
1037854g16a058e79820fc209p4e7116 <br />
#ENTER YOUR CURRENT CITY HERE <br />
San Diego <br />
#ENTER THE SENDER EMAIL HERE [Gmail Domain] <br />
bdahman.test@gmail.com <br />
#ENTER THE SENDER EMAIL PASSWORD HERE <br />
password90 <br />
#ENTER THE RECIEVER EMAIL HERE (YOUR REAL EMAIL) <br />
bashierd97@gmail.com <br />

### Install the Proper Modules

To install the required modules use ```pip install -r required_modules.txt```

## Automate Script to execute every Midnight 

**_Linux_** <br />
As mentioned before I used my Raspberry Pi Zero W, to allow my script to run every night at 12:00 AM. On a Linux Machine, you can easily do this by opening your command line and typing ```crontab -e``` (no need for the .bat file) and inserting a new line as shown:
```0 0 * * *  python3 /home/pi/Projects/system_notif.py``` of course, you may have to replace python3 to wherever your python3 executable is on your machine. Unless it's on your system PATH, then you should be fine with just having "python3" and change /home/pi/Projects/system_notif.py to /wherever/the/path/is_to/system_notify.py. The 0 0 * * * means at exactly, 12:00 AM at midnight run the following commands, every day.

Be sure to check the cron job is successfully running ```crontab -l```, and see if the command is correct.

**_Windows_** <br />
On a Windows machine, right click on 'notify_schedule.bat' and click edit. Choose your preferred editor, I used Notepad. From there you'll see the following two lines ```"python3" "C:\Users\bashi\Desktop\system_notify.py"```, if 'python3' is not on your system PATH, be sure to find python3.exe on your machine, and substitute the ENTIRE path with python3. Also, substitute the path to system_notify.py to wherever it's located on your machine, and save the editted file.

Following that, in your Windows search bar, search for Task Scheduler and **Run as Administrator**. Once open, under the Actions tab, click Create Basic Task, name your task to whatever you'd like, you may put a brief description if you'd want as well. Following that, set the Trigger as Daily, and have it start on the following day at 12:00:00 AM (example, if today is 8/1/20, I set the start to 8/2/20, since midnight is the next day technically). Under Action, have it as "Start a Program", locate your notify_schedule.bat file and select it. On the Finish section, make sure everything looks correct and hit Finish and TADA! Every night at midnight the script will run!

## To Run Manually
To just run the script manually use ```python3 system_notify.py```

### You're all set now, Congratualtions!
