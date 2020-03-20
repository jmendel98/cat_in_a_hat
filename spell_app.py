from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (StringProperty, ObjectProperty, BooleanProperty, NumericProperty)
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import time

server_ip = "192.168.43.104"

global my_health

##TOPICS##
button_broadcast = "button broadcast"
location_broadcast = "location broadcast"
spells_broadcast = "spells broadcast"
instructions_broadcast = "instructions broadcast"
results_broadcast = "results broadcast"
selection_broadcast = "selection broadcast"
cast_results_broadcast = "cast results broadcast"
instructions_listen = "instructions listen"
cast_synch = "cast synch"
recog_synch = "recog synch"
button_listen = "button listen"
location_listen = "location listen"
spells_listen = "spells listen"
selection_listen = "selection listen"
button_listen = "button listen"
gest_recog_start = "gesture recognition start"




my_health = '0'
opponent_health = '0'
myWidget = ObjectProperty(None)

class StatusBar(Widget):
    
    my_health_label = ObjectProperty(None)
    opp_health_label = ObjectProperty(None)
    round_number_label = ObjectProperty(None)
    location_label = ObjectProperty(None)
    my_CurrentWidget = ObjectProperty(None)
    
    ready_flag = BooleanProperty(True)
    
    round_number = NumericProperty(0)
    
    instruction_grabber = {
        1: "updated_health",
        2: "updated_round",
        3: "updated_location",
        4: "round_begin"
    }
    
    display_grabber = {
        1: "round_begin"
    }
    
    
    def receive_next_instruction(self,instance):
        print("called me!")
        if(self.ready_flag):
            self.ready_flag = False
            msg = subscribe.simple("display", hostname=server_ip, msg_count=1)
            get_instruction = msg.payload.strip()
            instruction = int(get_instruction.decode('ASCII'))
        
        
            instruction_name = self.instruction_grabber.get(instruction)
        
            method_name = 'receive_' + str(instruction_name).strip()
        
            # Get the method from 'self'. Default to a lambda.
            method = getattr(self, method_name, lambda: "Invalid month")
            method(instance)
            self.ready_flag = True
        else:
            print("I tried but was busy")
            
        
        
    def receive_updated_health(self,instance):
        
        msg = subscribe.simple("display", hostname=server_ip, msg_count=2)
        get_health_me = msg[0].payload
        get_health_opp = msg[1].payload
        health_me = get_health_me.decode('ASCII')
        self.my_health_label.text = health_me
        health_opp = get_health_opp.decode('ASCII')
        self.opp_health_label.text = health_opp
        
    def receive_updated_round(self, instance):
        msg = subscribe.simple("display", hostname=server_ip, msg_count=1)
        get_round = msg.payload.strip()
        rnd = get_round.decode('ASCII')
        self.round_number_label.text = rnd
        
    def receive_updated_location(self,instance):
        msg = subscribe.simple("display", hostname=server_ip, msg_count=1)
        get_loc = msg.payload.strip()
        location = get_loc.decode('ASCII')
        self.location_label.text = location
        
    def receive_round_begin(self,instance):
        self.round_number += 1
        my_round_begin = RoundBegin(round_number = self.round_number)
        my_round_begin.update_round_number(self,instance)
        self.my_CurrentWidget = my_round_begin
        print("done making the widget")
        self.add_widget(self.my_CurrentWidget)
        print("goodbye")
        
