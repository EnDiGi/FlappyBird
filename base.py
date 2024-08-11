class Base:
  def check_collision(self, coord, height):
    if coord[1] + 28 >= height - 100:
      return True
    return False