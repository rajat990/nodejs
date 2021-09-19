const express = require('express')
const router = express.Router()
const userDetail = require('../models/user')
    // find all users
router.get('/', async(req, res) => {
        try {
            const users = await userDetail.find()
            res.json(users)
        } catch (error) {
            res.send('Error' + error)
        }
    })
    // get user details by Id
router.get('/:id', async(req, res) => {
        try {
            const user = await userDetail.findById(req.params.id)
            res.json(user)
        } catch (error) {
            res.send('Error' + error)
        }
    })
    // save user details
router.post('/saveUser', async(req, res) => {
        const user = new userDetail({
            first_name: req.body.first_name,
            last_name: req.body.last_name,
            phone_no: req.body.phone_no,
            department_name: req.body.department_name,
            location: req.body.location,
            technology: req.body.technology
        })
        try {
            const out = await user.save()
            res.json(out)
        } catch (error) {
            res.send('error' + error)
        }
    })
    // update user by user ID
router.patch('/:id', async(req, res) => {
    try {
        const user = await userDetail.findById(req.params.id)
        user.first_name = req.body.first_name,
            user.last_name = req.body.last_name,
            user.phone_no = req.body.phone_no,
            user.department_name = req.body.department_name,
            user.location = req.body.location,
            user.technology = req.body.technology
        const userOut = await user.save()
        res.json(userOut)
    } catch (error) {
        res.send('Error' + error)
    }
})
router.delete('/delete/:id', async(req, res) => {
    try {
        const user = await userDetail.findByIdAndDelete(req.params.id)
        console.log(user)
        res.json(user)
    } catch (error) {
        res.send('Error' + error)
    }
})

module.exports = router