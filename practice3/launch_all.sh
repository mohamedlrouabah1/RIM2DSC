cd src
# for exo in 1 2 3 5 7 9
for exo in 7 9
do
    echo "Launching exo$exo"
    python3 main.py -e $exo
done
cd -