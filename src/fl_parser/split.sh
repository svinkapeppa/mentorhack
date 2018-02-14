i=0;
for f in *;
do
    d=dir_$(printf %03d $((i/260000+1)));
    mkdir -p $d;
    mv "$f" $d;
    let i++;
done