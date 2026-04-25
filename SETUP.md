# Как работать с репозиторием
1. Создайте папку проекта, например `sqllessons`
```
mrdir sqllessons
```
2. Перейдите в созданную папку `sqllessons`
```
cd sqllessons
```
3. Выполните комманду для клонирования репозитория в текущую директорию
```
git clone git@github.com:barmaley350/SQLLessons.git . 
```
4. Создайте виртуальное окружение и установите необходимые зависимости в проект
```
uv sync
```
5. Внесите изменения в `jupyter_notebooks/examples.ipynb`
6. Сгенерируйте новый файл `README.md`
```
uv run python3 main.py
```
