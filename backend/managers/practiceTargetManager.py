from typing import Optional
from redis import Redis
from models.practicetarget import PracticeTarget
from pydantic import ValidationError

class PracticeTargetManager:
    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client
        self.key = "practiceTarget"
    
    def create_practice_target(self, practice_target: PracticeTarget):
        self.redis_client.set(self.key, practice_target.json())

    def initialize_practice_target(self):
        practice_target = PracticeTarget(name="Targetos", xCord=1200, yCord=150, health=100, color='blue')
        self.create_practice_target(practice_target)

    def get_practice_target(self) -> Optional[PracticeTarget]:
        practice_target_data = self.redis_client.get(self.key)
        if practice_target_data:
            return PracticeTarget.parse_raw(practice_target_data)
        return None

    def update_health(self, health: int):
        practice_target = self.get_practice_target()
        if practice_target:
            practice_target.health = health
            self.create_practice_target(practice_target)
        else:
            raise ValidationError(f"Practice target not found")

    def update_x_cord(self, x: int):
        practice_target = self.get_practice_target()
        if practice_target:
            practice_target.xCord = x
            self.create_practice_target(practice_target)
        else:
            raise ValidationError(f"Practice target not found")
        
    def delete_practice_target(self):
        self.redis_client.delete(self.key)