class SpellGame(Widget):
    
    display_area = ObjectProperty(None)
    sequence_track = NumericProperty(0)
    
    transition_order = {
        1: "nine",
        2: "fourteen",
        3: "nine",
        4: "fifteen",
        5: "nine",
        6: "sixteen",
        7: "nine",
        8: "seventeen",
        9: "nine",
        10: "eighteen",
        11: "nine",
        12: "nineteen",
        13: "nine",
        14: "twenty",
        15: "nine",
        16: "twentyone",
        17: "nine",
        18: "twentytwo",
        19: "nine",
        20: "twentythree",
        21: "nine",
        22: "twentyfour",
        23: "nine",
        24: "twentyfive",
        25: "nine",
        26: "twentysix",
        27: "nine",
        28: "twentyseven",
        29: "nine",
        30: "twentyeight",
        31: "nine",
        32: "twentynine",
        33: "nine",
        34: "one",
        35: "two",
        36: "three",
        37: "four",
        38: "nine",
        39: "five",
        40: "nine",
        41: "six",
        42: "nine",
        43: "seven",
        44: "nine",
        45: "eight",
        46: "nine",
        47: "eight",
        48: "nine",
        49: "eight",
        50: "nine",
        51: "eight",
        52: "nine",
        53: "twelve",
        54: "nine",
        55: "reset",
        56: "nine"
    }
    
    def transition_fourteen(self,instance):
        print("fourteen")
        #first correct up
        time.sleep(1)
        publish.single(gest_recog_start, 'b', hostname=server_ip)
        msg = subscribe.simple(button_listen, hostname=server_ip, msg_count=1) 
        for child in self.display_area.children[:]:
            if child.id == "hello":
                corr = firstCorrect()
                child.layout.add_widget(corr)
                
    def transition_fifteen(self,instance):
        print("fifteen")
        time.sleep(1)
        publish.single(gest_recog_start, 'b', hostname=server_ip)
        msg = subscribe.simple(button_listen, hostname=server_ip, msg_count=1) 
        for child in self.display_area.children[:]:
            if child.id == "hello":
                corr = secondCorrect()
                child.layout.add_widget(corr)
             
    def transition_sixteen(self,instance):
        print("sixteen")
        time.sleep(1)
        publish.single(gest_recog_start, 'b', hostname=server_ip)
        msg = subscribe.simple(button_listen, hostname=server_ip, msg_count=1) 
        for child in self.display_area.children[:]:
            if child.id == "hello":
                corr = thirdCorrect()
                child.layout.add_widget(corr)
                
    def transition_seventeen(self,instance):
        time.sleep(3)
        
        for child in self.display_area.children[:]:
            if child.id == "hello":
                self.display_area.remove_widget(child)
                
        next_training = circleTrain(id='hello')
        self.display_area.add_widget(next_training)
        
    def transition_eighteen(self,instance):
        time.sleep(1)
        publish.single(gest_recog_start, 'l', hostname=server_ip)
        msg = subscribe.simple(button_listen, hostname=server_ip, msg_count=1) 
        for child in self.display_area.children[:]:
            if child.id == "hello":
                corr = firstCorrect()
                child.layout.add_widget(corr)

    def transition_nineteen(self,instance):
        time.sleep(1)
        publish.single(gest_recog_start, 'l', hostname=server_ip)
        msg = subscribe.simple(button_listen, hostname=server_ip, msg_count=1) 
        for child in self.display_area.children[:]:
            if child.id == "hello":
                corr = secondCorrect()
                child.layout.add_widget(corr)
                
    def transition_twenty(self,instance):
        time.sleep(1)
        publish.single(gest_recog_start, 'l', hostname=server_ip)
        msg = subscribe.simple(button_listen, hostname=server_ip, msg_count=1) 
        for child in self.display_area.children[:]:
            if child.id == "hello":
                corr = thirdCorrect()
                child.layout.add_widget(corr)
                
        
    def transition_twentyone(self,instance):
        time.sleep(3)
        
        for child in self.display_area.children[:]:
            if child.id == "hello":
                self.display_area.remove_widget(child)
                
        next_training = twistTrain(id='hello')
        self.display_area.add_widget(next_training)
      
    def transition_twentytwo(self,instance):
        time.sleep(1)
        publish.single(gest_recog_start, 'j', hostname=server_ip)
        msg = subscribe.simple(button_listen, hostname=server_ip, msg_count=1) 
        for child in self.display_area.children[:]:
            if child.id == "hello":
                corr = firstCorrect()
                child.layout.add_widget(corr)

    def transition_twentythree(self,instance):
        time.sleep(1)
        publish.single(gest_recog_start, 'j', hostname=server_ip)
        msg = subscribe.simple(button_listen, hostname=server_ip, msg_count=1) 
        for child in self.display_area.children[:]:
            if child.id == "hello":
                corr = secondCorrect()
                child.layout.add_widget(corr)

    def transition_twentyfour(self,instance):
        time.sleep(1)
        publish.single(gest_recog_start, 'j', hostname=server_ip)
        msg = subscribe.simple(button_listen, hostname=server_ip, msg_count=1) 
        for child in self.display_area.children[:]:
            if child.id == "hello":
                corr = thirdCorrect()
                child.layout.add_widget(corr)

    def transition_twentyfive(self,instance):
        time.sleep(3)
        
        for child in self.display_area.children[:]:
            if child.id == "hello":
                self.display_area.remove_widget(child)
                
        next_training = thrustTrain(id='hello')
        self.display_area.add_widget(next_training)
        
    def transition_twentysix(self,instance):
        time.sleep(1)
        publish.single(gest_recog_start, 'h', hostname=server_ip)
        msg = subscribe.simple(button_listen, hostname=server_ip, msg_count=1) 
        for child in self.display_area.children[:]:
            if child.id == "hello":
                corr = thirdCorrect()
                child.layout.add_widget(corr)

    def transition_twentyseven(self,instance):
        time.sleep(1)
        publish.single(gest_recog_start, 'h', hostname=server_ip)
        msg = subscribe.simple(button_listen, hostname=server_ip, msg_count=1) 
        for child in self.display_area.children[:]:
            if child.id == "hello":
                corr = thirdCorrect()
                child.layout.add_widget(corr)

    def transition_twentyeight(self,instance):
        time.sleep(1)
        publish.single(gest_recog_start, 'h', hostname=server_ip)
        msg = subscribe.simple(button_listen, hostname=server_ip, msg_count=1) 
        for child in self.display_area.children[:]:
            if child.id == "hello":
                corr = thirdCorrect()
                child.layout.add_widget(corr)
                
    def transition_twentynine(self,instance):
        time.sleep(3)
        
        for child in self.display_area.children[:]:
            if child.id == "hello":
                self.display_area.remove_widget(child)
                
        next_training = RoundBegin(id='hello')
        self.display_area.add_widget(next_training)


    def on_sequence_track(self,*args):
        
        transition = self.sequence_track
        
        
        transition_order = self.transition_order.get(transition)
        
            
        method_name = 'transition_' + str(transition_order).strip()
        print(method_name)
        
        method = getattr(self, method_name, lambda: "transition_reset")
        
        if(self.sequence_track != 55):
            method(self)
        else:
            method = getattr(self, "transition_reset")
            method(self)
        
    def next_display(self,*args):
        print(self.sequence_track)
        if(self.sequence_track == 55):
            self.sequence_track = 34
        elif(self.sequence_track < 34):
            self.sequence_track = 34
        elif(self.sequence_track < 56):
            self.sequence_track += 1
        
        
                
    def transition_one(self,instance):
        #start round --> move prompt
        #time.sleep(4)
        next_display = moveNow(id="hello")
        
        for child in self.display_area.children[:]:
            if child.id == "hello":
                self.display_area.remove_widget(child)
        
        self.display_area.add_widget(next_display)
    
    def transition_two(self,instance):
        #move prompt --> taking picture
        msg = subscribe.simple(button_listen, hostname=server_ip, msg_count=1) #user pushed button
            
        next_display = takingPic(id="hello")
        
        for child in self.display_area.children[:]:
            if child.id == "hello":
                self.display_area.remove_widget(child)
            
        
        self.display_area.add_widget(next_display)
        
    def transition_three(self,instance):
        #taking picture --> location updated
        msg = subscribe.simple(location_listen, hostname=server_ip, msg_count=1) #received location information
        
        next_display = locUpdated(id="hello")
        
        loc = str(msg.payload.strip())
        loc = loc[2:]
        

        
        for child in self.display_area.children[:]:
            if child.id == "hello":
                self.display_area.remove_widget(child)
            elif child.id == "status":
                child.location_label.text = str(loc[0])
        self.display_area.add_widget(next_display)
        
    def transition_four(self,instance):
        #location updated --> spell choices
        msg = subscribe.simple(spells_listen, hostname=server_ip, msg_count=3) #received spell choices
        first_spell = str(msg[0].payload.strip())
        first_spell = first_spell[2:]
        second_spell = str(msg[1].payload.strip())
        second_spell = second_spell[2:]
        third_spell = str(msg[2].payload.strip())
        third_spell = third_spell[2:]
        
        first_a = first_spell[0]
        first_d = first_spell[1]
        first_h = first_spell[2]
        first_w = first_spell[3]
        
        second_a = second_spell[0]
        second_d = second_spell[1]
        second_h = second_spell[2]
        second_w = second_spell[3]
        
        third_a = third_spell[0]
        third_d = third_spell[1]
        third_h = third_spell[2]
        third_w = third_spell[3]
        
        for child in self.display_area.children[:]:
            if child.id == "hello":
                self.display_area.remove_widget(child)
        
        one_stat = attackStat(id="a")
        one_stat.stat_label.text=first_a
        spell_1 = spellAttribute(id="a")
        
        
        spell_1.stat_list.add_widget(one_stat)
        
        two_stat = defenseStat(id="d")
        two_stat.stat_label.text=first_d
        spell_1.stat_list.add_widget(two_stat)
        
        three_stat = healStat(id="h")
        three_stat.stat_label.text=first_h
        spell_1.stat_list.add_widget(three_stat)
        
        four_stat = wildcardStat(id="w")
        four_stat.stat_label.text=first_w
        spell_1.stat_list.add_widget(four_stat)
        
        spell_2 = spellAttribute(id="b")
        s2_1 = attackStat(id="a")
        s2_1.stat_label.text=second_a
        s2_2 = defenseStat(id="d")
        s2_2.stat_label.text=second_d
        s2_3 = healStat(id="h")
        s2_3.stat_label.text=second_h
        s2_4 = wildcardStat(id="w")
        s2_4.stat_label.text=second_w
        spell_2.stat_list.add_widget(s2_1)
        spell_2.stat_list.add_widget(s2_2)
        spell_2.stat_list.add_widget(s2_3)
        spell_2.stat_list.add_widget(s2_4)
        
        spell_3 = spellAttribute(id="c")
        s3_1 = attackStat(id="a")
        s3_1.stat_label.text=third_a
        s3_2 = defenseStat(id="d")
        s3_2.stat_label.text=third_d
        s3_3 = healStat(id="h")
        s3_3.stat_label.text=third_h
        s3_4 = wildcardStat(id="w")
        s3_4.stat_label.text=third_w
        spell_3.stat_list.add_widget(s3_1)
        spell_3.stat_list.add_widget(s3_2)
        spell_3.stat_list.add_widget(s3_3)
        spell_3.stat_list.add_widget(s3_4)
        
        s_select = spellSelect(id = "hello")
        
        s_select.spell_grid.add_widget(spell_1)
        s_select.spell_grid.add_widget(spell_2)
        s_select.spell_grid.add_widget(spell_3)
        
        self.display_area.add_widget(s_select)
        
    def transition_five(self,instance):
        #spell choices --> selected spell
        
        msg = subscribe.simple(selection_listen, hostname=server_ip, msg_count=1) #receive selected spell
        
        selected_spell = ObjectProperty(None)
        spell_id = str(msg.payload.strip())
        spell_id = spell_id[2:]
        
        for child in self.display_area.children[:]:
            if child.id == "hello":
                
                for spells in child.spell_grid.children[:]:
                    if spells.id == spell_id[0]:
                        selected_spell = spells
                        child.spell_grid.remove_widget(selected_spell)
                
                self.display_area.remove_widget(child)
                
        next_display = spellChoice(id="hello")
        next_display.spell_area.add_widget(selected_spell)
        
        self.display_area.add_widget(next_display)
        
    def transition_six(self,instance):
        #selected spell --> get ready
        time.sleep(5)
        next_display = getReady(id="hello")
        
        for child in self.display_area.children[:]:
            if child.id == "hello":
                self.display_area.remove_widget(child)
        
        self.display_area.add_widget(next_display)
        
    def transition_seven(self,instance):
        time.sleep(4)
        #get ready --> cast
        gesture_grabber = {
            't': "thrust",
            'c': "circle",
            'u': "up",
            'w': "twist"
        }
        
        word_grabber = {
            'r': "red",
            'g': "green",
            'y': "yellow",
            'b': "blue"
        }
        
        publish.single(instructions_listen, "1", hostname=server_ip) #tell coordinator it's ok to move on
        msg = subscribe.simple(instructions_broadcast, hostname=server_ip, msg_count=1) #receive cast instructions
        
        cast_instruction = str(msg.payload.strip())
        cast_instruction = cast_instruction[2:]
        
        first_combo = combo(id="first")
        first_combo.word_label.text = " ' " + word_grabber.get(cast_instruction[0]) + " ' "
        first_combo.gest_label.text = gesture_grabber.get(cast_instruction[1])
        
        second_combo = combo(id="second")
        second_combo.word_label.text = " ' " + word_grabber.get(cast_instruction[2]) + " ' "
        second_combo.gest_label.text = gesture_grabber.get(cast_instruction[3])

        third_combo = combo(id="third")
        third_combo.word_label.text = " ' " + word_grabber.get(cast_instruction[4]) + " ' "
        third_combo.gest_label.text = gesture_grabber.get(cast_instruction[5])
        
        fourth_combo = combo(id="fourth")
        fourth_combo.word_label.text = " ' " + word_grabber.get(cast_instruction[6]) + " ' "
        fourth_combo.gest_label.text = gesture_grabber.get(cast_instruction[7])
        
        for child in self.display_area.children[:]:
            if child.id == "hello":
                self.display_area.remove_widget(child)
                
        s_cast = spellCast(id="hello")
        
        s_cast.combos.add_widget(first_combo)
        s_cast.combos.add_widget(second_combo)
        s_cast.combos.add_widget(third_combo)
        s_cast.combos.add_widget(fourth_combo)
        
        self.display_area.add_widget(s_cast)
        
    def transition_eight(self,instance):
        
        #runs 4 times, gives result of each spell chunk
        combo_tag = "first"
        print("here")
        
        if(self.sequence_track == 47):
            combo_tag = "second"
        elif(self.sequence_track == 49):
            combo_tag = "third"
        elif(self.sequence_track == 51):
            combo_tag = "fourth"
        
        publish.single(recog_synch, " ", hostname=server_ip)
        
        msg = subscribe.simple(cast_synch, hostname=server_ip, msg_count=1)
        
        msg = subscribe.simple(results_broadcast, hostname=server_ip, msg_count=1) #receive cast combo result
        
        results = str(msg.payload.strip())
        results = results[2:]
        
        word = results[0]
        gesture = results[1]
        
        word_result = ObjectProperty(None)
        
        if(word == 'y'):
            word_result = wordCorrect()
        else:
            word_result = wordIncorrect()
            
        gesture_result = ObjectProperty(None)
        
        if(gesture == 'y'):
            gesture_result = gestCorrect()
        else:
            gesture_result = gestIncorrect()
        
        for child in self.display_area.children[:]:
            if child.id == "hello":
                for combos in child.combos.children[:]:
                    if combos.id == combo_tag:
                        combos.cast_results.add_widget(word_result)
                        combos.cast_results.add_widget(gesture_result)
                        
    def transition_nine(self,instance):
        time.sleep(0.1)
    
    def transition_twelve(self,instance):
        #cast results
        print("Waiting!")
        msg = subscribe.simple(cast_results_broadcast, hostname=server_ip, msg_count=4) #receive cast results
        print("ok")
        my_spell = str(msg[0].payload.strip())
        opp_spell = str(msg[1].payload.strip())
        my_health = msg[2].payload.strip().decode('ASCII')
        opp_health = msg[3].payload.strip().decode('ASCII')
        
        my_spell = my_spell[2:]
        opp_spell = opp_spell[2:]
        
        my_att = my_spell[0]
        my_def = my_spell[1]
        my_heal = my_spell[2]
        
        opp_att = opp_spell[0]
        opp_def = opp_spell[1]
        opp_heal = opp_spell[2]
        
        s_cresult = castResult(id="hello")
        
        my_cast_spell = castSpell()
        my_att_stat = attackStat()
        my_att_stat.stat_label.text = my_att
        my_def_stat = defenseStat()
        my_def_stat.stat_label.text = my_def
        my_heal_stat = healStat()
        my_heal_stat.stat_label.text = my_heal
        my_cast_spell.spell_attributes.add_widget(my_att_stat)
        my_cast_spell.spell_attributes.add_widget(my_def_stat)
        my_cast_spell.spell_attributes.add_widget(my_heal_stat)
        
        opp_cast_spell = castSpell()
        opp_att_stat = attackStat()
        opp_att_stat.stat_label.text = opp_att
        opp_def_stat = defenseStat()
        opp_def_stat.stat_label.text = opp_def
        opp_heal_stat = healStat()
        opp_heal_stat.stat_label.text = opp_heal
        opp_cast_spell.spell_attributes.add_widget(opp_att_stat)
        opp_cast_spell.spell_attributes.add_widget(opp_def_stat)
        opp_cast_spell.spell_attributes.add_widget(opp_heal_stat)
        
        s_cresult.spell_results.add_widget(my_cast_spell)
        s_cresult.spell_results.add_widget(opp_cast_spell)
        
        for child in self.display_area.children[:]:
            if child.id == "hello":
                self.display_area.remove_widget(child)

        for child in self.display_area.children[:]:
                if child.id == "status":
                    child.my_health_label.text = str(my_health)
                    child.opp_health_label.text = str(opp_health) 
                    
        if int(my_health) <= 0 or int(opp_health) <= 0:
            final_display = ObjectProperty(None)
            if int(my_health) <= 0:
                if int(opp_health) <= 0:
                    final_display = youDraw()
                else:
                    final_display = youLose()
            else:
                final_display = youWin()
                
            self.display_area.add_widget(final_display)
            self.sequence_track = 30
        else:
            self.display_area.add_widget(s_cresult)
        
            
                
    def transition_reset(self,instance):
        print("hi")
        time.sleep(3)    
        new_round = RoundBegin(id="hello")
        current_round = 1
            
        for child in self.display_area.children[:]:
            if child.id == "hello":
                self.display_area.remove_widget(child)
            elif child.id == "status":
                current_round = int(child.round_number_label.text)
                current_round += 1
                child.round_number_label.text = str(current_round)
            
        new_round.round_label.text = str(current_round)
            
        self.display_area.add_widget(new_round)
            
          
        
    
        
        
        
        
