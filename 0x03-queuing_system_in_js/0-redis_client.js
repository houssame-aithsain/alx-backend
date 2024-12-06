import redis from 'redis';

// Create a Redis client
const client = redis.createClient();

// Handle connection event
client.on('connect', function() {
  console.log('Redis client connected to the server');
});

// Handle error event
client.on('error', function(err) {
  console.log(`Redis client not connected to the server: ${err}`);
});
