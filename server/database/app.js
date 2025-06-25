const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');

const app = express();
const port = 3030;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));

const reviewsData = JSON.parse(
  fs.readFileSync('reviews.json', 'utf8'),
);
const dealershipsData = JSON.parse(
  fs.readFileSync('dealerships.json', 'utf8'),
);

mongoose.connect(
  'mongodb://mongo_db:27017/',
  { dbName: 'dealershipsDB' },
);

const Reviews = require('./review');
const Dealerships = require('./dealership');

(async function seedDatabase() {
  try {
    await Reviews.deleteMany({});
    await Reviews.insertMany(reviewsData.reviews);

    await Dealerships.deleteMany({});
    await Dealerships.insertMany(dealershipsData.dealerships);

    console.log('Database seeded successfully.');
  } catch (error) {
    console.error('Error seeding database:', error);
  }
})();

app.get('/', (req, res) => {
  res.send('Welcome to the Mongoose API');
});

app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await Reviews.find({});
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

app.get('/fetchReviews/dealer/:id', async (req, res) => {
  const { id } = req.params;

  try {
    const documents = await Reviews.find({ dealership: id });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

app.get('/fetchDealers', async (req, res) => {
  try {
    const documents = await Dealerships.find({});
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

app.get('/fetchDealers/:state', async (req, res) => {
  const { state } = req.params;

  try {
    const documents = await Dealerships.find({ state });
    res.json(documents);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

app.get('/fetchDealer/:id', async (req, res) => {
  const { id } = req.params;

  try {
    const document = await Dealerships.findOne({ id });
    res.json(document);
  } catch (error) {
    res.status(500).json({ error: 'Error fetching document' });
  }
});

app.post('/insert_review', async (req, res) => {
  const data = req.body;

  try {
    const [latest] = await Reviews.find({})
      .sort({ id: -1 })
      .limit(1);
    const newId = (latest?.id || 0) + 1;

    const review = new Reviews({
      id: newId,
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year,
    });

    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.error('Error inserting review:', error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
