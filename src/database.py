import os
import mysql.connector
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class DatabaseManager:
    """数据库管理类，负责MySQL数据库的连接和查询"""
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME')
        self.connection = None
        
    def connect(self) -> bool:
        """建立数据库连接"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset='utf8mb4'
            )
            
            print("✅ 成功连接到数据库: {}".format(self.database))
            return True
            
        except Exception as e:
            print("❌ 数据库连接失败: {}".format(str(e)))
            return False
    
    def execute_query(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """执行SQL查询并返回字典列表"""
        try:
            if not self.connection:
                print("❌ 数据库未连接")
                return None
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)
            
            # 获取查询结果
            results = cursor.fetchall()
            cursor.close()
            
            if results:
                # 转换数据类型
                converted_results = [self._convert_row_types(row) for row in results]
                print("✅ 查询成功，返回 {} 行数据".format(len(converted_results)))
                return converted_results
            else:
                print("✅ 查询成功，但没有返回数据")
                return []
            
        except Exception as e:
            print("❌ 查询执行失败: {}".format(str(e)))
            return None
    
    def _convert_row_types(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """转换行数据中的特殊类型为JSON可序列化的类型"""
        converted = {}
        for key, value in row.items():
            if value is None:
                converted[key] = None
            elif isinstance(value, (int, float, str, bool)):
                converted[key] = value
            elif hasattr(value, 'isoformat'):  # datetime objects
                converted[key] = value.isoformat()
            elif isinstance(value, bytes):
                converted[key] = value.decode('utf-8', errors='ignore')
            else:
                converted[key] = str(value)
        return converted
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """获取表结构信息"""
        try:
            # 获取表结构
            structure_query = f"DESCRIBE {table_name}"
            structure_data = self.execute_query(structure_query)
            
            # 获取表数据样本
            sample_query = f"SELECT * FROM {table_name} LIMIT 5"
            sample_data = self.execute_query(sample_query)
            
            # 获取表统计信息
            count_query = f"SELECT COUNT(*) as total_rows FROM {table_name}"
            count_data = self.execute_query(count_query)
            
            total_rows = count_data[0]['total_rows'] if count_data and len(count_data) > 0 else 0
            
            return {
                'structure': structure_data,
                'sample_data': sample_data,
                'total_rows': total_rows
            }
            
        except Exception as e:
            print("❌ 获取表信息失败: {}".format(str(e)))
            return {}
    
    def get_all_tables(self) -> List[str]:
        """获取数据库中所有表名"""
        try:
            query = "SHOW TABLES"
            results = self.execute_query(query)
            if results:
                # 提取表名（通常是结果中的第一个字段）
                table_names = [list(row.values())[0] for row in results]
                return table_names
            return []
        except Exception as e:
            print("❌ 获取表列表失败: {}".format(str(e)))
            return []
    
    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("✅ 数据库连接已关闭")
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

# 示例用法
if __name__ == "__main__":
    # 使用上下文管理器
    with DatabaseManager() as db:
        # 获取所有表
        tables = db.get_all_tables()
        print(f"数据库中的表: {tables}")
        
        # 如果有表，获取第一个表的信息
        if tables:
            table_info = db.get_table_info(tables[0])
            print(f"\n表 {tables[0]} 的信息:")
            print(f"总行数: {table_info.get('total_rows', 0)}")
            if 'structure' in table_info:
                print("\n表结构:")
                for row in table_info['structure']:
                    print(row)
            if 'sample_data' in table_info:
                print("\n样本数据:")
                for row in table_info['sample_data']:
                    print(row)