import os
import sys
file_path = os.path.join(os.path.dirname(__file__), '..')
file_dir = os.path.dirname(os.path.realpath('__file__'))
sys.path.insert(0, os.path.abspath(file_path))
data_dir = file_path + '/Data/'

# ORIGINAL
# =============================================================================
# import os
# import sys
# file_path = os.path.join(os.path.dirname(__file__), '..')
# file_dir = os.path.dirname(os.path.realpath('__file__'))
# sys.path.insert(0, os.path.abspath(file_path))
# data_dir = file_dir + '/Data/'
# =============================================================================
# Lo cambié porque daba una ruta errónea, de forma App/Data en donde Data 
# estaba dentro de App, así que no encontraba los archivos.