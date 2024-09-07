import agentpy as ap
from owlready2 import *
import random
import json
import socket

onto = get_ontology("file://onto.owl")

def updateUnity():
  # Set get from Unity
  unitySetup["model"]["nextStep"] = unityUpdate['model']['nextStep']

# Get from Unity
unityUpdate = {
  "model": {
    "nextStep": True
  },
  "drone": {
        "warningPoint": (13, 25),
        "isWarningAlert": 1,
        "droneInWarningPos": 0,
        "droneSeeSuspicious": 0,
        "isRealWarning": 1
    },
    "guard": {
        "alertRevised": 0
    },
    "camera": {
        "cameraDetectSuspicious": 1
    }
}

# Setup Get from Unity
unitySetup = {
    "model": {
        "warehouse": [
          ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"],
          ["W", " ", "W", "C", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "W"],
          ["W", " ", "W", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "W"],
          ["W", " ", "W", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "W"],
          ["W", " ", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W"],
          ["W", " ", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W"],
          ["W", " ", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W"],
          ["W", "G", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W"],
          ["W", " ", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W"],
          ["W", " ", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W"],
          ["W", " ", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W"],
          ["W", " ", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W", "W", " ", " ", " ", " ", "W"],
          ["W", " ", "W", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "W"],
          ["W", " ", "W", " ", "D", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "W"],
          ["W", " ", "W", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "C", "W"],
          ["W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W", "W"]
        ],
        "endAgent": False,
        "nextStep": True
    },
}

message = {
    "sender": "Camera",
    "receiver":
      [
        "Guard",
        "Drone"
      ],
    "subject": "Alert",
    "content":
      {
        "cameraDetectSuspicious": 1,
        "warningPoint": (13, 25),
        "isWarningAlert": 1,
        "droneInWarningPos": 0,
        "droneSeeSuspicious": 0,
        "isRealWarning": 0,
        "alertRevised": 0
      },
}

with onto:
    class Entity(Thing):
      pass

    class Drone(Thing):
      pass

    class Guard(Thing):
      pass

    class Camera(Thing):
      pass

    class Wall(Thing):
      pass

    class World(Thing):
      pass

    class Place(Thing):
      pass

    class has_position(DataProperty, FunctionalProperty):
      domain = [Entity]
      range = [str]

    class has_place(ObjectProperty, FunctionalProperty):
      domain = [Entity]
      range = [Place]

class DroneAgent(ap.Agent):
  def next(self):
    for act in self.actions:
      for rule in self.rules:
        if rule(act):
          act()
          return

  def setup(self):
    self.agentType = 0
    self.direction = (-1, 0)
    self.flagPoints = [(13,4), (2,4), (2,10), (13,10), (13,16), (2,16), (2,22), (13,22), (13,28), (2,28)]
    self.isReturn = False
    self.isWarning = False
    self.warningPoint = (0, 0)
    self.inWarningPos = False
    self.droneReturned = False
    self.droneSeeSuspicious = False
    self.rules = (self.rule_1, self.rule_2, self.rule_3, self.rule_4, self.rule_5, self.rule_6, self.rule_7, self.rule_8)
    self.actions = (self.suspicious, self.returnDrone, self.landDrone, self.forward, self.moveUp, self.moveDown, self.moveLeft, self.moveRight)

  def readM(self):
    self.isWarning = message['content']['isWarningAlert']
    self.warningPoint = message['content']['warningPoint']
    self.inWarningPos = message['content']['droneInWarningPos']
    self.droneSeeSuspicious = message['content']['droneSeeSuspicious']

  def readMessage(self):
    if len(message['receiver']) > 1 :
      for receiver in message['receiver']:
        if receiver == "Drone":
          self.readM()
    elif len(message['receiver']) == 1:
      if message['receiver'][0] == "Drone":
        self.readM()
  
  def updateSend(self):
    print(self.direction) # Post Direction to Unity ----------------------------------------------

  def step(self):
    self.readMessage()
    self.updateSend()
    self.next()


  #RULES
  def rule_1(self, act): # Forward
    validador = [False, False]
    isFlag = False
    pos = self.model.grid.positions[self]
    if not self.inWarningPos:
      for flag in self.flagPoints:
        if pos == flag:
          isFlag = True
      if not isFlag:
        validador[0] = True
    if act == self.forward:
        validador[1] = True
    return sum(validador) == 2

  def rule_2(self, act): # MoveUp
    validador = [False, False]
    pos = self.model.grid.positions[self]
    if pos == self.flagPoints[0]:
      self.droneReturned = False
      self.isReturn = False
      validador[0] = True
    if not self.inWarningPos:
      for i in range(0, len(self.flagPoints)):
        if i % 4 == 0 and not self.isReturn:
          if pos == self.flagPoints[i]:
            validador[0] = True
        elif i % 4 == 3 and self.isReturn:
          if pos == self.flagPoints[i]:
            validador[0] = True
    if act == self.moveUp:
        validador[1] = True
    return sum(validador) == 2

  def rule_3(self, act): # MoveDown
    validador = [False, False]
    pos = self.model.grid.positions[self]
    if pos == self.flagPoints[len(self.flagPoints)-1]:
      self.isReturn = True
      validador[0] = True
    if not self.inWarningPos:
      for i in range(0, len(self.flagPoints)):
        if i % 4 == 2 and not self.isReturn:
          if pos == self.flagPoints[i]:
            validador[0] = True
        elif i % 4 == 1 and self.isReturn:
          if pos == self.flagPoints[i]:
            validador[0] = True
    if act == self.moveDown:
        validador[1] = True
    return sum(validador) == 2

  def rule_4(self, act): # MoveLeft
    validador = [False, False]
    pos = self.model.grid.positions[self]
    if self.isReturn and not self.inWarningPos:
      for i in range(0, len(self.flagPoints)):
        if i % 2 == 0 and i != 0:
          if pos == self.flagPoints[i]:
            validador[0] = True
    if act == self.moveLeft:
        validador[1] = True
    return sum(validador) == 2

  def rule_5(self, act): # MoveRight
    validador = [False, False]
    pos = self.model.grid.positions[self]
    if not self.isReturn and not self.inWarningPos:
      for i in range(0, len(self.flagPoints)):
        if i % 2 == 1 and i != 9:
          if pos == self.flagPoints[i]:
            validador[0] = True
    if act == self.moveRight:
        validador[1] = True
    return sum(validador) == 2

  def rule_6(self, act): # LandDrone
    validador = [False, False]
    pos = self.model.grid.positions[self]
    if self.isWarning:
      if self.warningPoint != (0, 0):
        if pos == self.warningPoint:
          validador[0] = True
    if act == self.landDrone:
        validador[1] = True
    return sum(validador) == 2

  def rule_7(self, act): # ReturnDrone
    validador = [False, False]
    pos = self.model.grid.positions[self]
    if self.isWarning and not self.droneReturned:
      if self.warningPoint != (0, 0):
        if self.warningPoint[1] < pos[1]:
          validador[0] = True
        elif self.warningPoint[1] == pos[1] and self.warningPoint[0] > pos[0]:
          validador[0] = True
    if act == self.returnDrone:
        validador[1] = True
    return sum(validador) == 2

  def rule_8(self, act): # Suspicious
    validador = [False, False]
    if self.droneSeeSuspicious:
      validador[0] = True
    if act == self.suspicious:
        validador[1] = True
    return sum(validador) == 2

  #ACTIONS
  def suspicious(self):
    message['sender'] = "Drone"
    message['receiver'] = ["Guard", "Camera"]
    message['subject'] = "Alert"
    message['content']['isWarningAlert'] = 1
    message['content']['droneInWarningPos'] = 1

  def returnDrone(self):
    self.droneReturned = True
    self.isReturn = True
    self.direction = (self.direction[0] * -1, self.direction[1] * -1)

  def landDrone(self):
    print("Land") # Post Land Action to Unity ----------------------------------------------
    message['sender'] = "Drone"
    message['receiver'] = ["Guard"]
    message['subject'] = "Alert"
    message['content']['droneInWarningPos'] = 1
    message['content']['droneSeeSuspicious'] = 0

  def moveUp(self):
    self.direction = (-1, 0)
    self.forward()

  def moveDown(self):
    self.direction = (1, 0)
    self.forward()

  def moveLeft(self):
    self.direction = (0, -1)
    self.forward()

  def moveRight(self):
    self.direction = (0, 1)
    self.forward()

  def forward(self):
    self.model.grid.move_by(self, self.direction)

class GuardAgent(ap.Agent):
  def setup(self):
    self.agentType = 1
    self.first_step = True
    self.pos = None
    self.isWarning = False
    self.inWarningPos = False
    self.alertRevised = False
    self.rules = (self.rule_1, self.rule_2)
    self.actions = (self.revised, self.controll)

  def readM(self):
    self.isWarning = message['content']['isWarningAlert']
    self.inWarningPos = message['content']['droneInWarningPos']
    self.alertRevised = message['content']['alertRevised']

  def readMessage(self):
    if len(message['receiver']) > 1 :
      for receiver in message['receiver']:
        if receiver == "Guard":
          self.readM()
    elif len(message['receiver']) == 1:
      if message['receiver'][0] == "Guard":
        self.readM()

  def step(self):
    if self.first_step:
      self.pos = self.model.grid.positions[self]
      self.first_step = False
    self.readMessage()
    self.next()

  def next(self):
    for act in self.actions:
      for rule in self.rules:
        if rule(act):
          act()
          return

  #RULES
  def rule_1(self, act): # Controll
    validador = [False, False]
    if self.isWarning:
      if self.inWarningPos:
        validador[0] = True
    if act == self.controll:
        validador[1] = True
    return sum(validador) == 2

  def rule_2(self, act): # Revised
    validador = [False, False]
    if self.isWarning:
      if self.inWarningPos:
        if self.alertRevised:
          validador[0] = True
    if act == self.revised:
        validador[1] = True
    return sum(validador) == 2

  #ACTIONS
  def controll(self):
    if unityUpdate['drone']['isRealWarning']:
      print("General Alert") # Post General Alert to Unity ----------------------------------------------
      message['sender'] = "Guard"
      message['receiver'] = ["Firefighters"]
      message['subject'] = "Real Alert"
      message['content']['isRealWarning'] = 1
      unitySetup["model"]["endAgent"] = True

  def revised(self):
    if not unityUpdate['drone']['isRealWarning']:
      print("False Alert") # Post False Alert to Unity ----------------------------------------------
      message['sender'] = "Guard"
      message['receiver'] = ["Drone", "Camera"]
      message['subject'] = "False Alert"
      message['content']['isRealWarning'] = 0
      message['content']['isWarningAlert'] = 0
      message['content']['droneInWarningPos'] = 0
      message['content']['droneSeeSuspicious'] = 0
      message['content']['warningPoint'] = (0, 0)
      message['content']['alertRevised'] = 0

class CameraAgent(ap.Agent):
  def setup(self):
    self.agentType = 2
    self.first_step = True
    self.pos = None
    self.suspiciousDetected = False
    self.rules = self.rule_1
    self.actions = self.notify

  def step(self):
    if self.first_step:
      self.pos = self.model.grid.positions[self]
      self.first_step = False
    self.next()

  def next(self):
    if self.rules(self.actions):
      self.actions()
      return

  #RULES
  def rule_1(self, act): # Notify
    validador = [False, False]
    if not self.suspiciousDetected:
      if unityUpdate['camera']['cameraDetectSuspicious']:
        validador[0] = True
    if act == self.notify:
        validador[1] = True
    return sum(validador) == 2

  #ACTIONS
  def notify(self):
    self.suspiciousDetected = True
    message['sender'] = "Camera"
    message['receiver'] = ["Guard", "Drone"]
    message['subject'] = "Alert"
    message['content']['isWarningAlert'] = 1
    message['content']['warningPoint'] = (13, 25) # Change the warning point with the camera vision

class WallAgent(ap.Agent):
  def setup(self):
    self.agentType = 3
    self.first_step = True
    self.pos = None

  def step(self):
    if self.first_step:
      self.pos = self.model.grid.positions[self]
      self.first_step = False

class WarehouseModel(ap.Model):
    def setup(self):
        self.drones = ap.AgentList(self, len(self.p.drones), DroneAgent)
        self.guards = ap.AgentList(self, len(self.p.guards), GuardAgent)
        self.cameras = ap.AgentList(self, len(self.p.cameras), CameraAgent)
        self.walls = ap.AgentList(self, len(self.p.walls), WallAgent)
        self.grid = ap.Grid(self, (self.p.M, self.p.N), track_empty=True)
        self.grid.add_agents(self.drones, positions=self.p.drones, empty=True)
        self.grid.add_agents(self.guards, positions=self.p.guards, empty=True)
        self.grid.add_agents(self.cameras, positions=self.p.cameras, empty=True)
        self.grid.add_agents(self.walls, positions=self.p.walls, empty=True)

    def step(self):
        self.drones.step()
        self.guards.step()
        self.cameras.step()
        self.walls.step()

def start_socket_server(model):
    server_address = ('localhost', 8888)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(1)  # Allow only one connection for simplicity
    print(f"Server started at {server_address}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        try:
            while True:
                data = client_socket.recv(1024)
                if data:
                    message = data.decode('utf-8')
                    print(f"Received message: {message}")
                    
                    if message == "STOP":
                        print("Stopping server as per client request.")
                        break

                    # Process the data (e.g., update the model state)
                    model.step()  # Call model steps on receiving data

                    drone_direction = f"{model.drones.direction}"

                    response = json.dumps({
                        "direction": drone_direction  # Send the direction in the response
                    })
                    client_socket.sendall(response.encode('utf-8'))
                else:
                    break
        finally:
            client_socket.close()


warehouse = unitySetup['model']['warehouse']

parameters = {
    'M': len(warehouse),
    'N': len(warehouse[0]),
    'drones': [],
    'guards': [],
    'walls': [],
    'cameras': [],
}

# Process the matrix
for row_idx, row in enumerate(warehouse):
    for col_idx, cell in enumerate(row):
        if cell == 'W':
            parameters['walls'].append((row_idx, col_idx))
        elif cell == 'G':
            parameters['guards'].append((row_idx, col_idx))
        elif cell == 'D':
            parameters['drones'].append((row_idx, col_idx))
        elif cell == 'C':
            parameters['cameras'].append((row_idx, col_idx))

model = WarehouseModel(parameters)
model.setup()

while not unitySetup["model"]["endAgent"]:
  updateUnity()
  if unitySetup["model"]["nextStep"]:
    start_socket_server(model)
    unitySetup["model"]["nextStep"] = False

model.end()