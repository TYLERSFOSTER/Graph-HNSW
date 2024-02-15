import dgl
import torch

import tier
import quotient_tower
import simplicial_set


def make_tier():
  output = tier.Tier()

  return output
  

if __name__ == '__main__':
  try:
    tier_0 = make_tier()
  except Exception as inst:
      print(type(inst))
      print(inst.args)
      print(inst) 

