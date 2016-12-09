#Authors: Anthony Calabrese, Nate Cefarelli
#File: finalProjectACNC.py
import viz
import math
import vizshape
import vizfx
import sys

class horror(viz.EventClass):

	def __init__(self):
		# must call constructor of EventClass first!!
		viz.EventClass.__init__(self)
		
		#set callbacks
		self.callback(viz.KEYDOWN_EVENT,self.onKeyDown)
		self.callback(viz.MOUSE_MOVE_EVENT,self.cameraMove)
		self.callback(viz.TIMER_EVENT, self.onTimer)
		self.callback(viz.KEYUP_EVENT, self.onKeyUp)
		self.callback(viz.COLLIDE_BEGIN_EVENT,self.onCollideBegin)
		self.starttimer(1, .25, viz.FOREVER)
		self.starttimer(2, 1, viz.FOREVER)
		
		#start background music
		self.background = viz.addAudio('audio/bellLoop.wav')
		self.background.loop(viz.ON)
		self.background.play()
		
		#set up tick sound
		self.tick = viz.addAudio('audio/tickingSound.wav')
		self.tick.volume(.8)
		self.panic = viz.addAudio('audio/HurryMechanic.wav')
		
		#set up key music
		self.tensionRed = viz.addAudio('audio/Tension Loop1.wav')
		self.tensionRed.loop(viz.ON)
		self.tensionBlue = viz.addAudio('audio/Tension Loop2.wav')
		self.tensionBlue.loop(viz.ON)
		
		#set up footsteps
		self.walking = viz.addAudio('audio/Footsteps.wav')
		self.sprinting = viz.addAudio('audio/Footsteps.wav')
		self.sprinting.setRate(1.6)
		
		#set up Fog
		viz.fogcolor(0,0,0)
		viz.fog(2,20)
		
		#set up plot text / corresponding audio
		self.textOne = viz.addText('You Were Here...') #set
		self.textOne.color(viz.RED)
		self.textOne.font("High Tower Text") 
		self.textOne.setAxisAngle(0,1,0,270)
		self.textOne.setPosition(-23.5,1.82,-1)
		self.textOneAudio = viz.addAudio('audio/ywh.wav')
		self.textOnePlayed = False
		
		self.textTwo = viz.addText('Text 2') #set
		self.textTwo.color(viz.RED)
		self.textTwo.font("High Tower Text")
		self.textTwo.setAxisAngle(0,1,0,270)
		self.textTwo.setPosition(-58.75,1.82,19.15)
		self.textTwoAudio = viz.addAudio('audio/ywh.wav')
		self.textTwoPlayed = False
		
		self.textThree = viz.addText('Text 3') #set
		self.textThree.color(viz.RED)
		self.textThree.font("High Tower Text")
		self.textThree.setAxisAngle(0,1,0,180)
		self.textThree.setPosition(-66.25,1.82,-5.8)
		self.textThreeAudio = viz.addAudio('audio/ywh.wav')
		self.textThreePlayed = False
		
		self.textFour = viz.addText('Text 4') #set
		self.textFour.color(viz.RED)
		self.textFour.font("High Tower Text")
		self.textFour.setAxisAngle(0,1,0,90)
		self.textFour.setPosition(-100.4,1.82,3.9)
		self.textFourAudio = viz.addAudio('audio/ywh.wav')
		self.textFourPlayed = False
		
		self.textFive = viz.addText('Text 5') #set
		self.textFive.color(viz.RED)
		self.textFive.font("High Tower Text")
		self.textFive.setPosition(-181.3,1.82,53.1)
		self.textFiveAudio = viz.addAudio('audio/ywh.wav')
		self.textFivePlayed = False
		
		self.textSix = viz.addText('Text 6') #set
		self.textSix.color(viz.RED)
		self.textSix.font("High Tower Text")
		self.textSix.setAxisAngle(0,1,0,90)
		self.textSix.setPosition(-35.63,1.82,-13.4)
		self.textSixAudio = viz.addAudio('audio/ywh.wav')
		self.textSixPlayed = False
		
		self.textSeven = viz.addText('Text 7') #set
		self.textSeven.color(viz.RED)
		self.textSeven.font("High Tower Text")
		self.textSeven.setAxisAngle(0,1,0,180)
		self.textSeven.setPosition(-13.3,1.82,-58.9)
		self.textSevenAudio = viz.addAudio('audio/ywh.wav')
		self.textSevenPlayed = False
		
		self.textEight = viz.addText('Text 8') #set
		self.textEight.color(viz.RED)
		self.textEight.font("High Tower Text")
		self.textEight.setAxisAngle(0,1,0,180)
		self.textEight.setPosition(-78.85,1.82,-94.3)
		self.textEightAudio = viz.addAudio('audio/ywh.wav')
		self.textEightPlayed = False
		
		self.textNine = viz.addText('Text 9') #set
		self.textNine.color(viz.RED)
		self.textNine.font("High Tower Text")
		self.textNine.setAxisAngle(0,1,0,270)
		self.textNine.setPosition(-124,1.82,-45.5)
		self.textNineAudio = viz.addAudio('audio/ywh.wav')
		self.textNinePlayed = False
		
		self.textTen = viz.addText('Text 10') #set
		self.textTen.color(viz.RED)
		self.textTen.font("High Tower Text")
		self.textTen.setAxisAngle(0,1,0,270)
		self.textTen.setPosition(-176.88,1.82,-75.4)
		self.textTenAudio = viz.addAudio('audio/ywh.wav')
		self.textTenPlayed = False
	
		#set up endgame mechanic
		self.endgame = False
		self.endMusic = viz.addAudio('audio/Beginning.wav')
		self.endMusic.loop(viz.ON)
		
		#creat sphere to go around the player camera / add physics
		self.view = viz.MainView 
		self.cambox = vizshape.addSphere(radius = .5, stacks = 40, slices = 40, color = viz.WHITE)
		self.cambox.collideMesh()
		self.cambox.enable(viz.COLLIDE_NOTIFY)
		
		#create urgency variable 
		self.timelimit = 300 #Set for 5 minutes 
		self.text = viz.addText( str(self.timelimit), viz.SCREEN, pos = [.85,.85,0] )
		self.text.color(viz.RED)
		self.text.font("High Tower Text")
		
		#create position
		self.x = -4.6
		self.y = 1.82
		self.z = 3.3
		
		mat = viz.Matrix()
		mat.postTrans(self.x,self.y,self.z)
		self.view.setMatrix(mat)
		
		#Turn the headlight on / set lighting conditions
		self.view.getHeadLight().enable()
		self.view.getHeadLight().color(.2,.2,.2)
		self.view.getHeadLight().intensity(.05)
		self.view.getHeadLight().spread(180)
		self.view.getHeadLight().quadraticattenuation(100)
		self.view.getHeadLight().spotexponent(60)
		
		#set key bind variables
		self.moveForward = 'w'
		self.moveBackward = 's'
		self.moveRight = 'd'
		self.moveLeft = 'a'
		self.sprint = viz.KEY_SHIFT_L
		self.interact = 'e'
		
		# left/right viewing angle, 0 degrees points in direction [1,0,0]
		# with positive angles ccw, and negative angles cw, as viewed from +Y
		self.angleLtRt = 180
		
		# up/down viewing angle, 0 degrees points in direction [1,0,0]
		# negative values look down, positive values look up
		self.angleUpDw = -10
		
		#Velocity vector
		self.dx = math.cos( math.radians( self.angleLtRt ) )
		self.dz = math.sin( math.radians( self.angleLtRt ) )
		
		#Set Up Object Variables 
		#set up blue gate
		self.gateBMod = viz.addChild('models/BlueGate.wrl')
		self.gateBX = -124
		self.gateBY = 0
		self.gateBZ = 30
		mat = viz.Matrix()
		mat.postScale(.3,.3,.3)
		mat.postAxisAngle(1,0,0,90)
		mat.postTrans(self.gateBX,self.gateBY,self.gateBZ)
		self.gateBMod.setMatrix( mat )
		self.gateBMod.collideMesh()
		
		#set up red gate
		self.gateRMod = viz.addChild('models/RedGate.wrl')
		self.gateRX = -138.52
		self.gateRY = 0
		self.gateRZ = -59
		mat = viz.Matrix()
		mat.postScale(.3,.3,.3)
		mat.postAxisAngle(0,0,1,90)
		mat.postAxisAngle(1,0,0,90)
		mat.postTrans(self.gateRX,self.gateRY,self.gateRZ)
		self.gateRMod.setMatrix( mat )
		self.gateRMod.collideMesh()

	
		#set up red key
		self.keyRMod = viz.addChild('models/RedKey.wrl')
		self.keyRX = -91.9
		self.keyRY = 1.82
		self.keyRZ = 33.5
		mat = viz.Matrix()
		mat.postAxisAngle(0,1,0,90)
		mat.postAxisAngle(0,0,1,180)
		mat.postTrans(self.keyRX,self.keyRY,self.keyRZ)
		self.keyRMod.setMatrix( mat )
		self.keyRMod.collideMesh()
		
		#set up blue key
		self.keyBMod = viz.addChild('models/BlueKey.wrl')
		self.keyBX = -122
		self.keyBY = 1.82
		self.keyBZ = -90.8
		mat = viz.Matrix()
		mat.postAxisAngle(0,1,0,90)
		mat.postAxisAngle(0,0,1,180)
		mat.postTrans(self.keyBX,self.keyBY,self.keyBZ)
		self.keyBMod.setMatrix( mat )
		self.keyBMod.collideMesh()
		
		#Player holding key variables
		self.keyBlue = False
		self.keyRed = False
		

		#Add the maze environment
		self.maze = viz.addChild('models/HorrorMazeFinal.wrl')
		mat = viz.Matrix()
		mat.postScale(.3,.3,.3)
		mat.postAxisAngle(0,0,1,90)
		mat.postAxisAngle(1,0,0,90)
		mat.postTrans(0, 0, 0)
		self.maze.setMatrix( mat ) 
		self.maze.collideMesh()
		#enable lighting for the maze
		self.maze.enable(viz.LIGHTING)
		effect = vizfx.addAmbientEffect(color=viz.RED)
		self.maze.apply(effect)
		
		self.walls = viz.addTexture('images/Diamond_Box.jpg')
		self.walls.wrap(viz.WRAP_S, viz.REPEAT)
		self.walls.wrap(viz.WRAP_T, viz.REPEAT)
		self.walls.wrap(viz.WRAP_R, viz.REPEAT)
		self.maze.texture( self.walls )
		
		#end contrsuctor
		
	def setView(self):
		#Update the camera
		mat = viz.Matrix()
		# for convenience, first make view look down +X axis
		mat.postAxisAngle(0,1,0,90)
		
		# rotate orientation up/down 
		mat.postAxisAngle(0,0,1,self.angleUpDw)
		
		# rotate orientation left/right 
		mat.postAxisAngle(0,1,0,-self.angleLtRt)
		
		# position view in the scene
		mat.postTrans(self.x,self.y,self.z)
		
		self.view.setMatrix( mat )
		self.cambox.setMatrix( mat )
		
	def setHUD(self):
		self.text.color(viz.RED)
		self.text.message(str(self.timelimit))
		
	def interaction(self):
		#handle interactions here
		
		dist = 0
		#Within range of the red gate
		dist = math.hypot(self.gateRX - self.x, self.gateRZ - self.z)
		if dist <= 5 and self.keyRed == True:
			self.openRedGate()
			
		#Within range of the blue gate
		dist = math.hypot(self.gateBX - self.x, self.gateBZ - self.z)
		if dist <= 5 and self.keyBlue == True:
			self.openBlueGate()
			
		#within range of the red key
		dist = math.hypot(self.keyRX - self.x, self.keyRZ - self.z)
		if dist <= 5 and self.keyRed == False:
			self.pickUpRedKey()
			
		#within range of the blue key
		dist = math.hypot(self.keyBX - self.x, self.keyBZ - self.z)
		if dist <= 5 and self.keyBlue == False:
			self.pickUpBlueKey()
		else:
			pass
		
	def openBlueGate(self):
		self.starttimer(3, .25, viz.FOREVER)
		
	def openRedGate(self):
		self.starttimer(4, .25, viz.FOREVER)
		
	def pickUpRedKey(self):
		self.background.pause()
		self.endMusic.pause()
		self.tensionBlue.pause()
		self.tensionRed.play()
		self.keyRed = True
		self.keyRMod.visible( viz.OFF )
		self.keyRY += 5
		if (self.keyBlue == True):
			self.resetBlueKey()
		mat = viz.Matrix()
		mat.postAxisAngle(0,1,0,90)
		mat.postAxisAngle(0,0,1,180)
		mat.postTrans(self.keyRX, self.keyRY, self.keyRZ)
		self.keyRMod.setMatrix( mat )
		
	def pickUpBlueKey(self):
		self.background.pause()
		self.endMusic.pause()
		self.tensionRed.pause()
		self.tensionBlue.play()
		self.keyBlue = True
		self.keyBMod.visible( viz.OFF )
		self.keyBY += 5
		if (self.keyRed == True):
			self.resetRedKey()
		mat = viz.Matrix()
		mat.postAxisAngle(0,1,0,90)
		mat.postAxisAngle(0,0,1,180)
		mat.postTrans(self.keyBX, self.keyBY, self.keyBZ)
		self.keyBMod.setMatrix( mat )
		
	def resetRedKey(self):
		self.keyRed = False
		self.keyRMod.visible( viz.ON )
		self.keyRY -= 5
		mat = viz.Matrix()
		mat.postAxisAngle(0,1,0,90)
		mat.postAxisAngle(0,0,1,180)
		mat.postTrans(self.keyRX, self.keyRY, self.keyRZ)
		self.keyRMod.setMatrix( mat )
			
	def resetBlueKey(self):
		self.keyBlue = False
		self.keyBMod.visible( viz.ON )
		self.keyBY -= 5
		mat = viz.Matrix()
		mat.postAxisAngle(0,1,0,90)
		mat.postAxisAngle(0,0,1,180)
		mat.postTrans(self.keyBX, self.keyBY, self.keyBZ)
		self.keyBMod.setMatrix( mat )
			
		
	def cameraMove(self, e):
		#Look around with the mouse
		self.angleLtRt -= e.dx * .3
		self.angleUpDw += e.dy * .3
		self.mx = e.x
		self.my = e.y
		#Update camera
		self.setView()
		
	def onKeyUp(self,key):
		if key == self.sprint:
			self.sprinting.stop()
		elif key == self.moveForward:
			self.walking.stop()
		elif key == self.moveBackward:
			self.walking.stop()
		elif key == self.moveRight:
			self.walking.stop()
		elif key == self.moveLeft:
			self.walking.stop()
		
	def onKeyDown(self,key):
		#store current position
		prevX = self.x
		prevZ = self.z
		
		#calculate vector of direction
		self.dx = math.cos( math.radians( self.angleLtRt ) )
		self.dz = math.sin( math.radians( self.angleLtRt ) )
		
		sz = self.dz*math.cos( math.radians( 90 ) ) - self.dx * math.sin( math.radians( 90 ) )
		sx = self.dz*math.sin( math.radians( 90 ) ) + self.dx * math.cos( math.radians( 90 ) )
		
		#Basic Keybinds
		if key == self.sprint:
			self.x += self.dx *2 *.1
			self.z += self.dz *2 *.1
			self.sprinting.play()
			
		elif key == self.moveForward:
			self.x += self.dx*.15
			self.z += self.dz*.15
			self.walking.play()
			
		elif key == self.moveBackward:
			self.x -= self.dx*.15
			self.z -= self.dz*.15
			self.walking.play()
			
		elif key == self.moveRight:
			self.x += sx*.15
			self.z += sz*.15
			self.walking.play()
			
		elif key == self.moveLeft:
			self.x -= sx*.15
			self.z -= sz*.15
			self.walking.play()
			
		elif key == self.interact:
			self.interaction()
			
		#Manual Looking
		elif key == viz.KEY_LEFT:
			self.angleLtRt += 3
			
		elif key == viz.KEY_RIGHT:
			self.angleLtRt -= 3
			
		elif key == viz.KEY_DOWN:
			self.angleUpDw -= 3
			
		elif key == viz.KEY_UP:
			self.angleUpDw += 3
			
		#Update Camera
		self.setView()
		
		#Restore prev position on collision
		if len(viz.phys.intersectNode(self.cambox)) > 0:
			self.z = prevZ
			self.x = prevX
			self.setView()
		
	def endGame(self):
		#teleport player
		self.x = -4.6
		self.y = 1.82
		self.z = 3.3
		self.angleLtRt = 180
		self.angleUpDw = -10
		self.setView()

		#reset text audio
		self.textOnePlayed = False
		self.textTwoPlayed = False
		self.textThreePlayed = False
		self.textFourPlayed = False
		self.textFivePlayed = False
		self.textSixPlayed = False
		self.textSevenPlayed = False
		self.textEightPlayed = False
		self.textNinePlayed = False
		self.textTenPlayed = False
		
		#kill gate timers
		self.killtimer(3)
		self.killtimer(4)
		
		#Set Up Object Variables 
		#set up blue gate
		self.gateBMod.visible( viz.ON )
		self.gateBX = -124
		self.gateBY = 0
		self.gateBZ = 30
		mat = viz.Matrix()
		mat.postScale(.3,.3,.3)
		mat.postAxisAngle(1,0,0,90)
		mat.postTrans(self.gateBX,self.gateBY,self.gateBZ)
		self.gateBMod.setMatrix( mat )
		
		#set up red gate
		self.gateRMod.visible( viz.ON )
		self.gateRX = -138.52
		self.gateRY = 0
		self.gateRZ = -59
		mat = viz.Matrix()
		mat.postScale(.3,.3,.3)
		mat.postAxisAngle(0,0,1,90)
		mat.postAxisAngle(1,0,0,90)
		mat.postTrans(self.gateRX,self.gateRY,self.gateRZ)
		self.gateRMod.setMatrix( mat )
	
		#set up red key
		self.keyRMod.visible( viz.ON )
		self.keyRX = -91.9
		self.keyRY = 1.82
		self.keyRZ = 33.5
		mat = viz.Matrix()
		mat.postAxisAngle(0,1,0,90)
		mat.postAxisAngle(0,0,1,180)
		mat.postTrans(self.keyRX,self.keyRY,self.keyRZ)
		self.keyRMod.setMatrix( mat )
		
		#set up blue key
		self.keyBMod.visible( viz.ON )
		self.keyBX = -122
		self.keyBY = 1.82
		self.keyBZ = -90.8
		mat = viz.Matrix()
		mat.postAxisAngle(0,1,0,90)
		mat.postAxisAngle(0,0,1,180)
		mat.postTrans(self.keyBX,self.keyBY,self.keyBZ)
		self.keyBMod.setMatrix( mat )
		
		#Player holding key variables
		self.keyBlue = False
		self.keyRed = False
		
		#resetsound
		self.background.stop()
		self.tensionBlue.stop()
		self.tensionRed.stop()
		self.endMusic.stop()

		#set endgame music
		self.endgame = True
	
	def onTimer(self,num):
		#print "self.x" + str(self.x)
		#print "self.z" + str(self.z)
		
		self.setView()
		if num == 2:
			self.timelimit -= 1
			self.tick.play()
			if self.timelimit <= 22:
				self.tensionBlue.pause()
				self.tensionRed.pause()
				self.background.pause()
				self.panic.play()
			elif self.timelimit == 0:
				pass
				
			self.setHUD()
			
		elif num == 3: #blue gate rise
			self.gateBY = self.gateBY + 2
			if self.gateBY >= 30:
				self.gateBMod.visible(viz.OFF)
				self.killtimer(3)
			mat = viz.Matrix()
			mat.postScale(.3,.3,.3)
			mat.postAxisAngle(1,0,0,90)
			mat.postTrans(self.gateBX,self.gateBY,self.gateBZ)
			self.gateBMod.setMatrix( mat )	
			
		elif num == 4: #red gate rise
			self.gateRY = self.gateRY + 2
			if self.gateRY >= 30:
				self.gateRMod.visible(viz.OFF)
				self.killtimer(4)
			mat = viz.Matrix()
			mat.postScale(.3,.3,.3)
			mat.postAxisAngle(0,0,1,90)
			mat.postAxisAngle(1,0,0,90)
			mat.postTrans(self.gateRX,self.gateRY,self.gateRZ)
			self.gateRMod.setMatrix( mat )
			
		dist = math.hypot(-189.99 - self.x, -56.23 - self.z)
		if (dist <= 5):
			self.endGame()
			
		dist = math.hypot(-23.006 - self.x, 2.574 - self.z) #realization
		if (dist <= 13 and self.endgame == True):
			self.endMusic.play()
			
		if (dist <= 16 and self.textOnePlayed == False): #audio plot 1
			self.textOnePlayed = True
			self.textOneAudio.play()
			
		dist = math.hypot(-58.75 - self.x, 19.15 - self.z) #audio plot 2
		if (dist <= 16 and self.textTwoPlayed == False):
			self.textTwoPlayed = True
			self.textTwoAudio.play()
			
		dist = math.hypot(-66.25 - self.x, -5.8 - self.z) #audio plot 3
		if (dist <= 7.3 and self.textThreePlayed == False):
			self.textThreePlayed = True
			self.textThreeAudio.play()
			
		dist = math.hypot(-100.4 - self.x, 3.9 - self.z) #audio plot 4
		if (dist <= 8 and self.textFourPlayed == False):
			self.textFourPlayed = True
			self.textFourAudio.play()
			
		dist = math.hypot(-181.3 - self.x, 53.1 - self.z) #audio plot 5
		if (dist <= 16 and self.textFivePlayed == False):
			self.textFivePlayed = True
			self.textFiveAudio.play()
			
		dist = math.hypot(-35.63 - self.x, -13.4 - self.z) #audio plot 6
		if (dist <= 12 and self.textSixPlayed == False):
			self.textSixPlayed = True
			self.textSixAudio.play()
			
		dist = math.hypot(-13.3 - self.x, -58.9 - self.z) #audio plot 7
		if (dist <= 16 and self.textSevenPlayed == False):
			self.textSevenPlayed = True
			self.textSevenAudio.play()
			
		dist = math.hypot(-78.85 - self.x, -94.3 - self.z) #audio plot 8
		if (dist <= 16 and self.textEightPlayed == False):
			self.textEightPlayed = True
			self.textEightAudio.play()
			
		dist = math.hypot(-124 - self.x, -45.5 - self.z) #audio plot 9
		if (dist <= 8.5 and self.textNinePlayed == False):
			self.textNinePlayed = True
			self.textNineAudio.play()
			
		dist = math.hypot(-176.88 - self.x, -75.4 - self.z) #audio plot 10
		if (dist <= 10 and self.textTenPlayed == False):
			self.textTenPlayed = True
			self.textTenAudio.play()
	
	def onCollideBegin(self,e):
		#print e.obj1, e.obj2
		self.z -=  ( self.dz / 3.9 ) + 1
		self.x -=  ( self.dx / 3.9 ) + 1
		self.setView()
	
