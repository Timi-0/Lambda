import boto3
import datetime
# Creates an rds client
rds = boto3.client('rds')
###########################################################################################################################################
############  IMPORTANT::::::::: MUST SET THE "DAYS" AND "DELETE" VARIABLE  TO AN INTEGER AND THE DBInstanceIdentifier TO A STRING ########
###########################################################################################################################################

#How many days before snapshot is copied
DAYS=33

#Create a variable DELETE to set how many days before manual snapshot is deleted
DELETE=56

#Lists available snapshots based on the DBInstanceIdentifier and SnapshotType(automated)
snapshots = rds.describe_db_snapshots(
            DBInstanceIdentifier='ade',
                SnapshotType='automated'
                )

#List available manual snapshots based on SnapshotType and DBInstanceIdentifier
snapshot = rds.describe_db_snapshots(
            DBInstanceIdentifier='ade',
                SnapshotType='manual'
                )

#Sets the DBSnapshotIdentifier to a variable
SnapIdent = snapshots['DBSnapshots'][0]['DBSnapshotIdentifier']

#Sets the DBInstanceIdentifier to a variable
SnapInstIdent = snapshots['DBSnapshots'][0]['DBInstanceIdentifier']

# Add the number of days before the snapshot is copied to the snapshotscreatetime and set the date to a variable called DueDate
DueDate = snapshots['DBSnapshots'][0]['SnapshotCreateTime'] + datetime.timedelta(days=DAYS)

# Set the snapshot create date to SnapDate
SnapDate = SnapIdent[-16:]

#Create a string by concatonating the DBInstanceName and the date and set the string to a variable called NewSnap
NewSnap = SnapInstIdent + "-" + SnapDate

#Create a condition that compares if the Duedate is less than( if the due date has passed) or equal to the present time, copy snapshot
if DueDate <= datetime.datetime.now(snapshots['DBSnapshots'][0]['SnapshotCreateTime'].tzinfo):
    print("Taking Snapshot...")
    copy = rds.copy_db_snapshot(
            SourceDBSnapshotIdentifier=SnapIdent,
            TargetDBSnapshotIdentifier=NewSnap)
else:
    print("No Snapshots to copy...")


# Add the number of days before the snapshot is deleted to the snapshotscreatetime and set the date to a variable called DeleteDate
DeleteDate = snapshot['DBSnapshots'][0]['SnapshotCreateTime'] + datetime.timedelta(days=DELETE)

#Set a variable for DB snapshot Identifier taken from the list of manual snapshots
DeleteSnapIdent = snapshot['DBSnapshots'][0]['DBSnapshotIdentifier']

#Create a condition that compares if the DeleteDate is less than( if the delete date has passed ) or equal to the present time, delete snapshot
if DeleteDate <= datetime.datetime.now(snapshot['DBSnapshots'][0]['SnapshotCreateTime'].tzinfo):
    print(f"Deleting Snapshot...{DeleteSnapIdent}")
    delete = rds.delete_db_snapshot(
    DBSnapshotIdentifier=DeleteSnapIdent
)
else:
    print("No snapshots to delete")
copy-automated-snapshots-and-delete-manual-snapshots.py
Displaying copy-automated-snapshots-and-delete-manual-snapshots.py.
