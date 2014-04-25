from sqlalchemy import Column, Integer, String, BigInteger
from db import Base

class TeamScore(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True)
    score = Column(BigInteger)
    teamName = Column(Integer)

    def __init__ (self, team, score):
        self.teamName = team
        self.score = score

    def __repr__ (self):
        return '<%s : %d>' % (self.teamName, self.score)
