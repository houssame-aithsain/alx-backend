import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

// Redis client setup
const redisClient = redis.createClient();
redisClient.on('connect', () => {
  console.log('Connected to Redis server');
});

// Promisify Redis methods for async/await
const getAsync = promisify(redisClient.get).bind(redisClient);
const setAsync = promisify(redisClient.set).bind(redisClient);

// Kue queue setup
const queue = kue.createQueue();
let reservationEnabled = true;

// Function to reserve a seat
const reserveSeat = async (number) => {
  await setAsync('available_seats', number);
};

// Function to get current available seats
const getCurrentAvailableSeats = async () => {
  const seats = await getAsync('available_seats');
  return seats;
};

// Express setup
const app = express();
const port = 1245;

// Function to initialize available seats and server
const initializeApp = async () => {
  // Set initial available seats to 50
  await setAsync('available_seats', 50);

  // Start the Express server
  app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
  });
};

// Route to get available seats
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservations are blocked' });
  }

  const job = queue.create('reserve_seat', {}).save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });

  // Print job completion/failure
  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
  });
});

// Route to process the queue
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    if (availableSeats <= 0) {
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
      return;
    }

    // Decrease available seats by 1
    await reserveSeat(availableSeats - 1);

    if (availableSeats - 1 === 0) {
      reservationEnabled = false;
    }

    done();
  });
});

// Initialize the app with available seats and server
initializeApp();
