rm -rf result_all
BACK=`pwd`
cd ../osdi_dbbench_expr;./1_collect_data.sh
cd $BACK
mkdir result_all
cp ../osdi_dbbench_expr/result_all/* ./result_all

