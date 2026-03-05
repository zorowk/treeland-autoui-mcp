deplist=$( ldd $1 | awk '{if (match($3,"/")){ print $3}}' )  
sudo cp -L -n $deplist $2  
