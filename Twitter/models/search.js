const mongoose = require('mongoose');

const searchSchema = new mongoose.Schema({
    userId: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true,
    },
    query: {
        type: String,
        required: true,
    },
    createdAt: {
        type: Date,
        default: Date.now,
    },
    duration: {
        type: Number,
        required: true,
    },
});

module.exports = mongoose.model('Search', searchSchema, 'search');
