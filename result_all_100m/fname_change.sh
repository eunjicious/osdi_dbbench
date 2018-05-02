prev=$1
after=$2
find . -name "*$1*" | sed -e 'p' -e "s/$prev/$after/g" | xargs -n 2 mv

