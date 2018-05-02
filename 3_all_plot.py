#!/bin/bash

bufflist="64 16384"

#function stat_plot(){
#	factors="
#		memtable.hit 
#		memtable.miss
#		l0.hit
#		l1.hit
#		block.cache.hit
#		block.cache.miss
#	"
#	for buff in $bufflist; do
#		for factor in $factors; do
#			fname=$factor.$buff.dat
#			echo "$fname ...."
#			python2.7 ./stat_plot.py $fname
#		done
#	done
#}

function perf_plot(){
	factors="fillseq fillrandom readseq readrandom"

	for factor in $factors; do
		temp1=$(cat $factor.64.dat | awk '{print $4}' | sort -r -n | head -n 1 )
		temp2=$(cat $factor.16384.dat | awk '{print $4}' | sort -r -n | head -n 1 )
		if [ ${temp1} -ge ${temp2} ];then
			max=$temp1
		else
			max=$temp2
		fi
		echo $max
		max=`expr $max / 1000`	
		echo $max 
	
		if [ ${max} -ge 1000 ];then ##thound
			if [ ${max} -ge 10000 ];then
				max=$(echo $max | awk '{printf"%d",$1 * 1.3}')
				remainder=$(echo $max | awk '{printf"%d", $1 % 1000}')
				max=`expr $max - $remainder`
				echo $max
			else
				max=$(echo $max | awk '{printf"%d",$1 * 1.3}')
				remainder=$(echo $max | awk '{printf"%d", $1 % 100}')
				max=`expr $max - $remainder`
				echo $max
			fi	
		else  ## hundred
			max=$(echo $max | awk '{printf"%d",$1 * 1.3}')
			remainder=$(echo $max | awk '{printf"%d", $1 % 10}')
			max=`expr $max - $remainder`
			echo $max
		fi
		
		for buff in $bufflist; do
			fname=$factor.$buff.dat
			echo "$fname ...."
			python2.7 ./perf_plot.py $fname $max
		done	
		max=0
	done
}

perf_plot


