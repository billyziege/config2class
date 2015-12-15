class A(object):
  def __init__(self,a1,a2=0,a3=1, a4=0,a5=None):
    A.a1 = a1
    A.a2 = a2

class B(A):
  def __init__(self,b1,b2,b3="b",a3=0,**kwargs):
    B.b2 = b2
    A.__init__(B,b1,b3,a3=a3,
               **kwargs)
