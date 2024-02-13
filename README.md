# openfoam ПЦР СУПЕР МЕГА РАСЧЕТЫ

1. Скопировать из source исходник в текущую директорию проекта:
cp -r cp -r ./sources/tube .
2. Переместиться в рабочую директорию /tube
cd tube/
3. Собрать сетку
blockMesh
4. Запустить решатель
foamJob buoyantBoussinesqPimpleFoam
5. Для просмотров логов можно заюзать команду
tail -f log
6. Запустить paraFoam

Возможные проблемы:
Q: Падает компилятор на перегрузке sqrt
A: Привести к конкретному типа с плавющей точкой. Например, так:
Было:
sqrt(($R - $Rb)*($R - $Rb) + $L*$L)
Стало:
sqrt((double)($R - $Rb)*($R - $Rb) + $L*$L)

Q: Не запускается paraFoam
A: Либо ошибка сборки со стороны разработки, либо не поддерживается дистрибутивом. Нужно установить paraViewe:
sudo apt install paraview

Q: Где посмотреть список доступных решателей
A: В папке с установленным openfoam
/usr/lib/openfoam/openfoam2312/applications/solvers
Узнать где установлен openfoam можно с помощью which openfoam