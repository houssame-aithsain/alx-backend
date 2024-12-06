import { createQueue } from 'kue';

const blacklistedNumbers = ['4153518780', '4153518781'];
const queue = createQueue();

function processNotification(phoneNumber, message, job, done) {
  // Track job progress, starting at 0%
  job.progress(0, 100);

  // Check if phone number is blacklisted
  if (blacklistedNumbers.includes(phoneNumber)) {
    const errorMsg = `Phone number ${phoneNumber} is blacklisted`;
    console.error(errorMsg);
    return done(new Error(errorMsg)); // Pass failure to the callback without marking the job as failed
  }

  // Track progress to 50% after blacklist check
  job.progress(50, 100);

  // Simulate sending the notification (log the action)
  console.log(`Sending notification to ${phoneNumber} with message: ${message}`);

  // Simulate some delay (1 second) for sending the notification
  setTimeout(() => {
    // Mark job as complete
    console.log(`Notification successfully sent to ${phoneNumber}`);
    done(); // Indicate job completion
  }, 1000);
}

// Process notification jobs from the 'push_notification_code_2' queue
queue.process('push_notification_code_2', 2, (job, done) => {
  const { phoneNumber, message } = job.data;
  processNotification(phoneNumber, message, job, done);
});
