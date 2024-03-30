# https://pyob.oxyry.com/
""#line:17
import sys ,pygame ,math ,numpy ,random ,time ,copy #line:19
from pygame .locals import *#line:20
from constants import *#line:22
from utils import *#line:23
from core import *#line:24
from moba2 import *#line:25
class WanderingMinion (Minion ):#line:30
	def __init__ (O0O0OOOO00OOOO0O0 ,OOOOOOOO000000000 ,OO00O0O00OOOOOO00 ,O0O00OOOO00OO00O0 ,image =NPC ,speed =SPEED ,viewangle =360 ,hitpoints =HITPOINTS ,firerate =FIRERATE ,bulletclass =SmallBullet ):#line:32
		Minion .__init__ (O0O0OOOO00OOOO0O0 ,OOOOOOOO000000000 ,OO00O0O00OOOOOO00 ,O0O00OOOO00OO00O0 ,image ,speed ,viewangle ,hitpoints ,firerate ,bulletclass )#line:33
		O0O0OOOO00OOOO0O0 .states =[MWander ,MKillHero ]#line:34
	def start (O0O00O0O000OOO0O0 ):#line:36
		StateAgent .start (O0O00O0O000OOO0O0 )#line:37
		O0O00O0O000OOO0O0 .world .computeFreeLocations (O0O00O0O000OOO0O0 )#line:38
		O0O00O0O000OOO0O0 .changeState (MWander )#line:39
class MWander (State ):#line:45
	def enter (O0OO00O00000O0O0O ,OO00OOOOO000OOOOO ):#line:47
		State .enter (O0OO00O00000O0O0O ,OO00OOOOO000OOOOO )#line:48
		O00OOOO0O00OOOO00 =O0OO00O00000O0O0O .agent .getPossibleDestinations ()#line:50
		if len (O00OOOO0O00OOOO00 )>0 :#line:51
			O00OO0000OOO0OO0O =random .randint (0 ,len (O00OOOO0O00OOOO00 )-1 )#line:52
			O0OOO00O00000OO0O =O00OOOO0O00OOOO00 [O00OO0000OOO0OO0O ]#line:53
			O0OO00O00000O0O0O .agent .navigateTo (O0OOO00O00000OO0O )#line:54
		return None #line:55
	def execute (O00O000OOO00OO0OO ,delta =0 ):#line:57
		State .execute (O00O000OOO00OO0OO ,delta )#line:58
		if O00O000OOO00OO0OO .agent .moveTarget ==None :#line:59
			O00O000OOO00OO0OO .agent .changeState (MWander )#line:61
		OO0O0000OOO0O00OO =O00O000OOO00OO0OO .agent .getVisibleType (Hero )#line:63
		O0OO0O0O0000OOO00 =[]#line:64
		for O00O0O0OO00OO0000 in OO0O0000OOO0O00OO :#line:65
			if O00O0O0OO00OO0000 .getTeam ()!=O00O000OOO00OO0OO .agent .getTeam ():#line:66
				O0OO0O0O0000OOO00 .append (O00O0O0OO00OO0000 )#line:67
		if len (O0OO0O0O0000OOO00 )>0 :#line:68
			for O00O0O0OO00OO0000 in O0OO0O0O0000OOO00 :#line:69
				if distance (O00O000OOO00OO0OO .agent .getLocation (),O00O0O0OO00OO0000 .getLocation ())<SMALLBULLETRANGE :#line:70
					O00O000OOO00OO0OO .agent .changeState (MKillHero ,O00O0O0OO00OO0000 )#line:71
					break #line:72
		return None #line:73
class MKillHero (State ):#line:79
	def parseArgs (O000OO0OOOO0000O0 ,O0000OO000O0000OO ):#line:83
		O000OO0OOOO0000O0 .target =O0000OO000O0000OO [0 ]#line:84
	def enter (OOOO0O0OO0OO0OO00 ,O000O0000O0O0O000 ):#line:86
		State .enter (OOOO0O0OO0OO0OO00 ,O000O0000O0O0O000 )#line:87
		OOOO0O0OO0OO0OO00 .agent .stopMoving ()#line:89
	def execute (O000O0OOO0O0OO0OO ,delta =0 ):#line:91
		if O000O0OOO0O0OO0OO .target not in O000O0OOO0O0OO0OO .agent .getVisible ():#line:92
			O000O0OOO0O0OO0OO .agent .changeState (MWander )#line:94
		elif distance (O000O0OOO0O0OO0OO .agent .getLocation (),O000O0OOO0O0OO0OO .target .getLocation ())>SMALLBULLETRANGE :#line:95
			O000O0OOO0O0OO0OO .agent .changeState (MWander )#line:97
		else :#line:98
			O000O0OOO0O0OO0OO .agent .turnToFace (O000O0OOO0O0OO0OO .target .getLocation ())#line:99
			O000O0OOO0O0OO0OO .agent .shoot ()#line:100
