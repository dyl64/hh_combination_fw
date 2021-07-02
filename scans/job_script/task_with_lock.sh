#!/usr/bin/env bash

# - Source your job definition (MODIFY THIS TO YOUR LOCAL SETUP!)
source ${hh_combination_fw_path}/scans/job_script/job_model_scan.sh 

# - Lock options

LOCKDIR=${hh_combination_fw_path}/scans/job_script/scans/locks
LOCKFILE=${LOCKDIR}/job.lock
MAXTRYLOCK=10000000
LOCKDELAY=5

##############################
### --- Lock mechanism --- ###
##############################

trytolock()
{
   # - Create a symlink from the LOCKFILE pointing to DUMMY
   # - `2>/dev/null` means rerouting the error stream to /dev/null
   # - For all practical purposes what this function does is the following:
   # - 1, Try creating a lockfile symlink
   # - 2, a) if it succeeds it returns 0 and jumps to the next line
   #         which tells the shell that it should remove the lock 
   #         upon exiting.
   # - 2, b) if it fails it returns 2 and exits the function
   DUMMY=$HOSTNAME-$$
	ln -s ${DUMMY} ${LOCKFILE} 2>/dev/null || return 2
	trap removelock EXIT
}


removelock()
{
	rm -f $LOCKFILE
	trap : EXIT
	GOTLOCK=0
}


main()
{
   TRYLOCK=0

	# - While loop which tries to get the
   while [ $TRYLOCK -lt $MAXTRYLOCK ] ; do 
   if trytolock ; then 
           GOTLOCK=1
           break
   else
           TRYLOCK=$(( $TRYLOCK + 1 ))
           echo "Failed to get the lock"
           sleep $LOCKDELAY
   fi
   done
	# - End of while loop
   
	# - At this point you either:
	# - a) have to lock and GOTLOCK is 1
	# - b) don't have the lock and GOTLOCK != 1, so you exit
   if [ $GOTLOCK -ne 1 ] ; then
   	echo "Reached ${MAXTRYLOCK} failed attempts getting a lock. Exiting..."
   	exit 1
   fi

	# - Create lock
	to_be_locked

	# - After finishing up the lock is removed.
	removelock
	echo "Remove lock"


	### - Job - ###
	echo "Job should be starting now."
	job $1

}

####################################

# - Start main()
main $1

