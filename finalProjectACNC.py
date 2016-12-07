#Authors: Anthony Calabrese, Nate Cefarelli
#File: finalProjectACNC.py
import viz
import math
import vizshape
import vizfx

class horror(viz.EventClass):

	def __init__(self):
		# must call constructor of EventClass first!!
		viz.EventClass.__init__(self)
		
		#set callbacks
		self.callback(viz.KEYDOWN_EVENT,self.onKeyDown)
		self.callback(viz.MOUSE_MOVE_EVENT,self.cameraMove)
		self.callback(viz.TIMER_EVENT, self.onTimer)
		self.callback(viz.COLLIDE_BEGIN_EVENT,self.onCollideBegin)
		self.starttimer(1, .25, viz.FOREVER)
		self.starttimer(2, 1, viz.FOREVER)
		
		#start background music
		self.background = viz.addAudio('bellLoop.wav')
		self.background.loop(viz.ON)
		self.background.play()
		
		#set up tick sound
		self.tick = viz.addAudio('tickingSound.wav')
		self.panic = viz.addAudio('HurryMechanic.wav')
		
		#set up key music
		self.tensionRed = viz.addAudio('Tension Loop1.wav')
		self.tensionRed.loop(viz.ON)
		self.tensionBlue = viz.addAudio('Tension Loop2.wav')
		self.tensionBlue.loop(viz.ON)
		
		#creat sphere to go around the player camera / add physics
		self.view = viz.MainView 
		self.cambox = vizshape.addSphere(radius = .5, stacks = 40, slices = 40, color = viz.WHITE)
		self.cambox.collideMesh()
		self.cambox.enable(viz.COLLIDE_NOTIFY)
		
		#create urgency variable 
		self.timelimit = 290
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
		
		#Mouse coordinates
		self.mx = 0
		self.my = 0
		
		#Set Up Object Variables 
		#set up blue gate
		self.gateBMod = viz.addChild('BlueGate.wrl')
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
		self.gateRMod = viz.addChild('RedGate.wrl')
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
		self.keyRMod = viz.addChild('RedKey.wrl')
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
		self.keyBMod = viz.addChild('BlueKey.wrl')
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
		self.maze = viz.addChild('HorrorMazeFinal.wrl')
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
		
		self.walls = viz.addTexture('Diamond_Box.jpg')
		self.walls.wrap(viz.WRAP_S, viz.REPEAT)
		self.walls.wrap(viz.WRAP_T, viz.REPEAT)
		self.walls.wrap(viz.WRAP_R, viz.REPEAT)
		self.maze.texture( self.walls )
		
		
		
		
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
			
		elif key == self.moveForward:
			self.x += self.dx*.15
			self.z += self.dz*.15
			
		elif key == self.moveBackward:
			self.x -= self.dx*.15
			self.z -= self.dz*.15
			
		elif key == self.moveRight:
			self.x += sx*.15
			self.z += sz*.15
			
		elif key == self.moveLeft:
			self.x -= sx*.15
			self.z -= sz*.15
			
		elif key == 'j':
			print 'j'
			self.x = -89
			self.z = 30
			self.setView()
			
		elif key == 'k':
			print 'k'
			self.x = -120
			self.z = -89
			self.setView()
			
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
			#print "move results in collisions - restore previous z coordinate"
			self.z = prevZ
			self.x = prevX
			self.setView()
			
	
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
			self.setHUD()
			
		elif num == 3: #blue gate rise
			self.gateBY = self.gateBY + 2
			if self.gateBY >= 30:
				self.gateBMod.visible(viz.OFF)
			mat = viz.Matrix()
			mat.postScale(.3,.3,.3)
			mat.postAxisAngle(1,0,0,90)
			mat.postTrans(self.gateBX,self.gateBY,self.gateBZ)
			self.gateBMod.setMatrix( mat )	
			
		elif num == 4: #red gate rise
			self.gateRY = self.gateRY + .2
			if self.gateRY >= 30:
				self.gateRMod.visible(viz.OFF)
			mat = viz.Matrix()
			mat.postScale(.3,.3,.3)
			mat.postAxisAngle(0,0,1,90)
			mat.postAxisAngle(1,0,0,90)
			mat.postTrans(self.gateRX,self.gateRY,self.gateRZ)
			self.gateRMod.setMatrix( mat )
	
	def onCollideBegin(self,e):
		#print e.obj1, e.obj2
		self.z -=  ( self.dz / 3.9 ) + 1
		self.x -=  ( self.dx / 3.9 ) + 1
		self.setView()
	
	

#Driver

#Set Window
#viz.window.setSize( 640*2, 480*2 )
viz.window.setSize( 1920, 1080 )
viz.window.setName( "Final Horror Project" )

#Turn on Physics engine
viz.phys.enable()

#Set Window Fullscreen / Background Color / 4x AntiAliasing / FOV 
viz.window.setBorder(viz.BORDER_NONE)
#viz.MainWindow.clearcolor( viz.BLACK ) 


viz.setMultiSample(4)
viz.fov(60)

#Change Vizard Mouse Nav / Trap mouse in the window / Turn mouse invisible
#viz.mouse(viz.ON)
viz.mouse(viz.OFF)
viz.mouse.setTrap(viz.ON)
viz.mouse.setVisible(viz.OFF)


#Create Environment
h = horror()



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
texture = viz.add('mazeBackground.gif')
background.texture(texture) 

#render scene
viz.go()


#Implement Audio in the game


#Self.quit for timer running out
#Endgame mechanics
#plot
#Notes into the environment
#Fog
#Menu
#publish as an exe