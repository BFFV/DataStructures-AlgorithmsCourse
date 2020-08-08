import time
from timeit import default_timer as timer
from pqdict import minpq

class Variable():
  """Representa una celda del problema, con un valor asignado y un dominio"""
  def __init__(self, row, col):
    # Los números del 1 al 9
    self.domain = {1,2,3,4,5,6,7,8,9}
    # Sin asignar
    self.value = 0 
    # Guardamos las coordenadas de la celda
    self.row = row
    self.col = col
    # Guardamos el cuadrante de la celda
    qrow = row // 3
    qcol = col // 3
    self.quad = (qrow, qcol)
  
  def __str__(self):
    if self.value == 0:
      return str(self.domain).replace(", ","")
    return str(self.value)

  def __repr__(self):
    return str(self)

class Sudoku():
  """Representa una instancia del puzzle"""

  def __init__(self, initial):
    # Variables contenidas en cada fila
    self.rows  = [set() for _ in range(9)]
    # Variables contenidas en cada columna
    self.cols  = [set() for _ in range(9)]
    # Variables contenidas en cada cuadrante
    self.quads = {(qrow, qcol): set() for qrow in range(3) for qcol in range(3)}

    # Tablero de variables
    self.board = [[Variable(row, col) for col in range(9)] for row in range(9)]

    # Inicialmente no hemos hecho ningun UNDO
    self.undos = 0

    # Variables sin asignar: una cola de prioridad que prioriza el número más pequeño
    self.unassigned = minpq()

    # Recorremos el tablero de variables para relacionar as variables entre ellas
    for row in range(9):
      for col in range(9):
        var = self.board[row][col]
        
        # Agregamos cada celda a su filas / columnas / y cuadrantes correspondiente
        self.cols[col] |= {var}
        self.rows[row] |= {var}
        self.quads[var.quad] |= {var}    
    
    for row in range(9):
      for col in range(9):
        var = self.board[row][col]

        # Todas las variables que afecta esta variable
        var.vecinos = self.cols[col] | self.rows[row] | self.quads[var.quad] - {var}

    # Recorremos el tablero original para actualizar los dominios de las variables
    for row in range(9):
      for col in range(9):
        var = self.board[row][col]

        # Si la celda esta sin asignar
        if initial[row][col] == 0:
          # Agregamos su variable a la lista de variables que tenemos que asignar.
          # Su prioridad es el tamaño de su dominio
          self.unassigned[var] = len(var.domain)
        # Si viene asignada
        else:
          # Entonces asignamos la variable asociada y actualizamos los dominios de las demas
          self.assign(var, initial[row][col])
  
  def assign(self, x, value):
    """Asigna una variable y actualiza los dominios de sus vecinos. Entrega una lista de los vecinos modificados"""
    x.value = value

    modified = []

    # Actualizamos el dominio de los vecinos, eliminando este valor
    for var in x.vecinos:
      # Solo modificamos los dominios de variables sin asignar
      if var.value == 0 and value in var.domain:
        var.domain -= {value}
        modified.append(var)
        # Actualizamos la prioridad de esta variable
        self.unassigned[var] = len(var.domain)
    
    return modified

  def unassign(self, x, value, modified):
    """Desasigna una variable y restaura las variables modificadas"""
    x.value = 0

    # Le devolvemos el valor a los que lo perdieron con esta variable
    for var in modified:
      var.domain |= {value}
      # Actualizamos la prioridad de esta variable
      self.unassigned[var] = len(var.domain)

    # Contamos un UNDO
    self.undos += 1

  def is_solution(self):
    """Indica que la asignación es una solución para el problema"""
    return len(self.unassigned) == 0

  def choose_unnasigned_variable(self):
    """Obtiene la siguiente variable sin asignar. Está será la con el dominio más pequeño"""
    var, _ = self.unassigned.popitem()
    return var
  
  def is_valid(self, x, value):
    """Revisa que la asignación sea válida."""
    return True  

  def is_solvable(self):
    """Revisa recursivamente si el problema es resolvible mediante Backtracking"""

    if self.is_solution():
      return True
    
    x = self.choose_unnasigned_variable()

    for value in x.domain:
      if self.is_valid(x, value):
        modified = self.assign(x, value)

        if self.is_solvable():
          return True
        
        self.unassign(x, value, modified)

    # Devolvemos la variable a la lista de "por asignar" con su prioridad original
    self.unassigned[x] = len(x.domain)
    return False

  def __str__(self):
    """Convierte el tablero en un string con filas y columnas alineadas"""
    s = [[str(e) for e in row] for row in self.board]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return '\n'.join(table)



if __name__ == "__main__":

  # Empty sudoku

  A = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0]    
  ]

  # 3x3 Sudoku Evil Puzzle ID: 5,928,177 [https://www.puzzle-sudoku.com/?size=5]

  B = [
    [6,0,0,1,0,0,0,7,4],
    [1,3,0,0,0,7,5,6,0],
    [0,7,4,0,5,0,1,0,0],
    [0,4,0,0,0,0,0,0,5],
    [0,0,7,0,0,0,9,0,0],
    [2,0,0,0,0,0,0,4,0],
    [0,0,3,0,9,0,7,5,0],
    [0,2,1,8,0,0,0,9,3],
    [7,6,0,0,0,3,0,0,1]
  ]

  # "Hard to solve by brute force"

  C = [
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,3,0,8,5],
    [0,0,1,0,2,0,0,0,0],
    [0,0,0,5,0,7,0,0,0],
    [0,0,4,0,0,0,1,0,0],
    [0,9,0,0,0,0,0,0,0],
    [5,0,0,0,0,0,0,7,3],
    [0,0,2,0,1,0,0,0,0],
    [0,0,0,0,4,0,0,0,9]
  ]

  start = timer()

  sudoku = Sudoku(A)

  print(f"Preprocesado en {timer() - start}s")

  print(sudoku)

  print("--------------------------")

  start = timer()

  if sudoku.is_solvable():
    print(sudoku)
  else:
    print("No se pudo resolver")

  print(f"Resuelto en {timer() - start}s")

  print(f"Me equivoqué {sudoku.undos} veces")
