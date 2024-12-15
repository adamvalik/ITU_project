# File: missileManager.py
# Description: Class which interacts with Redis to manage the missiles
# Author: Samuel Hejnicek (xhejni00)


from typing import Optional
from redis import Redis
from models.missile import Missile
from pydantic import ValidationError

class MissileManager:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client
        self.key_prefix = "missile"
    
    def create_missile(self, missile: Missile):
        missile_key = f"{self.key_prefix}{missile.id}"
        self.redis_client.set(missile_key, missile.json())

    def initialize_missile(self):
        small_missile = Missile(id=0, name="SMALL MISSILE", damage=20, radius=30, price=0, picture="assets/small_missile_icon.png")
        medium_missile = Missile(id=1, name="MEDIUM MISSILE", damage=30, radius=40, price=100, picture="assets/medium_missile_icon.png")
        big_missile = Missile(id=2, name="BIG MISSILE", damage=40, radius=50, price=200, picture="assets/big_missile_icon.png")

        self.create_missile(small_missile)
        self.create_missile(medium_missile)
        self.create_missile(big_missile)

    def get_missile(self, missile_id: int) -> Optional[Missile]:
        missile_key = f"{self.key_prefix}{missile_id}"
        missile_data = self.redis_client.get(missile_key)
        if missile_data:
            return Missile.parse_raw(missile_data)
        return None

    def get_missiles(self) -> list[Missile]:
        missiles = []
        for missile_id in range(0, 3):
            missile = self.get_missile(missile_id)
            if missile:
                missiles.append(missile)
        return missiles
    
    def delete_missile(self, missile_id: int):
        missile_key = f"{self.key_prefix}{missile_id}"
        self.redis_client.delete(missile_key)