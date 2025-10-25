const sqlite3 = require('sqlite3').verbose();
const path = require('path');
const fs = require('fs');

class Database {
    constructor() {
        this.db = null;
        this.dbPath = path.join(__dirname, 'taobei.db');
    }

    // 初始化数据库连接
    async init() {
        return new Promise((resolve, reject) => {
            this.db = new sqlite3.Database(this.dbPath, (err) => {
                if (err) {
                    console.error('数据库连接失败:', err.message);
                    reject(err);
                } else {
                    console.log('数据库连接成功');
                    this.createTables().then(resolve).catch(reject);
                }
            });
        });
    }

    // 创建数据表
    async createTables() {
        return new Promise((resolve, reject) => {
            console.log('正在初始化数据库...');
            
            // 读取SQL文件
            const sqlFile = path.join(__dirname, 'init.sql');
            const sqlContent = fs.readFileSync(sqlFile, 'utf8');
            
            // 简单的SQL语句分割，保留所有非注释内容
            const statements = [];
            const lines = sqlContent.split('\n');
            let currentStatement = '';
            
            for (let i = 0; i < lines.length; i++) {
                const line = lines[i];
                const trimmedLine = line.trim();
                
                // 跳过空行和注释行
                if (trimmedLine === '' || trimmedLine.startsWith('--')) {
                    continue;
                }
                
                currentStatement += line + '\n';
                
                // 如果行以分号结尾，表示语句结束
                if (trimmedLine.endsWith(';')) {
                    const stmt = currentStatement.trim().replace(/;$/, '');
                    if (stmt.length > 0) {
                        statements.push(stmt);
                    }
                    currentStatement = '';
                }
            }
            
            // 处理最后一个语句（如果没有分号结尾）
            if (currentStatement.trim().length > 0) {
                const stmt = currentStatement.trim().replace(/;$/, '');
                if (stmt.length > 0) {
                    statements.push(stmt);
                }
            }
            
            console.log('所有SQL语句:');
            statements.forEach((stmt, index) => {
                console.log(`${index + 1}: ${stmt.substring(0, 80)}...`);
            });
            
            // 打印所有语句以调试
            console.log('所有SQL语句:');
            statements.forEach((stmt, index) => {
                console.log(`${index + 1}: ${stmt.substring(0, 100)}...`);
            });
            
            // 按类型分组SQL语句
            const createTableStatements = statements.filter(stmt => {
                const upperStmt = stmt.toUpperCase().trim();
                const isCreateTable = upperStmt.includes('CREATE TABLE');
                console.log(`检查语句: ${stmt.substring(0, 50)}... 是否为CREATE TABLE: ${isCreateTable}`);
                return isCreateTable;
            });
            const createIndexStatements = statements.filter(stmt => {
                const upperStmt = stmt.toUpperCase().trim();
                return upperStmt.includes('CREATE INDEX');
            });
            const insertStatements = statements.filter(stmt => {
                const upperStmt = stmt.toUpperCase().trim();
                return upperStmt.startsWith('INSERT');
            });
            
            console.log(`找到 ${createTableStatements.length} 个CREATE TABLE语句`);
            console.log(`找到 ${createIndexStatements.length} 个CREATE INDEX语句`);
            console.log(`找到 ${insertStatements.length} 个INSERT语句`);
            
            // 按顺序执行：先创建表，再创建索引，最后插入数据
            const orderedStatements = [
                ...createTableStatements,
                ...createIndexStatements,
                ...insertStatements
            ];
            
            this.executeStatementsSequentially(orderedStatements, 0, resolve, reject);
        });
    }
    
    executeStatementsSequentially(statements, index, resolve, reject) {
        if (index >= statements.length) {
            console.log('数据库初始化完成');
            resolve();
            return;
        }
        
        const statement = statements[index];
        console.log(`执行SQL语句 (${index + 1}/${statements.length}): ${statement.substring(0, 50)}...`);
        
        this.db.run(statement, (err) => {
            if (err) {
                console.error(`执行SQL语句失败 (${index + 1}/${statements.length}): ${err.message}`);
                console.error(`SQL语句: ${statement}`);
                reject(err);
                return;
            }
            
            console.log(`SQL语句执行成功 (${index + 1}/${statements.length})`);
            // 递归执行下一个语句
            this.executeStatementsSequentially(statements, index + 1, resolve, reject);
        });
    }

    // 执行查询
    async query(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.all(sql, params, (err, rows) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(rows);
                }
            });
        });
    }

    // 执行单条查询
    async get(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.get(sql, params, (err, row) => {
                if (err) {
                    reject(err);
                } else {
                    resolve(row);
                }
            });
        });
    }

    // 执行插入/更新/删除
    async run(sql, params = []) {
        return new Promise((resolve, reject) => {
            this.db.run(sql, params, function(err) {
                if (err) {
                    reject(err);
                } else {
                    resolve({
                        id: this.lastID,
                        changes: this.changes
                    });
                }
            });
        });
    }

    // 关闭数据库连接
    close() {
        if (this.db) {
            this.db.close((err) => {
                if (err) {
                    console.error('关闭数据库连接失败:', err.message);
                } else {
                    console.log('数据库连接已关闭');
                }
            });
        }
    }
}

// 创建数据库实例
const database = new Database();

module.exports = database;