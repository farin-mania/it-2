class Mangekant():
    def __init__(self, sider):
        self.sider = sider

    def input(self, sidelengde):
        self.sidelengde = sidelengde

    def omkrets(self):
        if hasattr(self, "sider") and hasattr(self, "sidelengde"):
            return self.sider * self.sidelengde
        else:
            print("Manger slider eller omkrets")

    def __str__(self) -> str:
        return f"Sider {self.sider} med sidelengde: {self.sidelengde}"



trekant = Mangekant(3)
trekant.input(10)

print(trekant.omkrets())
print(trekant)


class Rektangel(Mangekant):
    def __init__(self, sider):
        super().__init__(sider)