const database = require('./database');
const userDAO = require('./userDAO');
const verificationCodeDAO = require('./verificationCodeDAO');
const productDAO = require('./productDAO');
const cartDAO = require('./cartDAO');
const orderDAO = require('./orderDAO');

// 初始化数据库
async function initDatabase() {
    try {
        await database.init();
        console.log('数据库初始化完成');
        return true;
    } catch (error) {
        console.error('数据库初始化失败:', error);
        throw error;
    }
}

// 关闭数据库连接
function closeDatabase() {
    database.close();
}

module.exports = {
    database,
    userDAO,
    verificationCodeDAO,
    productDAO,
    cartDAO,
    orderDAO,
    initDatabase,
    closeDatabase
};