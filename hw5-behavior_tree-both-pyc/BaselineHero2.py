# https://pyob.oxyry.com/
""#line:17
import sys ,pygame ,math ,numpy ,random ,time ,copy #line:19
from pygame .locals import *#line:20
from constants import *#line:22
from utils import *#line:23
from core import *#line:24
from moba2 import *#line:25
class BaselineHero2 (Hero ):#line:30
	def __init__ (OO00O000OOOO0OO00 ,O0OOO0OOO000O00O0 ,O0O0OOOOO000O000O ,O0000OOOO0000OO0O ,image =AGENT ,speed =SPEED ,viewangle =360 ,hitpoints =HEROHITPOINTS ,firerate =FIRERATE ,bulletclass =BigBullet ,dodgerate =DODGERATE ,areaeffectrate =AREAEFFECTRATE ,areaeffectdamage =AREAEFFECTDAMAGE ):#line:32
		Hero .__init__ (OO00O000OOOO0OO00 ,O0OOO0OOO000O00O0 ,O0O0OOOOO000O000O ,O0000OOOO0000OO0O ,image ,speed ,viewangle ,hitpoints ,firerate ,bulletclass ,dodgerate ,areaeffectrate ,areaeffectdamage )#line:33
		OO00O000OOOO0OO00 .states =[BL2Idle ]#line:34
		OO00O000OOOO0OO00 .states +=[BL2Hunt ,BL2Kill ,BL2Retreat ]#line:37
	def start (O0OOO0O0000OO0O0O ):#line:40
		Hero .start (O0OOO0O0000OO0O0O )#line:41
		O0OOO0O0000OO0O0O .changeState (BL2Idle )#line:42
class BL2Idle (State ):#line:48
	def enter (O0OOO000O0OO00OOO ,OO0O0O0O0O0OO0000 ):#line:50
		State .enter (O0OOO000O0OO00OOO ,OO0O0O0O0O0OO0000 )#line:51
		O0OOO000O0OO00OOO .agent .stopMoving ()#line:53
	def execute (OO00OO0OOOOOO0OO0 ,delta =0 ):#line:55
		State .execute (OO00OO0OOOOOO0OO0 ,delta )#line:56
		OOO0OOOOO0O000OO0 =OO00OO0OOOOOO0OO0 .agent .world .getEnemyNPCs (OO00OO0OOOOOO0OO0 .agent .getTeam ())#line:58
		OO0OO0O0O00OO0O0O =None #line:59
		for O0OOO00O0O0OOOOOO in OOO0OOOOO0O000OO0 :#line:60
			if isinstance (O0OOO00O0O0OOOOOO ,Hero ):#line:61
				OO0OO0O0O00OO0O0O =O0OOO00O0O0OOOOOO #line:62
				break #line:63
		if OO00OO0OOOOOO0OO0 .agent .getHitpoints ()<OO00OO0OOOOOO0OO0 .agent .getMaxHitpoints ()/2.0 :#line:64
			OO00OO0OOOOOO0OO0 .agent .changeState (BL2Retreat )#line:65
		elif OO0OO0O0O00OO0O0O is not None :#line:66
			OO00OO0OOOOOO0OO0 .agent .changeState (BL2Hunt ,OO0OO0O0O00OO0O0O )#line:67
		return None #line:69
class BL2Hunt (State ):#line:74
	def parseArgs (O0O0O00O0O0O00OO0 ,O0000OO0O0O0O00OO ):#line:76
		O0O0O00O0O0O00OO0 .target =O0000OO0O0O0O00OO [0 ]#line:77
	def enter (O00O0O0O0OOO0OO0O ,O0000OO00OO0O0O00 ):#line:79
		State .enter (O00O0O0O0OOO0OO0O ,O0000OO00OO0O0O00 )#line:80
		O00O0O0O0OOO0OO0O .agent .navigateTo (O00O0O0O0OOO0OO0O .target .getLocation ())#line:87
	def execute (O00OO00OO0O000OO0 ,delta =0 ):#line:91
		State .execute (O00OO00OO0O000OO0 ,delta )#line:92
		OOO0O0O0OO00O0OO0 =rayTraceWorld (O00OO00OO0O000OO0 .agent .getLocation (),O00OO00OO0O000OO0 .target .getLocation (),O00OO00OO0O000OO0 .agent .world .getLines ())#line:93
		if O00OO00OO0O000OO0 .agent .getHitpoints ()<O00OO00OO0O000OO0 .agent .getMaxHitpoints ()/2.0 :#line:94
			O00OO00OO0O000OO0 .agent .changeState (BL2Retreat )#line:95
		elif O00OO00OO0O000OO0 .target .isAlive ()==False :#line:96
			O00OO00OO0O000OO0 .agent .changeState (BL2Idle )#line:98
		elif distance (O00OO00OO0O000OO0 .agent .getLocation (),O00OO00OO0O000OO0 .target .getLocation ())<BIGBULLETRANGE -2 :#line:99
			if OOO0O0O0OO00O0OO0 ==None :#line:101
				O00OO00OO0O000OO0 .agent .changeState (BL2Kill ,O00OO00OO0O000OO0 .target )#line:103
		elif O00OO00OO0O000OO0 .agent .getMoveTarget ()==None :#line:105
			O00OO00OO0O000OO0 .agent .navigateTo (O00OO00OO0O000OO0 .target .getLocation ())#line:113
		f42 (O00OO00OO0O000OO0 .agent )#line:114
