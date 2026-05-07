'''Este arquivo será destinado a ser o arquivo principal no projeto, 
o qual iremos usar para importar tudo ja feito'''


import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from menus.menus_e_submenus import iniciar_sistema

iniciar_sistema()