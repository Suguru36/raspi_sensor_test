#! /usr/bin/env python3
# coding: UTF-8
#ラベルの表示確認
#2019.01.16 by SGR


from transitions import Machine

class StateMachine(object):
    #状態の定義
    states = ['idle', 'meas_dist', 'ready','proximity', 'heat','keep','finish','emo']

    #初期化（ステートマシンの定義：とりうる状態の定義、初期状態の定義、各種遷移と紐付くアクションの定義）
    def __init__(self, name):
        self.name = name
        self.machine =      Machine(model=self, states=StateMachine.states, initial='idle', auto_transitions=False)

        self.machine.add_transition(trigger='func_sw'    , source='idle'     , dest='meas_dist' ,before= 'action_idle2meas')
        self.machine.add_transition(trigger='in_range'   , source='meas_dist', dest='ready'     ,before= 'action_ready2in_range')
        self.machine.add_transition(trigger='out_range'  , source='ready'    , dest='meas_dist' ,before= 'action_ready2meas_dist')
        self.machine.add_transition(trigger='too_short'  , source='ready'    , dest='proximity' ,before= 'action_ready2proximity')
        self.machine.add_transition(trigger='in_range'   , source='proximity', dest='ready'     ,before= 'action_proximity2ready')
        self.machine.add_transition(trigger='func_sw'    , source='ready'    , dest='heat'      ,before= 'action_ready2heat')
        self.machine.add_transition(trigger='temp_reach' , source='heat'     , dest='keep'      ,before= 'action_heat2keep')
        self.machine.add_transition(trigger='timer'      , source='keep'     , dest='finish'    ,before= 'action_keep2finish')
        self.machine.add_transition(trigger='func_sw'    , source='finish'   , dest='idle'      ,before= 'action_finish2idle')

        self.machine.add_transition(trigger='emo_sw'     , source='idle'     , dest='emo'       ,before= 'action_emo_det')
        self.machine.add_transition(trigger='emo_sw'     , source='meas_dist', dest='emo'       ,before= 'action_emo_det')
        self.machine.add_transition(trigger='emo_sw'     , source='ready'    , dest='emo'       ,before= 'action_emo_det')
        self.machine.add_transition(trigger='emo_sw'     , source='proximity', dest='emo'       ,before= 'action_emo_det')
        self.machine.add_transition(trigger='emo_sw'     , source='heat'     , dest='emo'       ,before= 'action_emo_det')
        self.machine.add_transition(trigger='emo_sw'     , source='keep'     , dest='emo'       ,before= 'action_emo_det')
        self.machine.add_transition(trigger='emo_sw'     , source='finish'   , dest='emo'       ,before= 'action_emo_det')

        self.machine.add_transition(trigger='emo_releace', source='emo'      , dest='idle'      ,before= 'action_emo_releace')

        self.machine.add_transition(trigger='long_press' , source='idle'     , dest='idle'      ,before= 'action_long_press')
        self.machine.add_transition(trigger='long_press' , source='meas_dist', dest='idle'      ,before= 'action_long_press')
        self.machine.add_transition(trigger='long_press' , source='ready'    , dest='idle'      ,before= 'action_long_press')
        self.machine.add_transition(trigger='long_press' , source='proximity', dest='idle'      ,before= 'action_long_press')
        self.machine.add_transition(trigger='long_press' , source='heat'     , dest='idle'      ,before= 'action_long_press')
        self.machine.add_transition(trigger='long_press' , source='keep'     , dest='idle'      ,before= 'action_long_press')
        self.machine.add_transition(trigger='long_press' , source='finish'   , dest='idle'      ,before= 'action_long_press')


#---------------------------------------------
#--------- 以下、遷移時のアクション ----------
#---------------------------------------------
    def action_idle2meas(self):
        print ("*** from idle to meas_distance ***")
        self.display_state()
#----------------------
    def action_ready2in_range(self):
        print ("*** from meas_distance to ready ***")
        self.display_state()
#----------------------
    def action_ready2meas_dist(self):
        print ("*** from ready to meas_distance ***")
        self.display_state()
#----------------------
    def action_ready2proximity(self):
        print("*** from ready to proximity ***")
        self.display_state()
#----------------------
    def action_proximity2ready(self):
        print("*** from proximity to ready ***")
        self.display_state()
#----------------------
    def action_ready2heat(self):
        print("*** from ready to heat ***")
        self.display_state()
#----------------------
    def action_heat2keep(self):
        print("*** from heat to keep ***")
        self.display_state()
#----------------------
    def action_keep2finish(self):
        print("*** from keep to finish ***")
        self.display_state()
#----------------------
    def action_finish2idle(self):
        print("*** from finish to idle ***")
        self.display_state()
#----------------------
    def action_emo_det(self):
        print("*** EMO DETECTION***")
        self.display_state()
#----------------------
    def action_emo_releace(self):
        print("*** EMO RELEACE***")
        self.display_state()
#----------------------
    def action_long_press(self):
        print("*** LONG PRESS DETECT ***")
        self.display_state()


#------------------------
#-- ステートマシン取得 --
#------------------------
    def display_state(self):
        pass
###############################
if __name__ == '__main__':
    lump = StateMachine("mol")
    print(lump.state)
    lump.func_sw()
    print(lump.state)
