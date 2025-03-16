# tests/user_dao_test.py
import unittest
from datetime import datetime
from app.database import Base, get_session, engine
from trigger.dao.po import User
from app.logger import log

class TestUserCRUD(unittest.TestCase):
    def setUp(self):
        self.engine = engine
        Base.metadata.create_all(self.engine)
        self.session = get_session()

    def tearDown(self):
        self.session.close()
        # Base.metadata.drop_all(self.engine)

    def test_create_user(self):
        # 创建测试数据
        test_user = User(
            username="test_user",
            password_hash="hashed_password",
        )

        # 执行插入操作
        self.session.add(test_user)
        self.session.commit()

        # 验证结果
        db_user = self.session.query(User).filter_by(username="test_user").first()
        log.info(db_user)
        self.assertIsNotNone(db_user)
        self.assertEqual(db_user.role, "user")

    def test_read_user(self):
        # 准备测试数据
        test_user = User(username="reader", password_hash="secret")
        self.session.add(test_user)
        self.session.commit()

        # 执行查询
        result = self.session.query(User).filter_by(username="reader").one()
        log.info(result)
        # 验证字段
        self.assertEqual(result.password_hash, "secret")
        self.assertTrue(isinstance(result.created_time, datetime))  # 验证时间类型[3](@ref)

    def test_update_user(self):
        # 初始化数据
        user = User(username="old_name", password_hash="old_pwd")
        self.session.add(user)
        self.session.commit()

        # 执行更新
        user.username = "new_name"
        self.session.commit()

        # 验证变更
        updated = self.session.query(User).get(user.id)
        self.assertEqual(updated.username, "new_name")

    def test_delete_user(self):
        user = User(username="to_delete", password_hash="temp")
        self.session.add(user)
        self.session.commit()

        # 执行删除
        self.session.delete(user)
        self.session.commit()

        # 验证删除
        deleted = self.session.query(User).get(user.id)
        self.assertIsNone(deleted)

if __name__ == '__main__':
    unittest.main()