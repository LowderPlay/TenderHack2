const mysql = require("mysql");
const connection = mysql.createConnection({
    host     : 'localhost',
    user     : 'root',
    password : 'root',
    database : 'dataset'
});

connection.connect(function(err) {
    if (err) {
        return console.error('error connecting: ' + err.stack);
    }
    console.log('connected as id ' + connection.threadId);
});

function getMostPopularSeasonedGroups(inn, seasonedGroups) {
    return new Promise((resolve, reject) => {
        connection.query(`
            SELECT \`Код КПГЗ\` AS kpgz, COUNT(\`Код КПГЗ\`) AS \`value_occurrence\`
            FROM dataset.items
            WHERE \`ID СТЕ\` IN (SELECT *
                                 FROM json_table(
                                              (SELECT json_extract(json_arrayagg(\`СТЕ\`), '$**.Id') as ids
                                               FROM dataset.contracts
                                               WHERE \`ИНН поставщика\` = ?), '$[*]'
                                                  columns( id int path '$')
                                          ) as jt)
              AND \`Код КПГЗ\` IN (?)
            GROUP BY \`Код КПГЗ\`
            ORDER BY \`value_occurrence\` DESC LIMIT 100;
        `, [inn, seasonedGroups], function (error, results) {
            if(error) return reject(error);
            resolve(results);
        });
    });
}
function getItemsFromGroups(inn, groups, supplier) {
    return new Promise((resolve, reject) => {
        connection.query(`
            SELECT *
            FROM dataset.items
            WHERE \`ID СТЕ\` IN (SELECT *
                                 FROM json_table((SELECT json_extract(json_arrayagg(\`СТЕ\`), '$**.Id') as ids
                                                  FROM dataset.contracts
                                                  WHERE \`ИНН ${supplier ? "поставщика": "заказчика"}\` = ?), '$[*]'
                                                     columns( id int path '$')
                                          ) as jt)
              AND \`Код КПГЗ\` IN (?)
            GROUP BY \`Код КПГЗ\` LIMIT 100;
        `, [inn, groups], function (error, results) {
            if(error) return reject(error);
            resolve(results);
        });
    });
}
function getSupplierInfo(inn) {
    return new Promise((resolve, reject) => {
        connection.query(`
            SELECT \`ИНН поставщика\`, \`Наименование поставщика\`
            FROM dataset.contracts WHERE \`ИНН поставщика\` = ? LIMIT 1;
        `, [inn], function (error, results) {
            if(error) return reject(error);
            resolve({
                inn: results[0]['ИНН поставщика'],
                name: results[0]['Наименование поставщика'],
                type: "supplier"
            });
        });
    });
}
function getCustomerInfo(inn) {
    return new Promise((resolve, reject) => {
        connection.query(`
            SELECT \`ИНН заказчика\`, \`Наименование заказчика\` 
            FROM dataset.contracts WHERE \`ИНН заказчика\` = ? LIMIT 1;
        `, [inn], function (error, results) {
            if(error) return reject(error);
            resolve({
                inn: results[0]['ИНН заказчика'],
                name: results[0]['Наименование заказчика'],
                type: "customer"
            });
        });
    });
}
module.exports = {getMostPopularSeasonedGroups, getItemsFromGroups, getCustomerInfo, getSupplierInfo};