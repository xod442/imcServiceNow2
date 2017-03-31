#!/usr/bin/env python3
# author: @netwookie

""" Copyright 2015 Hewlett Packard Enterprise Development LP

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

   """

#   IMC create operators 1.0
#  Chris Young a.k.a @netmanchris
#
# Hewlett Packard Company    Revision 1.0

#Caution this is a proof of concept APP only,. You will definitly want to make sure you filter for ONLY the notifications
#that you actually want. Otherwise, this gets really annoying really quickly.

import time
from pyhpeimc.auth import *
from pyhpeimc.plat.alarms import *

auth = IMCAuth("http://", "10.101.0.15", "8080", "admin", "admin")

def create_alarm_list():
    x = get_alarms('admin', auth.creds, auth.url)
    alarm_list = []
    if len(x) is not 0:
        for i in x:
            alarm_list.append(i)
    return alarm_list

def alarm_state(alarm_list):
    alarm_state = 5
    for alarm in alarm_list:
        if int(alarm['alarmLevel']) < alarm_state:
            alarm_state = int(alarm['alarmLevel'])
    return alarm_state


global past_state
print ("It's try")
alarm_list = create_alarm_list()
current_state = alarm_state(alarm_list)
print ("Current state is: "+str(current_state))
print ("Past state is: "+ str(past_state)
