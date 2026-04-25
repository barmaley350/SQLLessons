# Порядок выполнения SQL‑запроса (логический)


Важно различать **порядок написания** SQL‑запроса и **порядок его выполнения** — они не совпадают. Разберу пошагово логический порядок обработки команд.

## Порядок выполнения


1. **`FROM` / `JOIN`**
   * Определяются источники данных: таблицы и соединения (`JOIN`).
   * Формируется базовый набор строк для дальнейшей обработки.


2. **`WHERE`**
   * Фильтрация строк: отбрасываются записи, не удовлетворяющие условиям.
   * Обработка происходит **до группировки**.


3. **`GROUP BY`**
   * Данные группируются по указанным столбцам.
   * Каждая группа содержит строки с одинаковыми значениями в указанных столбцах.

4. **Агрегирующие функции** (`SUM`, `COUNT`, `AVG` и т. д.)
   * Вычисляются над данными в группах.
   * Например, `COUNT(*)` считает количество строк в каждой группе.

5. **`HAVING`**
   * Фильтруются группы, не соответствующие условиям.
   * В отличие от `WHERE`, работает с **результатами агрегации**.

   * Пример: `HAVING COUNT(*) > 5` оставит только группы с более чем 5 строками.

6. **Оконные функции**
   * Выполняются вычисления по «окнам» строк (определённым `PARTITION BY` и `ORDER BY`).
   * Примеры: `ROW_NUMBER()`, `LAG()`, `SUM() OVER()`.

7. **`SELECT`**
   * Выбираются столбцы и выражения для итогового результата.
   * Создаются алиасы (псевдонимы) через `AS`.
   * На этом этапе становятся доступны для использования результаты оконных функций.

8. **`DISTINCT`**
   * Удаляются дублирующиеся строки из результата.
   * Применяется после выбора столбцов.

9. **`UNION` / `INTERSECT` / `EXCEPT`**
   * Объединяются результаты нескольких запросов.
   * `UNION` — объединение, `INTERSECT` — пересечение, `EXCEPT` — разность.

10. **`ORDER BY`**
    * Сортировка строк по указанным столбцам или выражениям.
    * Можно использовать алиасы из `SELECT`.
    * По умолчанию — по возрастанию (`ASC`), для убывания — `DESC`.

11. **`OFFSET`**
    * Пропускаются указанное количество строк.
    * Часто используется для постраничной навигации.
    * Пример: `OFFSET 10` пропустит первые 10 строк.

12. **`LIMIT` / `FETCH` / `TOP`**
    * Ограничивается количество возвращаемых строк.
    * `LIMIT 5` вернёт не более 5 строк.
    * Выполняется **в самом конце**, после всех остальных операций.

---

## Важные нюансы

* **Оптимизатор СУБД** может менять реальный порядок выполнения для повышения эффективности, но **логический порядок** остаётся таким, как описано выше.
* Нельзя использовать алиас из `SELECT` в `WHERE` или `GROUP BY` — на момент их выполнения `SELECT` ещё не выполнен.
* Оконные функции вычисляются **после** агрегации и `HAVING`, поэтому их нельзя использовать в `WHERE`.
* Для обхода ограничений можно использовать **CTE** (`WITH`) или подзапросы: сначала вычислить нужные значения, затем фильтровать по ним.

---

## Пример

Запрос:
```sql
SELECT name, SUM(amount) AS total
FROM orders
JOIN customers ON orders.customer_id = customers.id
WHERE order_date >= '2023-01-01'
GROUP BY name
HAVING SUM(amount) > 1000
ORDER BY total DESC
LIMIT 10;
```

Порядок выполнения:
1. Соединяем таблицы `orders` и `customers` (`FROM` + `JOIN`).
2. Оставляем только заказы с 2023 года (`WHERE`).
3. Группируем по имени клиента (`GROUP BY`).
4. Считаем сумму заказов для каждого клиента (`SUM(amount)`).
5. Отбрасываем клиентов с суммой меньше 1000 (`HAVING`).
6. Выбираем столбцы `name` и `total` (`SELECT`).
7. Сортируем по убыванию суммы (`ORDER BY`).
8. Оставляем топ‑10 клиентов (`LIMIT`).

