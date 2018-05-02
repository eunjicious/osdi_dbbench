#!/bin/bash
DB_DIR=/mnt/rocksdb
KVS="rocksdb_orig rocksdb_async rocksdb_sync"

ENABLE_PIPELINE=0
STATISTICS=1

TOT_OPS=`expr 100 \* 1024 \* 1024`
#TOT_OPS=`expr 1 \* 102400`

keysize=16
valsize=256
seek_num=10



###################################
function run(){
	buff=$1
	kvs=$2

	## key configuration 
	if [[ $kvs == "rocksdb_orig" ]]; then 
		mrep_list="skip_list cuckoo prefix_hash hash_linkedlist"
	else
		mrep_list="cuckoo"
	fi

  	for mr in $mrep_list; do
		th=1
		while [[ $th -lt 33 ]]; do
			ops=`expr $TOT_OPS / $th`
			echo "run_common $mr $th $ops $buff"
			fname="$mr"_"$th"_"c"_"$ops"_"$buff"
			#./1_memtable_run.sh $mr $th $disable_wal $ops $buff
			run_common $mr $th $ops $buff
			th=$((th+th))
#			sleep 20
		done
  	done
}


####################################
function run_common(){
	echo "run_common" 
	workload="fillseq,fillrandom,readseq,readrandom"
	mrep=$1
	th_num=$2
	op_num=$3
	buff_size=`expr $4 \* 1024 \* 1024` ## MB

	if [[ $mrep == "skip_list" ]]; then ALLOW_CON=1; else ALLOW_CON=0; fi

	## precheck 
	if [ ! -d $DB_DIR ]; then mkdir $DB_DIR; else rm $DB_DIR/*; fi

	## runs start 
	echo "=================================="
	echo $mrep ... $num_threads
	#res="$mrep"_www"$num_threads".perf
	rfname=$RESULT_DIR/"$mrep"_"$th_num"_"c"_"$op_num"_"$4".perf
	mfname=$RESULT_DIR/"$mrep"_"$th_num"_"c"_"$op_num"_"$4".iostat
	iostat 1 > $mfname & 
	echo "=+++++++++ $rfname" 

#	echo "$EXEC_DIR/db_bench --key_size=$keysize --value_size=$valsize --disable_auto_compactions=0 --write_buffer_size=$_buff_size --sync=0 --verify_checksum=0 --threads=$_th_num --use_existing_db=0 --allow_concurrent_memtable_write=$ALLOW_CON --benchmarks=$workload --memtablerep=$mrep --db=$DB_DIR --num=$num --keys_per_prefix=10 --prefix_size=8 --enable_pipelined_write=$ENABLE_PIPELINE --statistics=$STATISTICS --seek_nexts=$seek_num" > $res


	cline=`echo "$res
	$EXEC_DIR/db_bench \
		--key_size=$keysize \
		--value_size=$valsize \
		--memtablerep=$mrep \
		--db=$DB_DIR \
		--benchmarks=$workload \
		--write_buffer_size=$buff_size \
		--disable_auto_compactions=0 \
		--sync=0 \
		--verify_checksum=0 \
		--threads=$th_num \
		--use_existing_db=0 \
		--allow_concurrent_memtable_write=$ALLOW_CON \
		--num=$op_num \
		--keys_per_prefix=10 \
		--prefix_size=8 \
		--enable_pipelined_write=$ENABLE_PIPELINE \
		--seek_nexts=$seek_num \
		--reads=10 \
		--statistics=$STATISTICS 
	"`

	echo $cline > $rfname
	$cline >> $rfname
	kill -9 `ps aux | grep "iostat" | grep -v "grep" | awk '{print $2}'`
	mv $DB_DIR/LOG $rfname.log
}


###########################
#           main         #
###########################
#run 16384
#run 32768

for kvs in $KVS; do
	EXEC_DIR=`pwd`/$kvs
	if [ ! -d $EXEC_DIR ]; then echo "$EXEC_DIR does not exist";  exit; fi

	RESULT_DIR=`pwd`/result_common_"$kvs"
	if [ ! -d $RESULT_DIR ]; then 
		mkdir $RESULT_DIR
#	else
#		suffix=`date +%H%M%S`
#		backup=`echo "$RESULT_DIR"_"$suffix"`
#		mv $RESULT_DIR $backup
#		mkdir $RESULT_DIR
	fi

	run 16384 $kvs
done

