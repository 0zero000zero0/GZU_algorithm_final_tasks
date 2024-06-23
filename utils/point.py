class point:
    def __init__(self,x=0.0,y=0.0) -> None:
        self.x=x
        self.y=y
        self.coordinate=[x,y]

    def __repr__(self) -> str:
        return f'({self.x},{self.y})'

    def __str__(self) -> str:
        return f'({self.x},{self.y})'

    def __getitem__(self, i):
        return self.coordinate[i]
    def __setitem__(self, i):
        return self.coordinate[i]
if __name__=='__main__':
    p=point(1,2)
    print(p)
    print(p[0])
    print(p[1])