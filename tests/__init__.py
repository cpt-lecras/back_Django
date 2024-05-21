import os
import sys

# Получаем путь к родительской директории проекта
project_root = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.dirname(project_root)



# Добавляем родительскую директорию в sys.path
sys.path.append(parent_dir)