import redis from 'redis';

// Create a Redis client
const client = redis.createClient();

// Handle connection events
client.on('connect', () => {
  console.log('Redis client connected to the server');
});
client.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err.message}`);
});

// Function to set a key-value pair in Redis
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

// Function to get the value of a key from Redis
function displaySchoolValue(schoolName) {
  client.get(schoolName, (err, result) => {
    if (err) {
      console.error(err);
    } else {
      console.log(result);
    }
  });
}

// Call the functions as required
displaySchoolValue('ALX');
setNewSchool('ALXSanFrancisco', '100');
displaySchoolValue('ALXSanFrancisco');
