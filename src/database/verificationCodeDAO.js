const db = require('./database');

class VerificationCodeDAO {
    // 保存验证码
    async saveVerificationCode(phone, code, expiresAt) {
        const sql = `
            INSERT OR REPLACE INTO verification_codes (phone, code, expires_at, created_at)
            VALUES (?, ?, ?, datetime('now'))
        `;
        
        try {
            const result = await new Promise((resolve, reject) => {
                db.run(sql, [phone, code, expiresAt], function(err) {
                    if (err) {
                        reject(err);
                    } else {
                        resolve({ id: this.lastID, changes: this.changes });
                    }
                });
            });
            
            console.log(`验证码保存成功 - 手机号: ${phone}, 验证码: ${code}`);
            return result;
        } catch (error) {
            console.error('保存验证码失败:', error);
            throw error;
        }
    }

    // 验证验证码
    async verifyCode(phone, code) {
        const sql = `
            SELECT * FROM verification_codes 
            WHERE phone = ? AND code = ? AND expires_at > datetime('now')
            ORDER BY created_at DESC 
            LIMIT 1
        `;
        
        try {
            const result = await new Promise((resolve, reject) => {
                db.get(sql, [phone, code], (err, row) => {
                    if (err) {
                        reject(err);
                    } else {
                        resolve(row);
                    }
                });
            });
            
            if (result) {
                // 验证成功后删除验证码
                await this.deleteVerificationCode(phone, code);
                console.log(`验证码验证成功 - 手机号: ${phone}`);
                return true;
            } else {
                console.log(`验证码验证失败 - 手机号: ${phone}, 验证码: ${code}`);
                return false;
            }
        } catch (error) {
            console.error('验证验证码失败:', error);
            throw error;
        }
    }

    // 删除验证码
    async deleteVerificationCode(phone, code) {
        const sql = `DELETE FROM verification_codes WHERE phone = ? AND code = ?`;
        
        try {
            await new Promise((resolve, reject) => {
                db.run(sql, [phone, code], function(err) {
                    if (err) {
                        reject(err);
                    } else {
                        resolve({ changes: this.changes });
                    }
                });
            });
        } catch (error) {
            console.error('删除验证码失败:', error);
            throw error;
        }
    }

    // 清理过期验证码
    async cleanExpiredCodes() {
        const sql = `DELETE FROM verification_codes WHERE expires_at <= datetime('now')`;
        
        try {
            const result = await new Promise((resolve, reject) => {
                db.run(sql, [], function(err) {
                    if (err) {
                        reject(err);
                    } else {
                        resolve({ changes: this.changes });
                    }
                });
            });
            
            if (result.changes > 0) {
                console.log(`清理了 ${result.changes} 个过期验证码`);
            }
            
            return result;
        } catch (error) {
            console.error('清理过期验证码失败:', error);
            throw error;
        }
    }
}

module.exports = new VerificationCodeDAO();