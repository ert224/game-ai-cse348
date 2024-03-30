# https://pyob.oxyry.com/
""#line:17
import sys ,pygame ,math ,numpy ,random ,time ,copy #line:19
from pygame .locals import *#line:20
from constants import *#line:22
from utils import *#line:23
from core import *#line:24
from moba2 import *#line:25
class BaselineHero3 (Hero ):#line:30
	def __init__ (O0OO0O00O0O000OO0 ,OO0OOOOOO0OOOO0OO ,O000OO0OOOOO0OOOO ,OO0O0OO0O00OO0O0O ,image =AGENT ,speed =SPEED ,viewangle =360 ,hitpoints =HEROHITPOINTS ,firerate =FIRERATE ,bulletclass =BigBullet ,dodgerate =DODGERATE ,areaeffectrate =AREAEFFECTRATE ,areaeffectdamage =AREAEFFECTDAMAGE ):#line:32
		Hero .__init__ (O0OO0O00O0O000OO0 ,OO0OOOOOO0OOOO0OO ,O000OO0OOOOO0OOOO ,OO0O0OO0O00OO0O0O ,image ,speed ,viewangle ,hitpoints ,firerate ,bulletclass ,dodgerate ,areaeffectrate ,areaeffectdamage )#line:33
		O0OO0O00O0O000OO0 .states =[BL3Idle ]#line:34
		O0OO0O00O0O000OO0 .states +=[BL3Hunt ,BL3Kill ,BL3Retreat ,BL3Buff ]#line:37
	def start (O00OO00O00000O00O ):#line:40
		Hero .start (O00OO00O00000O00O )#line:41
		O00OO00O00000O00O .changeState (BL3Idle )#line:42
class BL3Idle (State ):#line:48
	def enter (O0000O0OOO00O0OO0 ,O0OO00OO00OO0O000 ):#line:50
		State .enter (O0000O0OOO00O0OO0 ,O0OO00OO00OO0O000 )#line:51
		O0000O0OOO00O0OO0 .agent .stopMoving ()#line:53
	def execute (O000OO0OOOOOOO0O0 ,delta =0 ):#line:55
		State .execute (O000OO0OOOOOOO0O0 ,delta )#line:56
		O0OO0O0OOO000O00O =O000OO0OOOOOOO0O0 .agent .world .getEnemyNPCs (O000OO0OOOOOOO0O0 .agent .getTeam ())#line:58
		O0OOOO0000OOO00O0 =None #line:59
		for OO00OO0OO0OOOOOO0 in O0OO0O0OOO000O00O :#line:60
			if isinstance (OO00OO0OO0OOOOOO0 ,Hero ):#line:61
				O0OOOO0000OOO00O0 =OO00OO0OO0OOOOOO0 #line:62
				break #line:63
		if O000OO0OOOOOOO0O0 .agent .getHitpoints ()<O000OO0OOOOOOO0O0 .agent .getMaxHitpoints ()/2.0 :#line:64
			O000OO0OOOOOOO0O0 .agent .changeState (BL3Retreat )#line:65
		elif O0OOOO0000OOO00O0 is not None and O000OO0OOOOOOO0O0 .agent .level >O0OOOO0000OOO00O0 .level +2 :#line:66
			O000OO0OOOOOOO0O0 .agent .changeState (BL3Hunt ,O0OOOO0000OOO00O0 )#line:67
		else :#line:68
			O000OO0OOOOOOO0O0 .agent .changeState (BL3Buff )#line:69
		return None #line:71
