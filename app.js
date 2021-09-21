const dot = require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose')
const app = express()
const db_ip = process.env.DB_HOST
const db_port = process.env.DB_PORT
const db_collection_name = process.env.DB_COLLECTION_NAME
const url = `mongodb://${db_ip}:${db_port}/${db_collection_name}`
    // <!-- dasd -->
mongoose.connect(url,
    err => {
        if (err) throw err;
        console.log('connected to MongoDB')
    });

app.use(express.json())
const crudRouter = require('./routes/crudAPI')
app.use('/node', crudRouter)

app.listen(9000, () => {
    console.log('server started')
})