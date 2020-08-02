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
