from datetime import datetime
from models import db
import json

class Assessment(db.Model):
    __tablename__ = 'assessments'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed
    score_network = db.Column(db.Float, default=0.0)
    score_credentials = db.Column(db.Float, default=0.0)
    score_malware = db.Column(db.Float, default=0.0)
    score_backup = db.Column(db.Float, default=0.0)
    score_compliance = db.Column(db.Float, default=0.0)
    total_score = db.Column(db.Float, default=0.0)
    responses_data = db.Column(db.Text)  # JSON com todas as respostas
    
    # Relacionamentos
    recommendations = db.relationship('Recommendation', backref='assessment', lazy=True)
    
    def set_responses(self, responses_dict):
        self.responses_data = json.dumps(responses_dict)
        
    def get_responses(self):
        return json.loads(self.responses_data) if self.responses_data else {}
    
    def calculate_scores(self):
        responses = self.get_responses()
        
        # Calcula pontuações para cada categoria
        self.score_network = self._calculate_category_score(responses, 'network')
        self.score_credentials = self._calculate_category_score(responses, 'credentials')
        self.score_malware = self._calculate_category_score(responses, 'malware')
        self.score_backup = self._calculate_category_score(responses, 'backup')
        self.score_compliance = self._calculate_category_score(responses, 'compliance')
        
        # Calcula pontuação total (média das categorias)
        self.total_score = (
            self.score_network + 
            self.score_credentials + 
            self.score_malware + 
            self.score_backup + 
            self.score_compliance
        ) / 5.0
        
    def _calculate_category_score(self, responses, category):
        category_questions = [q for q in responses.keys() if q.startswith(f"{category}_")]
        if not category_questions:
            return 0.0
            
        total_points = 0
        max_points = len(category_questions) * 5  # Assumindo escala de 0-5 por questão
        
        for question in category_questions:
            total_points += float(responses[question])
            
        return (total_points / max_points) * 100 if max_points > 0 else 0
        
    def __repr__(self):
        return f''
