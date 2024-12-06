import kue from 'kue';

// Create a Kue queue
const queue = kue.createQueue();

// Define the sendNotification function
const sendNotification = (phoneNumber, message) => {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
};

// Set up the queue process to listen for jobs in the 'push_notification_code' queue
queue.process('push_notification_code', (job, done) => {
  const { phoneNumber, message } = job.data;
  sendNotification(phoneNumber, message);
  done(); // Mark the job as completed
});
