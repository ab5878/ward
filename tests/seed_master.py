#!/usr/bin/env python3
"""
Master Data Seeder
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from master_data_service import MasterDataService
import os

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "test_database"

async def seed():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    service = MasterDataService(db)
    await service.seed_master_data()
    client.close()

if __name__ == "__main__":
    asyncio.run(seed())