class BL2Kill (State ):#line:123
	def parseArgs (O00O00O000O0OO00O ,OO00OO00OO00OO000 ):#line:127
		O00O00O000O0OO00O .target =OO00OO00OO00OO000 [0 ]#line:128
	def enter (O00O0OOO00O0OO0O0 ,O000000O00O00O000 ):#line:130
		State .enter (O00O0OOO00O0OO0O0 ,O000000O00O00O000 )#line:131
		O00O0OOO00O0OO0O0 .agent .stopMoving ()#line:133
	def execute (O00OOO00000O00O00 ,delta =0 ):#line:136
		State .execute (O00OOO00000O00O00 ,delta )#line:137
		if O00OOO00000O00O00 .agent .getHitpoints ()<O00OOO00000O00O00 .agent .getMaxHitpoints ()/2.0 :#line:138
			O00OOO00000O00O00 .agent .changeState (BL2Retreat )#line:139
		elif O00OOO00000O00O00 .target .isAlive ()==False :#line:140
			O00OOO00000O00O00 .agent .changeState (BL2Idle )#line:142
		elif O00OOO00000O00O00 .target not in O00OOO00000O00O00 .agent .getVisible ():#line:143
			O00OOO00000O00O00 .agent .changeState (BL2Hunt ,O00OOO00000O00O00 .target )#line:145
		elif distance (O00OOO00000O00O00 .agent .getLocation (),O00OOO00000O00O00 .target .getLocation ())>BIGBULLETRANGE -2 :#line:146
			O00OOO00000O00O00 .agent .changeState (BL2Hunt ,O00OOO00000O00O00 .target )#line:148
		else :#line:149
			O00OOO00000O00O00 .agent .turnToFace (O00OOO00000O00O00 .target .getLocation ())#line:150
			O00OOO00000O00O00 .agent .shoot ()#line:151
class BL2Retreat (State ):#line:157
	def enter (OOOO00OOOOO0O0O0O ,O000OO00000O00OOO ):#line:159
		State .enter (OOOO00OOOOO0O0O0O ,O000OO00000O00OOO )#line:160
		OOOOO0O00000000O0 =OOOO00OOOOO0O0O0O .agent .world .getBaseForTeam (OOOO00OOOOO0O0O0O .agent .getTeam ())#line:161
		if OOOOO0O00000000O0 is not None :#line:162
			OOOO00OOOOO0O0O0O .agent .navigateTo (OOOOO0O00000000O0 .getLocation ())#line:163
	def execute (OOOO00O0OOOO00000 ,delta =0 ):#line:166
		State .execute (OOOO00O0OOOO00000 ,delta )#line:167
		if OOOO00O0OOOO00000 .agent .getMoveTarget ()==None :#line:168
			OOOO00O0OOOO00000 .agent .changeState (BL2Retreat )#line:169
		elif OOOO00O0OOOO00000 .agent .getHitpoints ()==OOOO00O0OOOO00000 .agent .getMaxHitpoints ():#line:170
			OOOO00O0OOOO00000 .agent .changeState (BL2Idle )#line:171
		f42 (OOOO00O0OOOO00000 .agent )#line:172
def f42 (O0OO0O0OOOOOO0000 ):#line:177
	O0O00O0OO000O0OOO =O0OO0O0OOOOOO0000 .getVisibleType (Hero )#line:178
	OO0O000O0O0000O0O =O0OO0O0OOOOOO0000 .getVisibleType (Minion )#line:179
	O0O0OO000O0O00OO0 =None #line:180
	for O0OOOO0O0OOO0OO00 in O0O00O0OO000O0OOO +OO0O000O0O0000O0O :#line:181
		if O0OOOO0O0OOO0OO00 .getTeam ()!=O0OO0O0OOOOOO0000 .getTeam ()and distance (O0OO0O0OOOOOO0000 .getLocation (),O0OOOO0O0OOO0OO00 .getLocation ())<BIGBULLETRANGE -2 :#line:182
			O0O0OO000O0O00OO0 =O0OOOO0O0OOO0OO00 #line:183
			break #line:184
	if O0O0OO000O0O00OO0 is not None :#line:185
		if distance (O0OO0O0OOOOOO0000 .getLocation (),O0O0OO000O0O00OO0 .getLocation ())<=AREAEFFECTRANGE +O0O0OO000O0O00OO0 .getRadius ():#line:186
			O0OO0O0OOOOOO0000 .areaEffect ()#line:187
		else :#line:188
			O0OO0O0OOOOOO0000 .turnToFace (O0O0OO000O0O00OO0 .getLocation ())#line:189
			O0OO0O0OOOOOO0000 .shoot ()#line:190
