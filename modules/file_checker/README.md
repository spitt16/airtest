INTRODUCTION
------------

The purpose of File Checker is to verify that files managed by Drupal actually 
exist at the location where Drupal believes they are.

In a perfect Drupal world your server filesystem and its correspoding entries in 
Drupal's files table are 100% synchronized. But what if parts of your file system 
have been corrupted due to some disk failure? Or one of your modules messed up 
your database and files? Or your deploy script went beserk? Well, then this module 
will help you to monitor and find out which files are out of sync.

File Checker is available for both D7 and D8. These notes are largely for D8.

It offers the following features:

 * You can check all files immediately through the UI or using drush.
 * You can schedule regular checking of all files, triggered by cron or drush.
 * You can check specific files whenever file entities are created or updated.
 * A warning is logged if a file does not exist at the uri of the file entity.
 * Missing files are marked as missing and listed in a view.
 * It works with files stored locally or remotely.
 * It should work with any quantity of files.


USER INTERFACE
--------------
The File checker UI is at admin/config/media/file-system/file-checker.

If you press "Check files now" a bulk file checking will start, using
Drupal's Batch API. A progress bar will be displayed showing the proportion of
files checked so far. You will need to keep the browser window open, and not
navigate away, until checking is finished.

You can view missing files at admin/config/media/file-system/file-checker/missing.


BACKGROUND FILE CHECKING
------------------------
Checking files on remote servers can take a few seconds for each file, and so
checking from the UI becomes impractical when you have many files. Background
file checking solves this problem, and also allows for automated monitoring of
your filesystem's health.

If background checking is under way, you can see its progress and cancel from the UI.

Background checking divides one run of checking all files into many small executions,
to prevent performance problems if any one execution lasts too long. A typical setup
is for a new execution to be scheduled every 60 seconds, and for each execution
to last 50 seconds. Each execution will check as many files as it can in its time.
When there are no more files to check, the run comes to an end.

Given this, controlling background checking from drush or cron involves 2 stages:
* starting, which sets up a run of checking all files. You might schedule this to
happen once each night.
* executing, which actually checks files. You might schedule this to happen every
minute, all the time. If checking has not been started, then executions simply do
nothing and immediately stop. Every run must have at least 2 executions, no matter
how few files are on your system. If you have many remote files, you may need hundreds
of executions. Executions are sequential, so they cannot happen in parallel.

Out of the box, there are 2 ways to run background checking: Drush and Ultimate Cron.


DRUSH COMMANDS
--------------

* drush file-checking-start
Starts background file checking.

* drush file-checking-execute 50
Checks files for 50 seconds.

* drush file-checking-cancels
Cancels background file checking.

Setting up the following in crontab on Linux should cause file checking to
run at 2am each night until all files are checked:

0 2 * * * drush file-checking-start
* * * * * drush file-checking-execute 50



ULTIMATE CRON
-------------

The contrib module Ultimate Cron allows for many ways to control and launch
Drupal cron jobs. File checker provides configuration for 2 cron jobs
that should appear at admin/config/system/cron/jobs when Ultimate Cron is
installed. By default they work the same as the drush commands described
above, but you can edit them in the Ultimate Cron UI to change when they run.
You will need to make sure that Ultimate Cron itself is triggered every
minute, if you want these cron jobs to be triggered at this frequency
by Ultimate Cron.


REQUIREMENTS
------------

File checker has no special requirements.


CHECKING ON FILE ENTITY CHANGES
-------------------------------

You can configure File checker to check files whenever file entity is
created or has its uri changed. To do this, use the settings UI at
admin/config/media/file-system/file-checker.

If you choose 'Immediately' then files will be checked as soon as
they are saved, which may hold up the user experience for a few seconds.

If you choose 'Later', then files will be placed in a Drupal queue, and
checked the next time Drupal's main cron runs and processes its queues.


RECOMMENDED MODULES
-------------------

 * Various monitoring modules would allow you to receive an email notification 
   if missing files were detected.
 
 * Ultimate Cron to trigger background file checking.


INSTALLATION
------------
 
 * Install as you would normally install a contributed Drupal module. See:
   https://www.drupal.org/docs/8/extending-drupal/installing-contributed-modules
   for further information.


DRUPAL 7
--------
For Drupal 7, the module does not add a 'missing' basefield to the files table. Instead, it
uses the existing status field. Out of the box the files table has two kind of statuses: 
Temporary (0) and Permanent (1). This module introduces an additional status Missing (2). 

The file checker can be configured on admin/settings/file_checker. Take a look at the 
"Process batch size" first. Ideally you shouldn't run too many iterations, 
e. g. 100.000 files / 10.000 batch size = 10 runs sounds like a good approach. 
By pressing the button "Flag missing files" you can run the file verification manually.

On admin/reports/file_checker you can view the results.

MAINTAINERS
-----------

Current maintainers:
 * Gottfried Nindl (gnindl) - https://www.drupal.org/u/gnindl
 * Mike Del Tito (mdeltito) - https://www.drupal.org/u/mdeltito
 * Jonathan Shaw (jonathanjfshaw) - https://drupal.org/u/jonathanjfshaw

Supporting organisations:
 * OSCE: Organisation for Security and Co-operation in Europe - http://www.osce.org
 * Awakened Heart Sangha - http://www.ahs.org.uk