#Driver

#Turn on Physics engine
viz.phys.enable()

#Set Window / Background Color / 4x AntiAliasing / FOV 
#viz.window.setSize( 640*2, 480*2 )
viz.window.setName( "Labyrinth of Sins" )
viz.window.setBorder(viz.BORDER_NONE)
viz.window.setFullscreenMonitor( viz.AUTO_COMPUTE )
viz.setMultiSample(4)
viz.fov(60)

#Change Vizard Mouse Nav / Trap mouse in the window / Turn mouse invisible
viz.mouse(viz.OFF)
viz.mouse.setTrap(viz.ON)
viz.mouse.setVisible(viz.OFF)


#Create Environment
h = horror()
	

#create sky gif
def addBackgroundQuad(scene=viz.MainScene):
		group = viz.addGroup(scene=scene)
		group.leftQuad = viz.addRenderNode()
		group.leftQuad.disable(viz.RENDER_RIGHT)
		group.rightQuad = viz.addRenderNode()
		group.rightQuad.disable(viz.RENDER_LEFT)
		
		nodes = viz.ObjectGroup([group.leftQuad,group.rightQuad])
		nodes.setHUD(-1,1,-1,1,True)
		nodes.setOrder(viz.MAIN_RENDER)
		nodes.parent(group)
		group.drawOrder(-10000)
		group.polyMode(viz.POLY_FILL)

		return group

background = addBackgroundQuad()
texture = viz.add('images/mazeBackground.gif')
background.texture(texture) 

#publish settings
viz.setOption('viz.publish.load_message','Labyrinth of Sins')
viz.setOption('viz.publish.load_title','Labyrinth of Sins')
viz.setOption('viz.publish.persistent', 1)
viz.setOption('viz.publish.company','Siena College Computer Graphics')
viz.setOption('viz.publish.product','Labyrinth of Sins')
viz.setOption('viz.window.icon', 'images/illumPentIcon.ico')

#render scene
viz.go( viz.FULLSCREEN)

#plot 