class moveNow(Widget):
    pass

class takingPic(Widget):
    pass
class youWin(Widget):
    pass
class youLose(Widget):
    pass
class youDraw(Widget):
    pass
class locUpdated(Widget):
    pass

class spellAttribute(Widget):
    
    stat_list = ObjectProperty(None)

class attackStat(Widget):
    
    stat_label = ObjectProperty(None)
    
class defenseStat(Widget):
    
    stat_label = ObjectProperty(None)
    
class healStat(Widget):
    
    stat_label = ObjectProperty(None)
    
class wildcardStat(Widget):
    
    stat_label = ObjectProperty(None)


class RoundBegin(Widget):
    
    round_label = ObjectProperty(0)
    round_number = NumericProperty(0)
    
    def update_round_number(self,instance,round_number):
        self.round_label.text = str(self.round_number)

class spellSelect(Widget):
    
    spell_grid = ObjectProperty(None)
    
class spellChoice(Widget):
    
    spell_area = ObjectProperty(None)
    
class getReady(Widget):
    pass
    
class combo(Widget):
    
    gest_label = ObjectProperty(None)
    word_label = ObjectProperty(None)
    cast_results = ObjectProperty(None)
    
class spellCast(Widget):
    
    combos = ObjectProperty(None)
    
class firstCorrect(Widget):
    pass
