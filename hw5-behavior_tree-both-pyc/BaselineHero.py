# https://pyob.oxyry.com/
""#line:17
import sys ,pygame ,math ,numpy ,random ,time ,copy #line:19
from pygame .locals import *#line:20
from constants import *#line:22
from utils import *#line:23
from core import *#line:24
from moba2 import *#line:25
class BaselineHero (Hero ):#line:30
	def __init__ (O00O000O000O00OO0 ,O0O0000OO00OO0O00 ,O00000000O0OO0000 ,O000OOO0OOOO0O00O ,image =AGENT ,speed =SPEED ,viewangle =360 ,hitpoints =HEROHITPOINTS ,firerate =FIRERATE ,bulletclass =BigBullet ,dodgerate =DODGERATE ,areaeffectrate =AREAEFFECTRATE ,areaeffectdamage =AREAEFFECTDAMAGE ):#line:32
		Hero .__init__ (O00O000O000O00OO0 ,O0O0000OO00OO0O00 ,O00000000O0OO0000 ,O000OOO0OOOO0O00O ,image ,speed ,viewangle ,hitpoints ,firerate ,bulletclass ,dodgerate ,areaeffectrate ,areaeffectdamage )#line:33
		O00O000O000O00OO0 .states =[BLIdle ]#line:34
		O00O000O000O00OO0 .states +=[BLHunt ,BLKill ]#line:37
	def start (O0OO0OOOOOO0O0O0O ):#line:40
		Hero .start (O0OO0OOOOOO0O0O0O )#line:41
		O0OO0OOOOOO0O0O0O .changeState (BLIdle )#line:42
class BLIdle (State ):#line:48
	def enter (OO000O0OOOO0O0000 ,O0OO0O00OO0OOO0O0 ):#line:50
		State .enter (OO000O0OOOO0O0000 ,O0OO0O00OO0OOO0O0 )#line:51
		OO000O0OOOO0O0000 .agent .stopMoving ()#line:53
	def execute (O0OOO0O0OO0OO0OOO ,delta =0 ):#line:55
		State .execute (O0OOO0O0OO0OO0OOO ,delta )#line:56
		OO0OOOOOOOO0OOOOO =O0OOO0O0OO0OO0OOO .agent .world .getEnemyNPCs (O0OOO0O0OO0OO0OOO .agent .getTeam ())#line:58
		O000OO0O000O0O00O =None #line:59
		for O00O0000O0O00OO0O in OO0OOOOOOOO0OOOOO :#line:60
			if isinstance (O00O0000O0O00OO0O ,Hero ):#line:61
				O000OO0O000O0O00O =O00O0000O0O00OO0O #line:62
				break #line:63
		if O000OO0O000O0O00O is not None :#line:64
			O0OOO0O0OO0OO0OOO .agent .changeState (BLHunt ,O000OO0O000O0O00O )#line:65
		return None #line:67
class BLHunt (State ):#line:72
	def parseArgs (OOO0OOOO0OOO0O00O ,OO0O0O0OOO0OO0000 ):#line:74
		OOO0OOOO0OOO0O00O .target =OO0O0O0OOO0OO0000 [0 ]#line:75
	def enter (O0OO000O00OOO0O0O ,O000OO000OO00O0O0 ):#line:77
		State .enter (O0OO000O00OOO0O0O ,O000OO000OO00O0O0 )#line:78
		'''
		if self.target.isMoving():
			self.agent.navigateTo(self.target.getMoveTarget())
		else:
			self.agent.navigateTo(self.target.getLocation())
		'''#line:84
		O0OO000O00OOO0O0O .agent .navigateTo (O0OO000O00OOO0O0O .target .getLocation ())#line:85
	def execute (OO00O00OO0OOO0OOO ,delta =0 ):#line:89
		State .execute (OO00O00OO0OOO0OOO ,delta )#line:90
		O00OOOO0OOOO0OOO0 =rayTraceWorld (OO00O00OO0OOO0OOO .agent .getLocation (),OO00O00OO0OOO0OOO .target .getLocation (),OO00O00OO0OOO0OOO .agent .world .getLines ())#line:91
		if OO00O00OO0OOO0OOO .target .isAlive ()==False :#line:92
			OO00O00OO0OOO0OOO .agent .changeState (BLIdle )#line:94
		elif distance (OO00O00OO0OOO0OOO .agent .getLocation (),OO00O00OO0OOO0OOO .target .getLocation ())<BIGBULLETRANGE -2 :#line:95
			if O00OOOO0OOOO0OOO0 ==None :#line:97
				OO00O00OO0OOO0OOO .agent .changeState (BLKill ,OO00O00OO0OOO0OOO .target )#line:99
		elif OO00O00OO0OOO0OOO .agent .getMoveTarget ()==None :#line:101
			OO00O00OO0OOO0OOO .agent .navigateTo (OO00O00OO0OOO0OOO .target .getLocation ())#line:109
		blShootAtMinions (OO00O00OO0OOO0OOO .agent )#line:110
