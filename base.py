class Base:
  def check_collision(self, coord):
    if coord[1] + 57 >= 1430:
      return True
    return False