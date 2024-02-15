import dgl
import torch

class sSet():
  def __init__(self,
               dim=0,
               ):
    
    self.simplices = {0 : {}}