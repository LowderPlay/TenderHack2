const fs = require("fs");
const axios = require("axios");
const router = require("express").Router();

if(!fs.existsSync("cache/")) fs.mkdirSync("cache");

router.get("/:cte.jpg", async (req, res) => {
    const { cte } = req.params;
    const local = `${__dirname}/cache/${cte}.jpg`;
    if(fs.existsSync(local)) {
        console.log(`using local file for ${cte}`)
        return res.sendFile(local);
    }
    console.log(`fetching image for ${cte}`);
    try {
        const info = await axios
            .get(`https://old.zakupki.mos.ru/api/Cssp/Sku/GetEntity?id=${cte}`);
        const image = await axios
            .get(`https://zakupki.mos.ru/newapi/api/Core/Thumbnail/${info.data.images[0].fileStorage.id}/300/300`,
                {responseType: 'stream'});
        const writer = fs.createWriteStream(local);
        image.data.pipe(writer);
        writer.on('finish', ()=>{
            res.sendFile(local);
        })
    } catch (e) {
        res.status(500).sendFile(`${__dirname}/404.jpg`);
    }
});

module.exports = router;