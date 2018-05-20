DATA_DIR=./result_all

#if [[ $# -lt 1 ]]; then
#	echo "buff(MB)"
#fi
#buff=$1

workload=c
bufflist="16384"
factors="
	fillseq
	fillrandom
	readseq
	readrandom
"


echo "memtable.hit"
function norm_perf() {


		factor=$1
		buff=$2
		file_line=1
		skip_ops=0
		data_file=$factor.$buff.dat
		norm_file=$data_file.norm
		echo "# line line2 thread mrep count" > $norm_file
		###file read
		while read line line2 thread memtable ops
		do
			if [[ $line -e 1  ]];
			then
				file_line=$((file_line+1))
				continue
			fi

			if [[ "$memtable" == "toss_baseline" ]];
			then
				skip_ops=$ops
				echo $line $line2 $thread $memtable 1 >> $norm_file
			else 
				
				$norm=$(echo $ops $skip_ops | awk '{print $1/$2}')
				echo $line $line2 $thread $memtable $norm >> $norm_file
			fi	

		done < $data_file

}
for buff in $bufflist; do
		for factor in $factors; do
			norm_perf $factor $buff
		done
done
