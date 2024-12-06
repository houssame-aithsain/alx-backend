import redis from 'redis';

// Create a Redis client
const subscriber = redis.createClient();

// Handle connection events
subscriber.on('connect', () => {
  console.log('Redis client connected to the server');
});

subscriber.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

// Subscribe to the channel
subscriber.subscribe('ALXchannel');

// Handle messages
subscriber.on('message', (channel, message) => {
  console.log(message);

  // Handle server kill message
  if (message === 'KILL_SERVER') {
    subscriber.unsubscribe();
    subscriber.quit();
  }
});
