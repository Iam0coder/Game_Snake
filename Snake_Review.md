# Оценка сложности алгоритмов Snake

Ниже — оценка основных «алгоритмов» и операций в вашем коде с точки зрения временной и пространственной сложности (Big O):

1. **Snake.get_head_position**  
   - **Время:** O(1) — прямой доступ к первому элементу списка.  
   - **Память:** O(1).

2. **Snake.turn**  
   - **Время:** O(1) — несколько проверок и присвоений.  
   - **Память:** O(1).

3. **Snake.move**  
```python
cur = …                 # O(1)
new = …                 # O(1)
if len(self.positions)>1 and new in self.positions[1:]:
    …                   # проверка столкновения
else:
    self.positions.insert(0, new)    # вставка в начало списка
    if len(self.positions)>self.length:
        self.positions.pop()         # удаление из конца
```
   - **Создание среза** `self.positions[1:]` → O(n) времени и O(n) дополнительной памяти (где n = текущая длина змейки).  
   - **Проверка `new in …`** → O(n) по времени.  
   - **`insert(0, …)`** → O(n) по времени (сдвиг элементов).  
   - **`pop()`** → O(1).  
   - **Итого:** **O(n)** по времени на один ход, **O(n)** по общей памяти (список позиций) и **O(n)** дополнительной памяти на создание среза.

4. **Snake.draw**  
```python
for p in self.positions:
    …  # pygame.draw.rect
```
   - **Время:** O(n) — один проход по всем сегментам змейки.  
   - **Память:** O(1) доп., основная память — сам список `positions`.

5. **Snake.handle_keys**  
   - **Время:** O(E) на итерацию, где E = число событий в очереди (обычно мало).  
   - **Память:** O(1).

6. **Food.randomize_position**  
   - **Время и память:** O(1).

7. **Food.draw**  
   - **Время:** O(1).  
   - **Память:** O(1).

8. **Game.load_high_scores**  
```python
with open(…) as file:
    self.high_scores = json.load(file)
```
   - **Время и память:** O(m), где m = объём данных в файле рекордов.

9. **Game.save_high_score**  
```python
self.high_scores[difficulty].append(...)
self.high_scores[difficulty] = sorted(...)[…:5]
json.dump(...)
```
   - **Добавление в список** → O(1).  
   - **Сортировка списка длины k** → O(k log k) по времени, O(k) по памяти (k — число записей для данной сложности).  
   - **Запись в файл** → O(m) по времени, m = размер JSON.

10. **Интерактивные экраны (game_intro, game_over_screen)**  
   - Это event-loop с отрисовкой константного числа элементов (меню, текст, кнопки).  
   - **Время на кадр:** O(1).  
   - **Память:** O(1).

11. **Game.run (основной игровой цикл)**  
   На каждом тике (`self.clock.tick`):  
   - `handle_keys()` → O(E)  
   - `draw()` → O(n)  
   - `move()` → O(n)  
   - проверка столкновения с едой и `randomize_position()` → O(1)  
   - **Итого:** O(n) по времени на кадр, O(n) по памяти для списка позиций.

---

### Общая картина

- **Временная сложность игры:** растёт **линейно** от текущей длины змейки n — **O(n)** на каждый шаг/кадр.  
- **Пространственная сложность:** **O(n)** для хранения позиций змейки.  
- **Работа с рекордами:** O(m) или O(k log k), где m — объём всего файла, k ≤ 5 — число топ-записей в одной категории.

> **Возможная оптимизация:**  
> - Для проверки столкновения можно хранить позиции в `set` (O(1) на проверку вхождения), а сам список оставлять для отрисовки и порядка сегментов.  
> - Вместо `list.insert(0, …)` и `pop()` можно использовать `collections.deque`, где добавление/удаление с концов — O(1).
