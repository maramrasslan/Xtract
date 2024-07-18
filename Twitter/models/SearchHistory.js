//./models/SearchHistory
const mongoose = require('mongoose');

const searchHistorySchema = new mongoose.Schema({
    service: { type: String, default: 'Twitter'},
    query: { type: String, required: true },
    date: { type: Date, default: Date.now },
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
});

module.exports = mongoose.model('SearchHistory', searchHistorySchema, 'searchhistories');