class BL3Hunt (State ):#line:76
	def parseArgs (O0OO0OO0OO00OOOO0 ,OO0OOOO0OO00OO0O0 ):#line:78
		O0OO0OO0OO00OOOO0 .target =OO0OOOO0OO00OO0O0 [0 ]#line:79
	def enter (OOOO000000O000OOO ,OOOOO000O00O000O0 ):#line:81
		State .enter (OOOO000000O000OOO ,OOOOO000O00O000O0 )#line:82
		'''
		if self.target.isMoving():
			self.agent.navigateTo(self.target.getMoveTarget())
		else:
			self.agent.navigateTo(self.target.getLocation())
		'''#line:88
		OOOO000000O000OOO .agent .navigateTo (OOOO000000O000OOO .target .getLocation ())#line:89
	def execute (O000O0O000OOOOOO0 ,delta =0 ):#line:93
		State .execute (O000O0O000OOOOOO0 ,delta )#line:94
		O0O000O00O0OO0O0O =rayTraceWorld (O000O0O000OOOOOO0 .agent .getLocation (),O000O0O000OOOOOO0 .target .getLocation (),O000O0O000OOOOOO0 .agent .world .getLines ())#line:95
		if O000O0O000OOOOOO0 .agent .getHitpoints ()<O000O0O000OOOOOO0 .agent .getMaxHitpoints ()/2.0 :#line:96
			O000O0O000OOOOOO0 .agent .changeState (BL3Retreat )#line:97
		elif O000O0O000OOOOOO0 .target .isAlive ()==False :#line:98
			O000O0O000OOOOOO0 .agent .changeState (BL3Idle )#line:100
		elif distance (O000O0O000OOOOOO0 .agent .getLocation (),O000O0O000OOOOOO0 .target .getLocation ())<BIGBULLETRANGE -2 :#line:101
			if O0O000O00O0OO0O0O ==None :#line:103
				O000O0O000OOOOOO0 .agent .changeState (BL3Kill ,O000O0O000OOOOOO0 .target )#line:105
		elif O000O0O000OOOOOO0 .agent .getMoveTarget ()==None :#line:107
			O000O0O000OOOOOO0 .agent .navigateTo (O000O0O000OOOOOO0 .target .getLocation ())#line:115
		BL3shootAtMinions (O000O0O000OOOOOO0 .agent )#line:116
class BL3Kill (State ):#line:125
	def parseArgs (OO0O00O00OOOO0OO0 ,O00O0OO0O0O00OO00 ):#line:129
		OO0O00O00OOOO0OO0 .target =O00O0OO0O0O00OO00 [0 ]#line:130
	def enter (OOO000O000OO00O00 ,O00000OOO00000OOO ):#line:132
		State .enter (OOO000O000OO00O00 ,O00000OOO00000OOO )#line:133
		OOO000O000OO00O00 .agent .stopMoving ()#line:135
	def execute (O00000OO0OOOO0000 ,delta =0 ):#line:138
		State .execute (O00000OO0OOOO0000 ,delta )#line:139
		if O00000OO0OOOO0000 .agent .getHitpoints ()<O00000OO0OOOO0000 .agent .getMaxHitpoints ()/2.0 :#line:140
			O00000OO0OOOO0000 .agent .changeState (BL3Retreat )#line:141
		elif O00000OO0OOOO0000 .target .isAlive ()==False :#line:142
			O00000OO0OOOO0000 .agent .changeState (BL3Idle )#line:144
		elif O00000OO0OOOO0000 .target not in O00000OO0OOOO0000 .agent .getVisible ():#line:145
			O00000OO0OOOO0000 .agent .changeState (BL3Hunt ,O00000OO0OOOO0000 .target )#line:147
		elif distance (O00000OO0OOOO0000 .agent .getLocation (),O00000OO0OOOO0000 .target .getLocation ())>BIGBULLETRANGE -2 :#line:148
			O00000OO0OOOO0000 .agent .changeState (BL3Hunt ,O00000OO0OOOO0000 .target )#line:150
		else :#line:151
			O00000OO0OOOO0000 .agent .turnToFace (O00000OO0OOOO0000 .target .getLocation ())#line:152
			O00000OO0OOOO0000 .agent .shoot ()#line:153
class BL3Retreat (State ):#line:159
	def enter (OOOOOO0O00O0O00OO ,OO0O00OO0O0O00OOO ):#line:161
		State .enter (OOOOOO0O00O0O00OO ,OO0O00OO0O0O00OOO )#line:162
		O00OOOO00O00O00O0 =OOOOOO0O00O0O00OO .agent .world .getBaseForTeam (OOOOOO0O00O0O00OO .agent .getTeam ())#line:163
		if O00OOOO00O00O00O0 is not None :#line:164
			OOOOOO0O00O0O00OO .agent .navigateTo (O00OOOO00O00O00O0 .getLocation ())#line:165
	def execute (O0O0OO00O0OO000OO ,delta =0 ):#line:168
		State .execute (O0O0OO00O0OO000OO ,delta )#line:169
		if O0O0OO00O0OO000OO .agent .getMoveTarget ()==None :#line:170
			O0O0OO00O0OO000OO .agent .changeState (BL3Retreat )#line:171
		elif O0O0OO00O0OO000OO .agent .getHitpoints ()==O0O0OO00O0OO000OO .agent .getMaxHitpoints ():#line:172
			O0O0OO00O0OO000OO .agent .changeState (BL3Idle )#line:173
		BL3shootAtMinions (O0O0OO00O0OO000OO .agent )#line:174
