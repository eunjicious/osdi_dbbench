
ALL_DIR=result_all
#
#if [ -d $ALL_DIR ]; then
#	echo "$ALL_DIR already exists. Remove it(y/n)?" 
#	read ans
#	if [[ $ans == "y" ]]; then
#		rm -rf $ALL_DIR
#		mkdir $ALL_DIR
#	fi
#fi
#


### 
prefix="result_common_rocksdb_"
kvs="orig async sync"


for _kvs in $kvs; do
	dir=$prefix$_kvs
	echo $dir

	if [[ $_kvs == "async" ]] || [[ $_kvs == "sync" ]]; then
		prev="cuckoo"
		after=`echo toss_$_kvs`
		find $dir -name "$prev*" | sed -e 'p' -e "s/$prev/$after/g" | xargs -n 2 mv
	fi
	cp $dir/* $ALL_DIR
	ls $ALL_DIR
done
