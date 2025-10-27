const crypto = require('crypto');
const jwt = require('jsonwebtoken');

// 生成6位数字验证码
function generateVerificationCode() {
    return Math.floor(100000 + Math.random() * 900000).toString();
}

// 验证手机号格式
function validatePhoneNumber(phone) {
    const phoneRegex = /^1[3-9]\d{9}$/;
    return phoneRegex.test(phone);
}

// 生成JWT令牌
function generateToken(user) {
    const payload = {
        id: user.id,
        phone: user.phone,
        username: user.username
    };
    
    return jwt.sign(payload, process.env.JWT_SECRET || 'taobei-secret-key', {
        expiresIn: '24h'
    });
}

// 验证JWT令牌中间件
function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    const token = authHeader && authHeader.split(' ')[1];

    if (!token) {
        return res.status(401).json({ error: '访问令牌缺失' });
    }

    jwt.verify(token, process.env.JWT_SECRET || 'taobei-secret-key', (err, user) => {
        if (err) {
            return res.status(403).json({ error: '访问令牌无效' });
        }
        req.user = user;
        next();
    });
}

// 生成随机盐值
function generateSalt() {
    return crypto.randomBytes(16).toString('hex');
}

// 哈希密码
function hashPassword(password, salt) {
    return crypto.pbkdf2Sync(password, salt, 10000, 64, 'sha512').toString('hex');
}

// 验证密码
function verifyPassword(password, hash, salt) {
    const hashVerify = crypto.pbkdf2Sync(password, salt, 10000, 64, 'sha512').toString('hex');
    return hash === hashVerify;
}

module.exports = {
    generateVerificationCode,
    validatePhoneNumber,
    generateToken,
    authenticateToken,
    generateSalt,
    hashPassword,
    verifyPassword
};