class secondCorrect(Widget):
    pass
class thirdCorrect(Widget):
    pass
class upTrain(Widget):
    layout = ObjectProperty(None)
class twistTrain(Widget):
    layout = ObjectProperty(None)
class circleTrain(Widget):
    layout = ObjectProperty(None)
class thrustTrain(Widget):
    layout = ObjectProperty(None)
    

class castResult(Widget):
    
    spell_results = ObjectProperty(None)
    
class wordCorrect(Widget):
    pass

class gestCorrect(Widget):
    pass
    
class wordIncorrect(Widget):
    pass

class gestIncorrect(Widget):
    pass

class castSpell(Widget):
    
    spell_attributes = ObjectProperty(None)

class SpellApp(App):
    def build(self):
        
        myWidget = ObjectProperty(None)
        
        s_bar = StatusBar(id="status")
        s_round = upTrain(id = "hello")
        
        s_lay = BoxLayout()
        
        s_game = SpellGame()
        s_game.display_area.add_widget(s_bar)
        
        s_game.display_area.add_widget(s_round)
        
        
        s_lay.add_widget(s_game)
        
        
        Clock.schedule_interval(s_game.next_display,0.2)
        
        
        #s_game.remove_widget(myWidget)
        
        #s_game.add_widget(s_bar)
        #s_game.add_widget(s_round)
        #s_game.add_widget(s_bar)
        
        #update_status = Clock.create_trigger(s_bar.receive_next_instruction)
        #Clock.schedule_interval(update_status,2)
        #Clock.schedule_once(s_bar.receive_next_instruction,1)
        
        return s_lay


if __name__ == '__main__':
    SpellApp().run()