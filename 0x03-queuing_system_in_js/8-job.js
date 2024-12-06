/**
 * Creates push notification jobs in the queue and logs job events.
 * @param {Array} jobs - Array of job objects to be added to the queue.
 * @param {Object} queue - Kue queue object to process the jobs.
 * @throws {Error} If jobs is not an array.
 */
function createPushNotificationsJobs(jobs, queue) {
    if (!Array.isArray(jobs)) {
      throw new Error('Jobs is not an array');
    }

    // Loop through each job in the jobs array
    jobs.forEach((jobData) => {
      // Create a job for the 'push_notification_code_3' queue
      const job = queue.create('push_notification_code_3', jobData)
        .save((err) => {
          if (err) {
            console.error(`Error creating job: ${err}`);
          } else {
            // Log the job creation event
            console.log(`Notification job created: ${job.id}`);
          }
        });

      // Job events
      job.on('complete', () => {
        console.log(`Notification job ${job.id} completed`);
      });

      job.on('failed', (err) => {
        console.log(`Notification job ${job.id} failed: ${err}`);
      });

      job.on('progress', (progress, total) => {
        const percent = Math.floor((progress / total) * 100);
        console.log(`Notification job ${job.id} ${percent}% complete`);
      });
    });
}

export default createPushNotificationsJobs;
