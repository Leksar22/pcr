# gnuplot plot_script.gnu


set term x11 persist

set ticslevel 0
set view 60,30

# Установка заголовка и меток осей
set title "Pipe"
set xlabel "X"
set ylabel "Y"
set zlabel "Z"

# Установка палитры цветов
set palette rgbformulae 33,13,10

# Построение графика из файла 'data' с использованием точек и подписями
splot 'data' u 1:2:3 w points pt 7 ps 1.5 lc palette t "Points"
pause -1