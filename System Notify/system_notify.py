# Bashier Dahman: system_notify.py Script
# Be sure to change email / password (Sender)
# Be sure to change email (Reciever) 
# In the text file "info.txt"


# import all the modules I will be using
import smtplib, ssl, getpass, socket, requests, json
import psutil, platform
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

########################################################
# remote server for checking internet connection
REMOTE_SERVER = "one.one.one.one"

# function to check if pi is connected to internet
def is_connected(hostname):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except:
     pass
  return False
########################################################
########################################################

# function to return IP
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        # close socket
        s.close()
    return IP
    
########################################################
########################################################
# function to get size
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return '%.2f%s%s' % (round(bytes,2), unit, suffix)
        bytes /= factor
########################################################
########################################################
# This will get all the System Info 
uname = platform.uname()

system_name = uname.system
system_node = uname.node
system_release = uname.release
system_version = uname.version
system_machine = uname.machine
system_processor = uname.processor

########################################################
########################################################
# This will get boot time info
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)

########################################################
########################################################
# this will get CPU information
# number of cores
physical_cores = psutil.cpu_count(logical=False)
total_cores = psutil.cpu_count(logical=True)

# CPU frequencies
cpufreq = psutil.cpu_freq()
max_freq =  round(cpufreq.max, 2)
min_freq =  round(cpufreq.min, 2)
cur_freq =  round(cpufreq.current, 2)

# CPU usage
cpu_usage = psutil.cpu_percent()

########################################################
########################################################
# This section will get all the memory information
# get the memory details
svmem = psutil.virtual_memory()
total_mem = get_size(svmem.total)
available_mem = get_size(svmem.available)
used_mem = get_size(svmem.used)
percent_mem = svmem.percent

# get the swap memory details (if exists)
swap = psutil.swap_memory()
total_swap = get_size(swap.total)
free_swap = get_size(swap.free)
used_swap = get_size(swap.used)
percent_swap = swap.percent


########################################################
########################################################
# This section will get all the disk information

# get all disk partitions
partitions = psutil.disk_partitions()

for partition in partitions:
  device_partition = partition.device
  mountpoint_partition = partition.mountpoint
  file_system_type = partition.fstype
  try:
      partition_usage = psutil.disk_usage(partition.mountpoint)
  except PermissionError:
      # this can be catched due to the disk that
      # isn't ready
      continue
  total_p_size = get_size(partition_usage.total)
  used_p_size = get_size(partition_usage.used)
  free_p_size = get_size(partition_usage.free)
  percent_p_used = partition_usage.percent
  
# get IO statistics since boot
disk_io = psutil.disk_io_counters()
total_disk_read = get_size(disk_io.read_bytes)
total_disk_write = get_size(disk_io.write_bytes)

########################################################
########################################################
# This section will get Network Information

# get IO statistics since boot
net_io = psutil.net_io_counters()
total_bytes_sent = get_size(net_io.bytes_sent)
total_bytes_received = get_size(net_io.bytes_recv)

########################################################
########################################################

# Reading in the edited info.txt file
# THIS FILE MUST BE IN THE SAME DIRECTORY AS
# THE PYTHON SCRIPT
with open("./info.txt", 'r') as inFile:
  # create a list to hold in the info 
  info = []
  # split the lines seperated by \n
  lines = inFile.read().splitlines() 
  # iterate through the info
  for line in lines:
    # if it's a comment skip it
    if (line.startswith("#")):
        continue
    # if it's data add it to my list
    info.append(line)
  
########################################################
########################################################
###### THIS WILL BE USED FOR FINDING DAILY WEATHER REPORTS ######
api_key = info[0]
  
# base_url variable to store url 
base_url = "http://api.openweathermap.org/data/2.5/weather?"
  
# Give city name 
city_name = info[1]
  
# complete_url variable to store 
# complete url address 
complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
  
# get method of requests module 
# return response object 
response = requests.get(complete_url) 
  
# json method of response object  
# convert json format data into 
# python format data 
x = response.json() 
  
# Now x contains list of nested dictionaries 
# Check the value of "cod" key is equal to 
# "404", means city is found otherwise, 
# city is not found 
if x["cod"] != "404": 
  
    # store the value of "main" 
    # key in variable y 
    y = x["main"] 
  
    # store the value corresponding 
    # to the "temp" key of y 
    current_temperature = y["temp"]
    
    # converting temp from Kelvin to Fhrenheit
    current_f_temp = round((current_temperature - 273.15) * 9/5 + 32, 2)
  
    # store the value corresponding 
    # to the "pressure" key of y 
    current_pressure = y["pressure"] 
  
    # store the value corresponding 
    # to the "humidity" key of y 
    current_humidiy = y["humidity"] 
  
    # store the value of "weather" 
    # key in variable z 
    z = x["weather"] 
  
    # store the value corresponding  
    # to the "description" key at  
    # the 0th index of z 
    weather_description = z[0]["description"] 
    
