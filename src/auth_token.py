#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
认证token生成模块
提供RSA密钥对生成和访问令牌创建功能
"""

from fastmcp.server.auth import BearerAuthProvider
from fastmcp.server.auth.providers.bearer import RSAKeyPair


def create_auth_components():
    """
    创建认证组件
    
    Returns:
        tuple: (access_token, auth_provider)
    """
    # 生成RSA密钥对
    key_pair = RSAKeyPair.generate()
    
    # 创建访问令牌
    access_token = key_pair.create_token(
        subject="58bf32d9-ef25-484f-bb7d-bfc683e5b3eb",
        issuer="https://fastmcp.example.com",
        audience="data-analysis-mcp",
        scopes=["data:read_tables", "data:read_table_data"]
    )
    
    print(f'Authorization=Bearer {access_token}')

    # 创建认证提供者
    auth = BearerAuthProvider(
        public_key=key_pair.public_key,
        audience="data-analysis-mcp",
    )
    
    return auth