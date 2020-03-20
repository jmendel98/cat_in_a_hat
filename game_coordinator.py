import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

import time
import random as random

##TOPICS##
button_listen = "button listen"
button_broadcast = "button broadcast"
location_listen = "location listen"
location_broadcast = "location broadcast"
spells_listen = "spells listen"
spells_broadcast = "spells broadcast"
selection_listen = "selection listen"
selection_broadcast = "selection broadcast"
results_listen = "results listen"
results_broadcast = "results broadcast"
instructions_listen = "instructions listen"
instructions_broadcast = "instructions broadcast"
cast_results_listen = "cast results listen"
cast_results_broadcast = "cast results broadcast"
instructions_broadcast_1 = "instructions broadcast1"


server_ip = "192.168.43.104"

health_a = 10
health_b = 10

def round_go(a_health,b_health):
    
    health_a = a_health
    health_b = b_health


    gesture_grabber = {
        0: 't',
        2: 'c',
        3: 'u',
        1: 'w'
    }

    word_grabber = {
        1: 'r',
        2: 'g',
        3: 'y',
        0: 'b'
    }
    instructions = ""
    
    a = random.randrange(4)
    word = word_grabber.get(a)
    instructions += word
    a = random.randrange(4)
    gest = gesture_grabber.get(a)
    instructions += gest
    a = random.randrange(4)
    word = word_grabber.get(a)
    instructions += word
    a = random.randrange(4)
    gest = gesture_grabber.get(a)
    instructions += gest
    a = random.randrange(4)
    word = word_grabber.get(a)
    instructions += word
    a = random.randrange(4)
    gest = gesture_grabber.get(a)
    instructions += gest
    a = random.randrange(4)
    word = word_grabber.get(a)
    instructions += word
    a = random.randrange(4)
    gest = gesture_grabber.get(a)
    instructions += gest

    msg = subscribe.simple(instructions_listen, hostname=server_ip, msg_count=2) 
    
    time.sleep(2)
    
    publish.single(instructions_broadcast, instructions, hostname=server_ip) #Tell UI how to cast the spell, START OF CASTING PROCESS
    
    
    msg = subscribe.simple(cast_results_listen, hostname=server_ip, msg_count=2) #it for players to report their cast 
    
    first = str(msg[0].payload.strip())
    first = first[2:]
    
    second = str(msg[1].payload.strip())
    second = second[2:]
    
    msg1 = ""
    msg2 = ""

 
    player1 = first[0]

    if(player1== 'a'):
        msg1 = first[1:]
        msg2 = second[1:]
    else:
        msg2 = first[1:]
        msg1 = second[1:]


    att_a = int(msg1[0])
    def_a = int(msg1[1])
    heal_a = int(msg1[2])

    att_b = int(msg2[0])
    def_b = int(msg2[1])
    heal_b = int(msg2[2])

    a_life_change = 0
    b_life_change = 0

    a_attack_att = att_a
    b_defend_def = def_b
    b_defend_heal = heal_b

    while(a_attack_att > 0):
        a_attack_att -= 1
        if(b_defend_heal > 0):
            b_defend_heal -= 1
            print(b_defend_heal)
            print("absorb")
        elif(b_defend_def > 0):
            b_defend_def -= 1
        else:
            b_life_change -= 1

    b_attack_att = att_b
    a_defend_def = def_a
    a_defend_heal = heal_a

    while(b_attack_att > 0):
        b_attack_att -= 1
        if(a_defend_heal > 0):
            a_defend_heal -= 1
            print(a_defend_heal)
            print("absorb")
        elif(a_defend_def > 0):
            a_defend_def -= 1
        else:
            a_life_change -= 1
        
        
    while(a_defend_heal > 0):
        a_defend_heal -= 1
        a_life_change += 1

    while(b_defend_heal > 0):
        b_defend_heal -= 1
        b_life_change += 1
    
    print(a_life_change)
    print(b_life_change)

    health_a += a_life_change
    health_b += b_life_change

    result_msgs = [{'topic':"cast results broadcast", 'payload':msg1},
        ("cast results broadcast", msg2),
        ("cast results broadcast", str(health_a)),
        ("cast results broadcast", str(health_b)),
        ]
    
    result_msgs1 = [{'topic':"cast results broadcast1", 'payload':msg2},
        ("cast results broadcast1", msg1),
        ("cast results broadcast1", str(health_b)),
        ("cast results broadcast1", str(health_a)),
        ]


    time.sleep(2)
    publish.multiple(result_msgs, hostname = server_ip) #Tell UI cast results for both players
    publish.multiple(result_msgs1, hostname = server_ip)
    
    return health_a, health_b

while(True):
    health_a, health_b = round_go(health_a,health_b)


