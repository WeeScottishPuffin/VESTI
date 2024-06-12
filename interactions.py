curGarageId:int = 0
curLisenceId:int = 0

#No way in python that I know of to get a class object with a certain value. Workaround below
lisenceList={}

class Car:
  def __init__(self,licensePlate:str,brand:str,model:str,colour:str) -> None:
    self.lisencePlate = licensePlate
    self.brand = brand
    self.model = model
    self.colour = colour

  def getLisencePlate(self) -> str:
    return self.lisencePlate

  def getBrand(self) -> str:
    return self.brand

  def getModel(self) -> str:
    return self.model

  def getColour(self) -> str:
    return self.colour

class Lisence:
  def __init__(self,lisenceHolder:Car,validGarageId:int) -> None:
    global curLisenceId
    global idList
    self.uniqueId, self.id = curLisenceId, curLisenceId
    curLisenceId += 1
    self.lisenceHolder = lisenceHolder
    self.validGarageId = validGarageId
    lisenceList[lisenceHolder] = self #Workaround

  def getLisenceHolderPlate(self) -> Car:
    return self.lisenceHolder.getLisencePlate()

  def getValidInGarageId(self) -> int:
    return self.validGarageId

class Garage:
  def __init__(self,parkedCars:list,maxCapacity:int) -> None:
    global curGarageId
    self.uniqueId, self.id = curGarageId, curGarageId
    curGarageId += 1
    self.parkedCars = parkedCars
    self.maxCapacity = maxCapacity

  def checkIfValid(self, car:Car, lisence:Lisence) -> bool:
    return (self.getCapacity() < self.maxCapacity 
           and lisence.getLisenceHolderPlate() == car.getLisencePlate() 
           and lisence.getValidInGarageId() == self.getId())
    
  def parkCar(self, car:Car) -> bool: #Return type is bool in the casus
    try:
      if self.checkIfValid(car,lisenceList[car]): 
        self.parkedCars.append(car)
        return True
    except: pass
    return False

  def unparkCar(self, car:Car) -> None:
    if car in self.parkedCars:
      self.parkedCars.remove(car)
      #return True                      #Wheras here it is not. Still added it for completeness
    #return False

  def getCarByLisence(self,lisence:str) -> Car | None:
    for car in self.parkedCars:
      if car.lisencePlate == lisence:
        return car
    return None

  def getCarByModel(self,model:str) -> Car | None:
    for car in self.parkedCars:
      if car.model == model:
        return car
    return None

  def getId(self) -> int:
    return self.id

  def getCapacity(self) -> int:
    return len(self.parkedCars)