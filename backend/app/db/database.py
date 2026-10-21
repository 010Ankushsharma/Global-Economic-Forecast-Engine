#!/usr/bin/env python3
"""Database Manager for GEFE - PostgreSQL Connection Management"""

import os
from typing import Optional
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import logging

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Singleton database manager for connection pooling and session management"""
    
    _instance: Optional['DatabaseManager'] = None
    _engine: Optional[async_engine] = None
    _session_factory: Optional[async_sessionmaker] = None
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL', 'postgresql://gefe_user:gefe_pass@postgres/gefe_db')
        self.pool_size = int(os.getenv('DB_POOL_SIZE', '10'))
        self.max_overflow = int(os.getenv('DB_MAX_OVERFLOW', '20'))
        
    @classmethod
    async def get_instance(cls) -> 'DatabaseManager':
        """Get singleton instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    async def initialize(self):
        """Initialize database connection pool"""
        logger.info(f"Initializing database connection to {self.database_url[:50]}...")
        
        self._engine = create_async_engine(
            self.database_url,
            echo=False,
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
            pool_pre_ping=True,
            pool_recycle=1800,
            connect_args={"connect_timeout": 10}
        )
        
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )
        
        logger.info("Database connection pool initialized successfully")
    
    async def close(self):
        """Close database connections"""
        if self._engine:
            await self._engine.dispose()
            logger.info("Database connections closed")
    
    async def get_session(self) -> AsyncSession:
        """Get database session"""
        async with self._session_factory() as session:
            yield session
    
    async def execute_query(self, query: str, params: dict = None):
        """Execute raw SQL query"""
        async with self._engine.begin() as conn:
            result = await conn.execute(query, params or {})
            return result


# Global session dependency
async def get_db():
    """FastAPI dependency for database sessions"""
    db_manager = await DatabaseManager.get_instance()
    async with db_manager.get_session() as session:
        yield session


# Import after definition to avoid circular imports
import sys
sys.path.insert(0, '/mnt/data/global_economic_forecast_engine/backend')
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
