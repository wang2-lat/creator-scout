import sqlite3
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str = "creator_scout.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS creators (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                platform TEXT NOT NULL,
                niche TEXT NOT NULL,
                followers INTEGER NOT NULL,
                engagement_rate REAL NOT NULL,
                contact TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS partnerships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                creator_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                budget REAL DEFAULT 0,
                revenue REAL DEFAULT 0,
                roi REAL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (creator_id) REFERENCES creators (id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_creator(self, creator) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO creators (name, platform, niche, followers, engagement_rate, contact) VALUES (?, ?, ?, ?, ?, ?)",
            (creator.name, creator.platform, creator.niche, creator.followers, creator.engagement_rate, creator.contact)
        )
        creator_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return creator_id
    
    def get_creator(self, creator_id: int) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM creators WHERE id = ?", (creator_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    def get_all_creators(self) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM creators ORDER BY followers DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def search_creators(self, platform: Optional[str], niche: Optional[str], 
                       min_followers: Optional[int], max_followers: Optional[int]) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM creators WHERE 1=1"
        params = []
        
        if platform:
            query += " AND platform = ?"
            params.append(platform)
        if niche:
            query += " AND niche LIKE ?"
            params.append(f"%{niche}%")
        if min_followers:
            query += " AND followers >= ?"
            params.append(min_followers)
        if max_followers:
            query += " AND followers <= ?"
            params.append(max_followers)
        
        query += " ORDER BY engagement_rate DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def add_partnership(self, partnership) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO partnerships (creator_id, status, budget, notes) VALUES (?, ?, ?, ?)",
            (partnership.creator_id, partnership.status, partnership.budget, partnership.notes)
        )
        partnership_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return partnership_id
    
    def get_partnerships(self, creator_id: Optional[int] = None) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = """
            SELECT p.*, c.name as creator_name 
            FROM partnerships p 
            JOIN creators c ON p.creator_id = c.id
        """
        
        if creator_id:
            query += " WHERE p.creator_id = ?"
            cursor.execute(query, (creator_id,))
        else:
            cursor.execute(query)
        
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def update_partnership_roi(self, partnership_id: int, revenue: float):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT budget FROM partnerships WHERE id = ?", (partnership_id,))
        row = cursor.fetchone()
        
        if row and row[0] > 0:
            roi = ((revenue - row[0]) / row[0]) * 100
            cursor.execute(
                "UPDATE partnerships SET revenue = ?, roi = ? WHERE id = ?",
                (revenue, roi, partnership_id)
            )
        
        conn.commit()
        conn.close()
