const mongoose = require('mongoose')

const userSchema = new mongoose.Schema({
    first_name: {
        type: String,
        required: true
    },
    last_name: {
        type: String,
        required: true
    },
    phone_no: {
        type: Number,
        required: true
    },
    department_name: {
        type: String,
        required: true
    },
    location: {
        type: String,
        required: true
    },
    technology: {
        type: Array,
        required: true
    }
})

module.exports = mongoose.model('user', userSchema)