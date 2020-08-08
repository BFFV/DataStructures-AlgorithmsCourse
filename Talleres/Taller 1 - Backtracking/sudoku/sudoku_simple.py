import numpy as np
from timeit import default_timer as timer


class Variable():
  """Representa una celda del problema, con un valor asignado y un dominio"""
  def __init__(self, row, col):
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
    return str(self.value)

  def __repr__(self):
    return str(self)

class Sudoku():
  """Representa una instancia del puzzle"""

  def __init__(self, initial):
    # Números contenidos en cada fila
    self.rows  = [set() for _ in range(9)]
    # Números contenidos en cada columna
    self.cols  = [set() for _ in range(9)]
    # Números contenidos en cada cuadrante
    self.quads = {(qrow, qcol): set() for qrow in range(3) for qcol in range(3)}

    # Tablero de variables
    self.board = [[Variable(row, col) for col in range(9)] for row in range(9)]

    # Inicialmente no hemos hecho ningun UNDO
    self.undos = 0

    # Variables sin asignar
    self.unassigned = []

    # Recorremos el tablero inicial
    for row in range(9):
      for col in range(9):
        # Si la celda esta sin asignar
        if initial[row][col] == 0:
          # Agregamos su variable a la lista de variables que tenemos que asignar
          self.unassigned.append(self.board[row][col])
        # Si viene asignada
        else:
          # Entonces asignamos la variable asociada y actualizamos los contadores
          self.assign(self.board[row][col], initial[row][col])

    

  def assign(self, x, value):
    """Asigna una variable y actualiza los contadores"""
    x.value = value

    # Avisamos que su fila, columna y cuadrante ahora contienen ese valor
    self.rows[x.row]   |= {value}
    self.cols[x.col]   |= {value}
    self.quads[x.quad] |= {value}

  def unassign(self, x, value):
    """Desasigna una variable y actualiza los contadores"""
    x.value = 0

    # Avisamos que su fila, columna y cuadrante ya no contienen ese valor
    self.rows[x.row]   -= {value}
    self.cols[x.col]   -= {value}
    self.quads[x.quad] -= {value}

    # Contamos un UNDO
    self.undos += 1

  def is_solution(self):
    """Indica que la asignación es una solución para el problema"""
    return len(self.unassigned) == 0

  def choose_unnasigned_variable(self):
    """Obtiene la siguiente variable sin asignar"""
    return self.unassigned.pop()
  
  def is_valid(self, x, value):
    """Revisa que la asignación sea válida."""
    # Si esa fila ya tiene ese número
    if value in self.rows[x.row]:
      return False
    # Si esa columna ya tiene ese número
    if value in self.cols[x.col]:
      return False
    # Si ese cuadrante ya tiene ese número
    if value in self.quads[x.quad]:
      return False
    return True  

  def is_solvable(self):
    """Revisa recursivamente si el problema es resolvible mediante Backtracking"""

    if self.is_solution():
      return True
    
    x = self.choose_unnasigned_variable()

    for value in [1,2,3,4,5,6,7,8,9]:
      if self.is_valid(x, value):
        self.assign(x, value)

        if self.is_solvable():
          return True
        
        self.unassign(x, value)
    
    # Devolvemos la variable a la lista de "por asignar"
    self.unassigned.append(x)
    return False

  def __str__(self):
    return str(np.array(self.board))



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

  sudoku = Sudoku(B)

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
