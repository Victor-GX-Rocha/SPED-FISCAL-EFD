""" 
from src.efd_interactor import EfdInterector, AppConfig

efd_interector = EfdInterector(AppConfig())
efd_interector.open()
"""

import os, time, shutil

dest_dir = 'erro'
current_path = os.path.abspath('a.a')
filename = os.path.basename(current_path)
dest_path = os.path.join(dest_dir, filename)

print(
f'''
{dest_dir = },
{current_path = },
{filename = },
{dest_path = }
'''
)
if os.path.exists(dest_path):
    base, ext = os.path.splitext(filename)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    new_name = f"{base}_{timestamp}{ext}"
    dest_path = os.path.join(dest_dir, new_name)

print(
f'''
{dest_path}
'''
)

shutil.move(current_path, dest_path)

# if not os.path.exists('processado'):
#     os.mkdir('processado')

# os.makedirs('processado', exist_ok=True)

# print(os.path.basename('main.py'))
# print(os.path.abspath('main.py'))

# import shutil

# shutil.move(os.path.abspath('main.py'), 'processado')
# shutil.move(os.path.abspath('46377727002218-353100786114-20250101-20250131-0-AF2854AA9F89B7A3A0B30E9A6DD1044F2BE8F277-SPED-EFD_limpo_20260705_220444.txt'), 'erro')
# def move_file(src_path, dest_dir):
#     """Move o arquivo para o diretório de destino (processado ou erro)."""
#     try:
#         os.makedirs(dest_dir, exist_ok=True)
#         filename = os.path.basename(src_path)
#         dest_path = os.path.join(dest_dir, filename)
        
#         # Evitar sobrescrita: adicionar timestamp se existir
#         if os.path.exists(dest_path):
#             base, ext = os.path.splitext(filename)
#             timestamp = time.strftime("%Y%m%d_%H%M%S")
#             new_name = f"{base}_{timestamp}{ext}"
#             dest_path = os.path.join(dest_dir, new_name)
        
#         shutil.move(src_path, dest_path)
#         logger.info(f"Arquivo movido para {dest_path}")
#     except Exception as e:
#         logger.exception(f"Falha ao mover {src_path}: {e}")
#         raise