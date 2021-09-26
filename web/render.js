const router = require("express").Router();
const db = require("./database");
const {getSupplierInfo, getCustomerInfo} = require("./database");
const axios = require("axios");
const api = "http://localhost:5000/api";

router.get('/', (req, res) => {
    res.render('index');
})

router.get('/supplier/:inn', async (req, res) => {
    try {
        const {inn} = req.params;
        const {day} = req.query;

        const dateGroups = await axios.get(`${api}/provider/${day}`);

        const groups = [...await db.getMostPopularSeasonedGroups(inn,
            dateGroups.data.products)].map(row=> row.kpgz);
        const items = [...await db.getItemsFromGroups(inn, groups, true)]
            .map(row=>({id: row['ID СТЕ'], name: row['Название СТЕ'], category: row['Категория']}));

        res.render('recommends', {items, info: await getSupplierInfo(inn)})
    } catch (e) {
        res.status(500).send(e);
    }
});

router.get('/customer/:inn', async (req, res) => {
    try {
        const {inn} = req.params;
        const {day} = req.query;

        const groups = await axios.get(`${api}/customer/${inn}&${day}`);
        const items = [...await db.getItemsFromGroups(inn, groups.data.products, false)]
            .map(row=>({id: row['ID СТЕ'], name: row['Название СТЕ'], category: row['Категория']}));

        res.render('recommends', {items, info: await getCustomerInfo(inn)})
    } catch (e) {
        res.status(500).send(e);
    }
});

module.exports = router;