class BL3Buff (State ):#line:179
	def enter (OO0O0OOO00O000000 ,OOO0000O00OO0OO0O ):#line:181
		State .enter (OO0O0OOO00O000000 ,OOO0000O00OO0OO0O )#line:182
		OO0O0OOO00O000000 .target =None #line:183
		OO0O0OOO00O000000 .timer =0 #line:184
		O000O00O000OOOO00 =OO0O0OOO00O000000 .agent .world .getEnemyNPCs (OO0O0OOO00O000000 .agent .getTeam ())#line:185
		if len (O000O00O000OOOO00 )>0 :#line:186
			for O0O0OO0O0OO0O0OOO in O000O00O000OOOO00 :#line:187
				if isinstance (O0O0OO0O0OO0O0OOO ,Minion ):#line:188
					OO0O0OOO00O000000 .target =O0O0OO0O0OO0O0OOO #line:189
					break #line:190
		if OO0O0OOO00O000000 .target is not None :#line:191
			OO0O0OOO00O000000 .agent .navigateTo (OO0O0OOO00O000000 .target .getLocation ())#line:192
	def execute (O00OO00000000OOOO ,delta =0 ):#line:194
		State .execute (O00OO00000000OOOO ,delta )#line:195
		if O00OO00000000OOOO .target ==None :#line:196
			O00OO00000000OOOO .agent .changeState (BL3Buff )#line:197
		else :#line:198
			O00OO00000000OOOO .timer =O00OO00000000OOOO .timer +1 #line:199
			if O00OO00000000OOOO .target .isAlive ==False :#line:200
				O00OO00000000OOOO .agent .changeState (BL3Idle )#line:201
			elif O00OO00000000OOOO .agent .getHitpoints ()<O00OO00000000OOOO .agent .getMaxHitpoints ()/2.0 :#line:202
				O00OO00000000OOOO .agent .changeState (BL3Retreat )#line:203
			elif distance (O00OO00000000OOOO .agent .getLocation (),O00OO00000000OOOO .target .getLocation ())<BIGBULLETRANGE -2 :#line:204
				O000000000OO0O0O0 =rayTraceWorld (O00OO00000000OOOO .agent .getLocation (),O00OO00000000OOOO .target .getLocation (),O00OO00000000OOOO .agent .world .getLines ())#line:206
				if O000000000OO0O0O0 ==None :#line:207
					O00OO00000000OOOO .agent .changeState (BL3Kill ,O00OO00000000OOOO .target )#line:209
			elif O00OO00000000OOOO .timer >50 or O00OO00000000OOOO .agent .getMoveTarget ()==None :#line:211
				O00OO00000000OOOO .agent .navigateTo (O00OO00000000OOOO .target .getLocation ())#line:213
				O00OO00000000OOOO .timer =0 #line:214
		BL3shootAtMinions (O00OO00000000OOOO .agent )#line:215
def BL3shootAtMinions (O0O0O00OOO0OO000O ):#line:220
	O00OO000OOOOOOOO0 =O0O0O00OOO0OO000O .getVisibleType (Hero )#line:221
	O0O0000OO00OO0OO0 =O0O0O00OOO0OO000O .getVisibleType (Minion )#line:222
	O000O00OOOOOO0000 =None #line:223
	for O0OOOO0O0OO00O000 in O00OO000OOOOOOOO0 +O0O0000OO00OO0OO0 :#line:224
		if O0OOOO0O0OO00O000 .getTeam ()!=O0O0O00OOO0OO000O .getTeam ()and distance (O0O0O00OOO0OO000O .getLocation (),O0OOOO0O0OO00O000 .getLocation ())<BIGBULLETRANGE -2 :#line:225
			O000O00OOOOOO0000 =O0OOOO0O0OO00O000 #line:226
			break #line:227
	if O000O00OOOOOO0000 is not None :#line:228
		if distance (O0O0O00OOO0OO000O .getLocation (),O000O00OOOOOO0000 .getLocation ())<=AREAEFFECTRANGE +O000O00OOOOOO0000 .getRadius ():#line:229
			O0O0O00OOO0OO000O .areaEffect ()#line:230
		else :#line:231
			O0O0O00OOO0OO000O .turnToFace (O000O00OOOOOO0000 .getLocation ())#line:232
			O0O0O00OOO0OO000O .shoot ()#line:233
