while read line           
 do           
 echo $line
 
 cd data/
 mkdir "$line"
 cd ..

 cd reviews/
 #mkdir $1
 cd ..

 python search.py "$line"
 
 done < "queries"

exit


cd data/
mkdir $1
cd ..

cd reviews/
#mkdir $1
cd ..

python search.py $1
