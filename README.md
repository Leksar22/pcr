# openfoam ПЦР

1. Скопировать из source исходник в текущую директорию проекта:
cp -r cp -r ./sources/tube .
2. Переместиться в рабочую директорию /tube
cd tube/
3. Собрать сетку
blockMesh
4. Добавить решатель в sytem/controlDict в поле application
5. Запустить решатель (подтянется с контрола)
buoyantBoussinesqPimpleFoam 
6. Для просмотров логов можно заюзать команду
tail -f log 
7. Запустить paraFoam

*. Параллельный запуск
decomposePar
mpirun -np 4 buoyantBoussinesqPimpleFoam -parallel
??????????reconstructPar -latestTime??????????????
https://www.openfoam.com/documentation/guides/latest/man/reconstructPar.html
touch results.foam
https://www.youtube.com/watch?v=YdYHDMygNPU&ab_channel=Interfluo

Возможные проблемы:
Q: Падает компилятор на перегрузке sqrt
A: На замену компилятора нет реакций. Самый оптимальный вариант: сделать точечно правки и подстроиться под компилятор. В данном кейс так:
Было:
sqrt(($R - $Rb)*($R - $Rb) + $L*$L)
Стало:
sqrt((double)($R - $Rb)*($R - $Rb) + $L*$L)

Q: Не запускается paraFoam
A: Либо ошибка в сборке/зависимостях со стороны разработки, либо не поддерживается дистрибутивом. Нужно установить paraViewe:
sudo apt install paraview

Q: Где посмотреть список доступных решателей
A: В папке с установленным openfoam
/usr/lib/openfoam/openfoam2312/applications/solvers
Узнать где установлен openfoam можно с помощью which openfoam