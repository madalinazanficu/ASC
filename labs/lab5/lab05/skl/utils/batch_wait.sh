#!/bin/bash
read -a array
# last element int the ouput of sbatch is the job_id
job_id=${array[-1]}
# echo $job_id

#wait until the job has finished
still_in_queue=1
while [ $still_in_queue == 1 ]
do
  sleep 1
  still_in_queue=$(squeue  | awk 'NR>1 {print $1}' | grep $job_id | wc -l)
  #echo "waiting"
done

#print th job output
cat slurm-$job_id.out

#test if the script is working
#sbatch --time 01:00:00 -p hpsl batch_sleep.sh | ./batch_wait.sh