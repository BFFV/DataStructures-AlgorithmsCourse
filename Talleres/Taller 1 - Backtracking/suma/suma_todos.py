import numpy as np

class Variable():
  """Representa una numero del problema, y si está incluido o no en la suma"""
  def __init__(self, key, value):
    # La clave única que identifica esta variable
    self.key = key
    # Cuanto vale esta variable para la suma
    self.numeric_value = value
    # Sin asignar
    self.value = 0

  def __str__(self):
    return f"{self.key}:{self.numeric_value}"

  def __repr__(self):
    return str(self)


class SetSum():
  """Representa una instancia del puzzle"""

  def __init__(self, numbers, target):
    # El número al que queremos llegar
    self.target = target
    # Inicialmente no hemos hecho ningun UNDO
    self.undos = 0
    # Combinaciones válidas
    self.combinations = []
    # Cuales son las variables que están incluidas en la suma
    self.included = []
    # Variables sin asignar
    self.unassigned = []
    # Suma total de las variables sin asignar
    self.total = 0

    for (k,v) in numbers.items():
      self.unassigned.append(Variable(k,v))
      self.total += v

  def assign(self, x, value):
    """Asigna una variable y actualiza los contadores"""
    x.value = value

    # Si el valor va incluido en la suma
    if value == 1:
      # Podemos extraerlo del objetivo
      self.target -= x.numeric_value
      # Lo agregamos a lista de valores incluidos
      self.included.append(x)
    # Extraemos su valor del total
    self.total -= x.numeric_value

  def unassign(self, x, value):
    """Desasigna una variable y actualiza los contadores"""
    x.value = 0

    # Si el valor estaba incluido en la suma
    if value == 1:
      # Lo volvemos a agregar al objetivo
      self.target += x.numeric_value
      # Lo quitamos de la lista de valores incluidos
      self.included.pop()
    # Agregamos su valor al total
    self.total += x.numeric_value


  def is_solution(self):
    """Indica que la asignación es una solución para el problema"""
    return len(self.unassigned) == 0

  def choose_unnasigned_variable(self):
    """Obtiene la siguiente variable sin asignar"""
    return self.unassigned.pop()
  
  def is_valid(self, x, value):
    """Revisa que la asignación sea válida."""
    # Si estamos incluyendo el valor
    if value == 1:
      # No se puede pasar del target
      return self.target >= x.numeric_value
    # Si no se está incluyendo
    else:
      return self.target <= self.total - x.numeric_value

  def generate_solutions(self):
    """Revisa recursivamente si el problema es resolvible mediante Backtracking"""

    if self.is_solution():
      return True
    
    x = self.choose_unnasigned_variable()

    for value in [-1, 1]:
      if self.is_valid(x, value):
        self.assign(x, value)

        if self.generate_solutions():
          self.combinations.append(self.included.copy())
        
        self.unassign(x, value)
        self.undos += 1
      
    self.unassigned.append(x)
    return False

  def __str__(self):
    return str(self.combinations)



if __name__ == "__main__":  

  edificios = {
    "Azkaban": 10000,
    "SanAgustin": 6000,
    "RaulDeves": 3000,
    "Domo": 1000,
    "Mall": 3000
  }

  setsum = SetSum(edificios, 10000)

  print(setsum)

  print("--------------------------")

  setsum.generate_solutions()
  print(setsum)
