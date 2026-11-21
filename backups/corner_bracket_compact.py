"""
Компактный трёхсторонний L-образный угловой кронштейн под 1 винт М3 и 1 гайку на каждую стенку.
Соединяет 3 стенки: заднюю, боковую и верхнюю (толщина 3.6 мм).

Особенности:
- Компактный размер: полки 20×20×20 мм (толщина полок 6 мм).
- По 1 винту М3 и 1 гайке М3 на каждую стенку (всего 3 винта и 3 гайки).
- Встроенные шестигранные гнёзда под гайки М3 (DIN 934, S=5.5 мм) на внутренней стороне.
- Гайки удерживаются от проворота, затягиваются снаружи одной отвёрткой.
- Открытый L-образный профиль полок: максимальная прочность при минимальном весе и объёме.
"""
import cadquery as cq
import math

# ==========================================
# ПАРАМЕТРЫ КРОНШТЕЙНА (МЕНЯЙТЕ ПРИ НЕОБХОДИМОСТИ)
# ==========================================
arm_len = 20.0          # Длина полок кронштейна вдоль стенок, мм
flange_t = 6.0          # Толщина полок, мм
wall_thickness = 3.6    # Толщина стенки корпуса, мм

# Параметры крепежа М3
screw_d = 3.4           # Отверстие под винт М3 (свободная посадка), мм
nut_s = 5.7             # Размер гнезда под гайку М3 «под ключ» (S=5.5 + 0.2 зазор), мм
nut_depth = 2.6         # Глубина гнезда под гайку М3 (толщина гайки 2.4 мм), мм
nut_r = nut_s / (2 * math.cos(math.pi / 6))  # Описанный радиус шестигранника

# Положение центра винта от внешнего угла
pos = 13.0              # Центр отверстия от точки стыка стенок, мм

# ==========================================
# ПОСТРОЕНИЕ ГЕОМЕТРИИ
# ==========================================
# Система координат:
# (0, 0, 0) — точка схождения 3 наружных стенок.
# Плоскость Y = 0: Задняя стенка (Back)
# Плоскость X = 0: Боковая стенка (Side)
# Плоскость Z = 0: Верхняя стенка (Top)

# 1. Базовый габаритный куб 20×20×20 мм
base_box = (
    cq.Workplane("XY")
    .rect(arm_len, arm_len, centered=False)
    .extrude(-arm_len)
)

# 2. Вырезаем внутреннюю полость, образуя 3 L-образные полки толщиной flange_t (6 мм)
inner_cut = (
    cq.Workplane("XY")
    .workplane(offset=-flange_t)
    .transformed(offset=cq.Vector(flange_t, flange_t, 0))
    .rect(arm_len, arm_len, centered=False)
    .extrude(-(arm_len - flange_t + 2))
)
bracket = base_box.cut(inner_cut)

# ==========================================
# СВЕРЛЕНИЕ ОТВЕРСТИЙ И ГНЁЗД ПОД ГАЙКИ
# ==========================================

# 1. ЗАДНЯЯ СТЕНКА (грань Y = 0, отверстие идёт по +Y)
hole_back = cq.Solid.makeCylinder(
    screw_d / 2, flange_t + 2,
    cq.Vector(pos, -1, -pos),
    cq.Vector(0, 1, 0)
)
pocket_back = (
    cq.Workplane("XZ")
    .workplane(offset=-(flange_t - nut_depth))
    .transformed(offset=cq.Vector(pos, -pos, 0))
    .polygon(6, nut_r * 2)
    .extrude(-(nut_depth + 0.5))
)
bracket = bracket.cut(hole_back).cut(pocket_back)

# 2. БОКОВАЯ СТЕНКА (грань X = 0, отверстие идёт по +X)
hole_side = cq.Solid.makeCylinder(
    screw_d / 2, flange_t + 2,
    cq.Vector(-1, pos, -pos),
    cq.Vector(1, 0, 0)
)
pocket_side = (
    cq.Workplane("YZ")
    .workplane(offset=(flange_t - nut_depth))
    .transformed(offset=cq.Vector(pos, -pos, 0))
    .polygon(6, nut_r * 2)
    .extrude(nut_depth + 0.5)
)
bracket = bracket.cut(hole_side).cut(pocket_side)

# 3. ВЕРХНЯЯ СТЕНКА (грань Z = 0, отверстие идёт по -Z)
hole_top = cq.Solid.makeCylinder(
    screw_d / 2, flange_t + 2,
    cq.Vector(pos, pos, 1),
    cq.Vector(0, 0, -1)
)
pocket_top = (
    cq.Workplane("XY")
    .workplane(offset=-(flange_t - nut_depth))
    .transformed(offset=cq.Vector(pos, pos, 0))
    .polygon(6, nut_r * 2)
    .extrude(-(nut_depth + 0.5))
)
bracket = bracket.cut(hole_top).cut(pocket_top)

# ==========================================
# ЭКСПОРТ
# ==========================================
step_file = "corner_bracket_compact.step"
stl_file = "corner_bracket_compact.stl"

cq.exporters.export(bracket, step_file)
cq.exporters.export(bracket, stl_file)

print("Готово! Компактный L-образный кронштейн сохранён:")
print(f" - STEP: {step_file}")
print(f" - STL:  {stl_file}")
print(f"Габариты: {arm_len}×{arm_len}×{arm_len} мм, толщина полок {flange_t} мм")
print("Крепёж: 3× М3 с гайками (по 1 винту на каждую стенку)")
print(f"Для стенки {wall_thickness} мм рекомендуются винты М3×10 мм или М3×12 мм")
