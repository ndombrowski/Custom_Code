#search a pattern stored in the first column in a list and replace with pattern stored in second column
#usage: awk -f search_replace.awk file input > output

FNR==NR { array[$1]=$2; next } { for (i in array) gsub(i, array[i]) }1
