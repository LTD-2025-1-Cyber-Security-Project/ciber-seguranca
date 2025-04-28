from datetime import datetime
from models import db

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # network, credentials, malware, backup, compliance
    priority = db.Column(db.String(20), nullable=False)  # high, medium, low
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    implementation_steps = db.Column(db.Text, nullable=True)
    resources = db.Column(db.Text, nullable=True)  # Links e recursos úteis
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, implemented
    
    def __repr__(self):
        return f''
