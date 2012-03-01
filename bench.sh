#!/bin/bash

total=0;
iterations=100;

for a in `seq $iterations`
do
    this=`(TIMEFORMAT="%U"; time $* > /dev/null) |& tr -d .`;
    total=`expr $total + $this`;
done

average=`expr $total / $iterations`;

echo "Average: $average";
