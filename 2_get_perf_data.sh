DATA_DIR=./result_all

#if [[ $# -lt 1 ]]; then
#	echo "buff(MB)"
#fi
#buff=$1

workload=c
#tot_ops=`expr 100 \* 1024 \* 1024`
tot_ops=`expr 1 \* 1024 \* 1024`
tot_ops=`expr 1 \* 102400`
#mrep="skip_list cuckoo"
mrep="skip_list cuckoo prefix_hash hash_linkedlist toss_async toss_sync toss_ccuck"
mrep="skip_list cuckoo toss_async toss_sync toss_ccuck"
bufflist="16384"
factors="
	fillseq
	fillrandom
	readseq
	readrandom
"


echo "memtable.hit"

function get_stat() {
	factor=$1

	for buff in $bufflist; do
		echo "========= $factor $buff ==========="
		data_file=$factor.$buff.dat
		echo "# line line2 thread mrep count" > $data_file
		#echo "# line thread mrep count" > $data_file
		touch tmp
		th=1
		line=1
		mul=1
		while [[ $th -lt 31 ]]; do
			line2=$line
			ops=`expr $tot_ops / $th`
	  		for mr in $mrep; do
				prefix="$mr"_"$th"_"$workload"_"$ops"_"$buff"
				fname=$prefix.perf
				echo $fname
				if [ ! -e $fname ]; then
					echo "$fname is not found"
					#th=$((th+th))
					continue
				fi
				count=`cat $fname | grep -v rocks | grep $factor | awk '{print $5}'`
				#count=`cat $fname | grep "memtable.hit" | awk '{print $NF}'`
				#cat $fname | grep -v "Percentile" | grep "rocksdb" | awk -F: '$2!=0 {print $0}'
				#echo "./1_memtable_run.sh $mr $th $workload $ops $buff"
	#			./1_memtable_run.sh $mr $th $workload $ops $buff
				#echo $line $th $mr $count >> tmp
				echo $line $line2 $th $mr $count >> tmp
				line=$((line+1))
	#			sleep 5
			done	
			th=`expr $mul \* 5`
			mul=$((mul+1))
			#th=$((th+th))
			line=$((line+1))
	  	done
		sort -n tmp >> $data_file
		rm tmp
		cat $data_file
		echo $data_file
#		mv $data_file $DATA_DIR
	done
}

######
cd $DATA_DIR
for factor in $factors; do
	get_stat $factor		
done