# О базе данных **Chinook**
**База данных примеров Chinook** — это общедоступная база данных с открытым исходным кодом, созданная разработчиком Microsoft Линном Рутом.

Она широко используется в обучающих материалах и курсах.

В каждой таблице базы данных хранится достоверная информация о продажах музыки:
- **album** — названия альбомов и исполнители
- **artist** — информация об исполнителях
- **track** — отдельные музыкальные треки с указанием альбома, жанра и типа носителя
- **genre** — список доступных музыкальных жанров
- **customer** — контактные данные и местоположение клиентов
- **invoice** — счета клиентов
- **invoice_item** — позиции, включенные в каждый счет
- **playlist** — плейлисты, созданные пользователями
- **playlist_track** — сопоставление плейлистов и треков
- **employee** — данные о сотрудниках и представителях службы поддержки 

# Схема базы данных **Chinook**
![img_1](files/scheme.png)

# Примеры запросов при работе с базой данных **Chinook**

##  Подключаем необходимые модули


```python
import sqlite3
from pathlib import Path

import pandas as pd
```


```python
db_path = Path(Path.cwd().parent) / "db/chinook.db"
conn = sqlite3.connect(db_path)
```

##  Выбрать все записи из таблицы `customer`
Запрос `SELECT * FROM customer LIMIT 5;` извлекает все столбцы из таблицы `customer` и возвращает первые 5 строк данных — остальные записи игнорируются.


```python
sql = "SELECT * FROM customer LIMIT 5;"
data = pd.read_sql_query(sql, conn)
data
```




<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CustomerId</th>
      <th>FirstName</th>
      <th>LastName</th>
      <th>Company</th>
      <th>Address</th>
      <th>City</th>
      <th>State</th>
      <th>Country</th>
      <th>PostalCode</th>
      <th>Phone</th>
      <th>Fax</th>
      <th>Email</th>
      <th>SupportRepId</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>Luís</td>
      <td>Gonçalves</td>
      <td>Embraer - Empresa Brasileira de Aeronáutica S.A.</td>
      <td>Av. Brigadeiro Faria Lima, 2170</td>
      <td>São José dos Campos</td>
      <td>SP</td>
      <td>Brazil</td>
      <td>12227-000</td>
      <td>+55 (12) 3923-5555</td>
      <td>+55 (12) 3923-5566</td>
      <td>luisg@embraer.com.br</td>
      <td>3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Leonie</td>
      <td>Köhler</td>
      <td>NaN</td>
      <td>Theodor-Heuss-Straße 34</td>
      <td>Stuttgart</td>
      <td>NaN</td>
      <td>Germany</td>
      <td>70174</td>
      <td>+49 0711 2842222</td>
      <td>NaN</td>
      <td>leonekohler@surfeu.de</td>
      <td>5</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>François</td>
      <td>Tremblay</td>
      <td>NaN</td>
      <td>1498 rue Bélanger</td>
      <td>Montréal</td>
      <td>QC</td>
      <td>Canada</td>
      <td>H2G 1A7</td>
      <td>+1 (514) 721-4711</td>
      <td>NaN</td>
      <td>ftremblay@gmail.com</td>
      <td>3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Bjørn</td>
      <td>Hansen</td>
      <td>NaN</td>
      <td>Ullevålsveien 14</td>
      <td>Oslo</td>
      <td>NaN</td>
      <td>Norway</td>
      <td>0171</td>
      <td>+47 22 44 22 22</td>
      <td>NaN</td>
      <td>bjorn.hansen@yahoo.no</td>
      <td>4</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>František</td>
      <td>Wichterlová</td>
      <td>JetBrains s.r.o.</td>
      <td>Klanova 9/506</td>
      <td>Prague</td>
      <td>NaN</td>
      <td>Czech Republic</td>
      <td>14700</td>
      <td>+420 2 4172 5555</td>
      <td>+420 2 4172 5555</td>
      <td>frantisekw@jetbrains.com</td>
      <td>4</td>
    </tr>
  </tbody>
</table>
</div>


