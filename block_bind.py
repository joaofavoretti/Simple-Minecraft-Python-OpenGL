from bidict import bidict

from Block import Block
from Dirt import Dirt
from Grass import Grass
from Stone import Stone

BLOCK_BIND = bidict({
    'grass': Grass,
    'dirt': Dirt,
    'stone': Stone
})