else:
    # incase user inputs a city that's not necessarily 
    # spelt right or exists, you can check OPW
    # for a list of cities you can use
    print(" City Not Found ")
########################################################
########################################################
# if Pi is connected to the internet, send out emails
if (is_connected(REMOTE_SERVER) == True):
    
    port = 465  # For SSL Protocol
    smtp_server = "smtp.gmail.com" # GMAIL will be used as the smtp server
    
    # using the info list to fill in the following
    # variables
    sender_email = info[2]  # Enter your address
    password = info[3]  # sender password
    receiver_email = info[4]  # receiver address
    
    # to print out to the local terminal
    # the current user / and email's
    user = getpass.getuser()
    print("User of Local Machine: %s\n" % user)
    print("Sender Email Adddress: %s\n" % sender_email)
    print("Receiver Email Address: %s\n" % receiver_email)

    # edit crontab to have this script run
    # on a routine (I edited my crontab to have it run every night at 12 AM) 

    # this can prompt the user for a password, if needed
    # password = getpass.getpass("Password for %s email: " % sender_email)
  
    # using MIMEtext to send the email
    message = MIMEMultipart("alternative")
    message["Subject"] = "System Daily Notification"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    This is a Daily Notifcation from Bashier Dahman.
    Internet Connection: ON
    Primary IP Address: """ + get_ip() + """
    
    ===== Weather Details in """ + city_name + """ =====
    Temperature (in Kelvin) = """ + str(current_temperature) + """K
    Temperature (in Fahrenheit) = """ + str(current_f_temp) + """°F
    Atmospheric Pressure (in hPa) = """ + str(current_pressure) + """hPa
    Humidity (in Percentage) = """ + str(current_humidiy) + """%
    Description = """ + str(weather_description) + """

   ===== SYSTEM INFO =====
   System Name: """ + system_name + """
   Node Name: """ + system_node + """
   Release: """ + system_release + """
   Version: """ + system_version + """
   Machine: """ + system_machine + """
   System Processor: """ + system_processor + """
    
    ===== BOOT TIME INFO =====
   Boot Date: """ + str(bt.year) + """/""" + str(bt.month) + """/""" + str(bt.day) + """
   Boot Time: """ + str(bt.hour) + """:""" + str(bt.minute) + """:""" + str(bt.second) + """
   
   ===== CPU INFO =====
   --- Core Info ---
   Physical Cores: """ + str(physical_cores) + """ 
   Total Cores: """ + str(total_cores) + """
   
   --- Frequency Info ---
   Maximum Frequency: """ + str(max_freq) + """ Mhz
   Minimum Frequency: """ + str(min_freq) + """ Mhz
   Current Frequency: """ + str(cur_freq) + """ Mhz
   
   --- CPU Usage ---
   CPU Usage (Percentage): """ + str(cpu_usage) + """%

   
   ===== MEMORY USAGE =====
   Total Memory: """ + str(total_mem) + """
   Available Memory: """ + str(available_mem) + """
   Used Memory: """ + str(used_mem) + """
   Percentage Used: """ + str(percent_mem) + """%
   
    --- Swap Memory (If Exists) ---
    Total Swap Memory: """ + str(total_swap) + """
    Total Free Swap Memory: """ + str(free_swap) + """
    Total Used Swap Memory: """ + str(used_swap) + """
    Percentage of Swap Memory: """ + str(percent_swap) + """
    
    
    ===== DISK INFO =====
    --- Partition Info ---
    Device Partition: """ + str(device_partition) + """
    Mountpoint Partition: """ + str(mountpoint_partition) + """
    File System Type: """ + str(file_system_type) + """

    Total Partition Size: """ + str(total_p_size) + """
    Used Partition Size: """ + str(used_p_size) + """
    Free Partition Size: """ + str(free_p_size) + """
    Percent of Partition Used: """ + str(percent_p_used) + """
    
    --- IO STATISTICS ---
    Total Disk Read """ + str(total_disk_read) + """
    Total Disk Write """ + str(total_disk_write) + """
    
    
    ===== NETWORK INFO =====   
    --- NET IO STATS ---
    Total Bytes Sent: """ + str(total_bytes_sent) + """
    Total Bytes Received: """ + str(total_bytes_received) + """     
    
   
    Sent from """ + str(user) + """
    """ 
    html = """\
    <html>
      <body>
        <p> Hi, <br>
        <i> This is a Daily Notifcation from </i>
           <a href="https://www.linkedin.com/in/bashier-dahman">Bashier Dahman</a>. <br>
            
            <br>
            Internet Connection: <b> <ins>ON</ins> </b> <br>
            Primary IP Address: <b><ins>""" + get_ip() + """</ins></b> <br>
            <br>
            
            <ins> ===== Weather Details in """ + city_name + """ ===== </ins> <br>
            Temperature (in Kelvin) = """ + str(current_temperature) + """ K <br>
            Temperature (in Fahrenheit) = """ + str(current_f_temp) + """°F <br>
            Atmospheric Pressure (in hPa) = """ +str(current_pressure) + """ hPa <br>
            Humidity (in Percentage) = """ + str(current_humidiy) + """% <br>
            Description = """ + str(weather_description) + """ <br>
            
            <p style="color:DarkRed;">===== SYSTEM INFO =====</p>
           System Name: """ + system_name + """ <br>
           Node Name: """ + system_node + """ <br>
           Release: """ + system_release + """ <br>
           Version: """ + system_version + """ <br>
           Machine: """ + system_machine + """ <br>
           System Processor: """ + system_processor + """ <br>
           
           <p style="color:Orchid;">===== BOOT TIME INFO =====</p>
           Boot Date: """ + str(bt.month) + """/""" + str(bt.day) + """/""" + str(bt.year) + """ <br>
           Boot Time: """ + str(bt.hour) + """:""" + str(bt.minute) + """:""" + str(bt.second) + """ <br>
           <br>
           
           <p style = "color:RebeccaPurple;">===== CPU INFO =====</p>
            --- Core Info --- <br>
            Physical Cores: """ + str(physical_cores) + """ <br>
            Total Cores: """ + str(total_cores) + """ <br>
            
            --- Frequency Info --- <br>
            Maximum Frequency: """ + str(max_freq) + """ Mhz<br>
            Minimum Frequency: """ + str(min_freq) + """ Mhz<br>
            Current Frequency: """ + str(cur_freq) + """ Mhz<br>
            
            --- CPU Usage --- <br>
            CPU Usage (Percentage): """ + str(cpu_usage) + """%<br>
            
           <p style = "color:SkyBlue;">===== MEMORY USAGE =====</p>
           Total Memory: """ + str(total_mem) + """ <br>
           Available Memory: """ + str(available_mem) + """ <br>
           Used Memory: """ + str(used_mem) + """ <br>
           Percentage Used: """ + str(percent_mem) + """% <br>
           
            --- Swap Memory (If Exists) --- <br>
            Total Swap Memory: """ + str(total_swap) + """ <br>
            Total Free Swap Memory: """ + str(free_swap) + """ <br>
            Total Used Swap Memory: """ + str(used_swap) + """ <br>
            Percentage of Swap Memory: """ + str(percent_swap) + """ <br>
            
            <p style = "color:DarkGreen;">===== DISK INFO =====</p>
            --- Partition Info --- <br>
            Device Partition: """ + str(device_partition) + """ <br>
            Mountpoint Partition: """ + str(mountpoint_partition) + """ <br>
            File System Type: """ + str(file_system_type) + """ <br>
          
            Total Partition Size: """ + str(total_p_size) + """ <br>
            Used Partition Size: """ + str(used_p_size) + """ <br>
            Free Partition Size: """ + str(free_p_size) + """ <br>
            Percent of Partition Used: """ + str(percent_p_used) + """ <br>
            
            --- IO STATISTICS --- <br>
            Total Disk Read """ + str(total_disk_read) + """ <br>
            Total Disk Write """ + str(total_disk_write) + """ <br>
            
            
            <p style = "color:DarkGoldenRod;">===== NETWORK INFO =====</p>
            --- NET IO STATS ---<br>
            Total Bytes Sent: """ + str(total_bytes_sent) + """ <br>
            Total Bytes Received: """ + str(total_bytes_received) + """ <br>
                   
           <br>
            <b> <i> Sent from """ + user + """ </i> </b> 
      </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # sending the mail
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
else:
    # IF NO INTERNET PRINT TO CONSOLE, THAT THERE'S NO INTERNET
    print("NO INTERNET CONNECTION")
