const database = require('./database');

class VerificationCodeDAO {
    // DB-CreateVerificationCode: 在数据库中创建验证码记录
    async createVerificationCode(phoneNumber, code, expiresInSeconds = 60) {
        try {
            // 计算过期时间
            const expiresAt = new Date(Date.now() + expiresInSeconds * 1000).toISOString();
            
            // 先删除该手机号的旧验证码
            await this.deleteExpiredCodes(phoneNumber);
            
            const sql = `
                INSERT INTO verification_codes (phone_number, code, created_at, expires_at, used)
                VALUES (?, ?, CURRENT_TIMESTAMP, ?, FALSE)
            `;
            
            const result = await database.run(sql, [phoneNumber, code, expiresAt]);
            
            return {
                id: result.id,
                phoneNumber,
                code,
                expiresAt,
                used: false
            };
        } catch (error) {
            console.error('创建验证码失败:', error);
            throw error;
        }
    }

    // DB-VerifyCode: 验证手机号对应的验证码是否正确且未过期
    async verifyCode(phoneNumber, code) {
        try {
            const sql = `
                SELECT * FROM verification_codes 
                WHERE phone_number = ? AND code = ? AND used = FALSE
                ORDER BY created_at DESC 
                LIMIT 1
            `;
            
            const record = await database.get(sql, [phoneNumber, code]);
            
            if (!record) {
                return { valid: false, reason: '验证码错误' };
            }

            // 检查是否过期
            const now = new Date();
            const expiresAt = new Date(record.expires_at);
            
            if (now > expiresAt) {
                return { valid: false, reason: '验证码已过期' };
            }

            // 标记验证码为已使用
            await this.markCodeAsUsed(record.id);
            
            return { valid: true, record };
        } catch (error) {
            console.error('验证码验证失败:', error);
            throw error;
        }
    }

    // 标记验证码为已使用
    async markCodeAsUsed(codeId) {
        try {
            const sql = 'UPDATE verification_codes SET used = TRUE WHERE id = ?';
            await database.run(sql, [codeId]);
        } catch (error) {
            console.error('标记验证码为已使用失败:', error);
            throw error;
        }
    }

    // 删除过期的验证码
    async deleteExpiredCodes(phoneNumber = null) {
        try {
            let sql = 'DELETE FROM verification_codes WHERE expires_at < CURRENT_TIMESTAMP';
            const params = [];
            
            if (phoneNumber) {
                sql += ' OR phone_number = ?';
                params.push(phoneNumber);
            }
            
            const result = await database.run(sql, params);
            return result.changes;
        } catch (error) {
            console.error('删除过期验证码失败:', error);
            throw error;
        }
    }

    // 检查手机号是否在限制时间内已发送过验证码
    async checkRateLimit(phoneNumber, limitSeconds = 60) {
        try {
            const limitTime = new Date(Date.now() - limitSeconds * 1000).toISOString();
            
            const sql = `
                SELECT COUNT(*) as count FROM verification_codes 
                WHERE phone_number = ? AND created_at > ?
            `;
            
            const result = await database.get(sql, [phoneNumber, limitTime]);
            return result.count > 0;
        } catch (error) {
            console.error('检查发送频率限制失败:', error);
            throw error;
        }
    }

    // 获取手机号的最新验证码（用于测试）
    async getLatestCode(phoneNumber) {
        try {
            const sql = `
                SELECT * FROM verification_codes 
                WHERE phone_number = ? 
                ORDER BY created_at DESC 
                LIMIT 1
            `;
            
            return await database.get(sql, [phoneNumber]);
        } catch (error) {
            console.error('获取最新验证码失败:', error);
            throw error;
        }
    }

    // 清理所有验证码（用于测试）
    async clearAllCodes() {
        try {
            const sql = 'DELETE FROM verification_codes';
            const result = await database.run(sql);
            return result.changes;
        } catch (error) {
            console.error('清理验证码失败:', error);
            throw error;
        }
    }
}

module.exports = new VerificationCodeDAO();