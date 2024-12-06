/* eslint-disable no-undef */
import kue from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job'; // Assuming this is the correct path to the function.

describe('createPushNotificationsJobs', () => {
  let queue;

  beforeEach(() => {
    // Set up Kue with test mode enabled
    queue = kue.createQueue();
    queue.testMode = true;
  });

  afterEach(() => {
    // Clear the queue after each test
    queue.testMode = false; // Disable test mode
    queue.shutdown(500, () => {}); // Shutdown the queue to clear jobs
  });

  it('should display an error message if jobs is not an array', () => {
    try {
      createPushNotificationsJobs({}, queue);
    } catch (err) {
      // Expect the error message to be "Jobs is not an array"
      expect(err.message).toBe('Jobs is not an array');
    }
  });

  it('should create jobs in the queue', (done) => {
    const jobs = [
      {
        phoneNumber: '4153518780',
        message: 'This is the code 1234 to verify your account'
      },
      {
        phoneNumber: '4153518781',
        message: 'This is the code 5678 to verify your account'
      }
    ];

    createPushNotificationsJobs(jobs, queue);

    queue.process('push_notification_code_3', (job, done) => {
      console.log(`Notification job created: ${job.id}`);
      done();
    });

    // Validate that two jobs were created in the queue
    setTimeout(() => {
      const jobCount = queue.testMode.jobs.length;
      expect(jobCount).to.equal(2); // We expect two jobs to be created
      done();
    }, 50);
  });

  it('should log progress, completion, and failure for jobs', (done) => {
    const jobs = [
      {
        phoneNumber: '4153518782',
        message: 'This is the code 9876 to verify your account'
      }
    ];

    createPushNotificationsJobs(jobs, queue);

    queue.process('push_notification_code_3', (job, done) => {
      job.progress(10, 100); // Simulating progress
      console.log(`Notification job ${job.id} 10% complete`);
      job.progress(50, 100); // Simulating progress
      console.log(`Notification job ${job.id} 50% complete`);
      job.complete(); // Mark the job as complete
      console.log(`Notification job ${job.id} completed`);
      done();
    });

    setTimeout(() => {
      const jobCount = queue.testMode.jobs.length;
      expect(jobCount).to.equal(1); // Only one job should be created in this case
      done();
    }, 50);
  });
});