class BLKill (State ):#line:119
	def parseArgs (O00OO0000OOO0OOOO ,OOO000OO000O0000O ):#line:123
		O00OO0000OOO0OOOO .target =OOO000OO000O0000O [0 ]#line:124
	def enter (OO0OO0OO0O0O00OO0 ,O000000OO0O00O00O ):#line:126
		State .enter (OO0OO0OO0O0O00OO0 ,O000000OO0O00O00O )#line:127
		OO0OO0OO0O0O00OO0 .agent .stopMoving ()#line:129
	def execute (O00O00OO000OOOOOO ,delta =0 ):#line:132
		State .execute (O00O00OO000OOOOOO ,delta )#line:133
		if O00O00OO000OOOOOO .target .isAlive ()==False :#line:134
			O00O00OO000OOOOOO .agent .changeState (BLIdle )#line:136
		elif O00O00OO000OOOOOO .target not in O00O00OO000OOOOOO .agent .getVisible ():#line:137
			O00O00OO000OOOOOO .agent .changeState (BLHunt ,O00O00OO000OOOOOO .target )#line:139
		elif distance (O00O00OO000OOOOOO .agent .getLocation (),O00O00OO000OOOOOO .target .getLocation ())>BIGBULLETRANGE -2 :#line:140
			O00O00OO000OOOOOO .agent .changeState (BLHunt ,O00O00OO000OOOOOO .target )#line:142
		else :#line:143
			O00O00OO000OOOOOO .agent .turnToFace (O00O00OO000OOOOOO .target .getLocation ())#line:144
			O00O00OO000OOOOOO .agent .shoot ()#line:145
def blShootAtMinions (O0OO00OOOO0O0O000 ):#line:151
	O0O0O0O0O0O00O00O =O0OO00OOOO0O0O000 .getVisibleType (Hero )#line:152
	OOOO0OOOOOOO0OO00 =O0OO00OOOO0O0O000 .getVisibleType (Minion )#line:153
	OO00O0000000OOOO0 =None #line:154
	for OOOOOO00O0OOO00O0 in O0O0O0O0O0O00O00O +OOOO0OOOOOOO0OO00 :#line:155
		if OOOOOO00O0OOO00O0 .getTeam ()!=O0OO00OOOO0O0O000 .getTeam ()and distance (O0OO00OOOO0O0O000 .getLocation (),OOOOOO00O0OOO00O0 .getLocation ())<BIGBULLETRANGE -2 :#line:156
			OO00O0000000OOOO0 =OOOOOO00O0OOO00O0 #line:157
			break #line:158
	if OO00O0000000OOOO0 is not None :#line:159
		if distance (O0OO00OOOO0O0O000 .getLocation (),OO00O0000000OOOO0 .getLocation ())<=AREAEFFECTRANGE +OO00O0000000OOOO0 .getRadius ():#line:160
			O0OO00OOOO0O0O000 .areaEffect ()#line:161
		else :#line:162
			O0OO00OOOO0O0O000 .turnToFace (OO00O0000000OOOO0 .getLocation ())#line:163
			O0OO00OOOO0O0O000 .shoot ()#line:164
