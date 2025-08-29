from datetime import datetime, timedelta
from models import Company, CensusData, CensusOperation, PalmTree
from app import db
import random

def get_dashboard_summary():
    """Get dashboard summary data"""
    # Get company info (assuming single company for now)
    company = Company.query.first()
    if not company:
        # Create default company if none exists
        company = Company(
            name="PT Sawit Mandiri",
            area_hectares=1250.5,
            location="Cikijang, Sukabumi, Jawa Barat"
        )
        db.session.add(company)
        db.session.commit()
    
    # Get latest census data
    latest_census = CensusData.query.order_by(CensusData.created_at.desc()).first()
    
    # Calculate totals from all census operations
    total_trees = PalmTree.query.count()
    productive_trees = PalmTree.query.filter_by(productivity='productive').count()
    unproductive_trees = total_trees - productive_trees
    
    return {
        'company': company,
        'total_trees': total_trees,
        'productive_trees': productive_trees,
        'unproductive_trees': unproductive_trees,
        'latest_census': latest_census
    }

def get_census_summary():
    """Get census activity summary"""
    # Get latest census data aggregated
    latest_operations = CensusOperation.query.order_by(CensusOperation.date.desc()).limit(5).all()
    
    # Aggregate census data from recent operations
    total_data = {
        'male_flower': 0,
        'female_flower': 0,
        'purse_flower': 0,
        'red_fruit': 0,
        'black_fruit': 0,
        'land_area_census': 0.0,
        'operations_count': len(latest_operations)
    }
    
    for operation in latest_operations:
        census_data = CensusData.query.filter_by(operation_id=operation.operation_id).first()
        if census_data:
            total_data['male_flower'] += census_data.male_flower
            total_data['female_flower'] += census_data.female_flower
            total_data['purse_flower'] += census_data.purse_flower
            total_data['red_fruit'] += census_data.red_fruit
            total_data['black_fruit'] += census_data.black_fruit
            total_data['land_area_census'] += census_data.land_area_census
    
    return total_data

def get_monitoring_data():
    """Get monitoring and intelligence data"""
    # Calculate predictions based on current census data
    census_summary = get_census_summary()
    
    # Simple prediction algorithm (in real implementation, this would be AI-based)
    predicted_red_fruit = int(census_summary['red_fruit'] * 1.15)  # 15% growth prediction
    predicted_black_fruit = int(census_summary['black_fruit'] * 1.08)  # 8% growth prediction
    
    # Health monitoring data
    total_trees = PalmTree.query.count()
    healthy_trees = PalmTree.query.filter(PalmTree.health_score >= 0.7).count()
    warning_trees = PalmTree.query.filter(
        PalmTree.health_score >= 0.4, 
        PalmTree.health_score < 0.7
    ).count()
    critical_trees = PalmTree.query.filter(PalmTree.health_score < 0.4).count()
    
    return {
        'predictions': {
            'red_fruit': predicted_red_fruit,
            'black_fruit': predicted_black_fruit,
            'total_fruit': predicted_red_fruit + predicted_black_fruit,
            'confidence': 0.87  # Mock confidence score
        },
        'health_status': {
            'total_trees': total_trees,
            'healthy': healthy_trees,
            'warning': warning_trees,
            'critical': critical_trees
        },
        'recommendations': [
            "Lakukan pemupukan pada area dengan skor kesehatan rendah",
            "Tingkatkan frekuensi monitoring pada pohon dengan status warning", 
            "Pertimbangkan penggantian pohon dengan produktivitas rendah",
            "Optimalisasi jadwal panen berdasarkan prediksi buah matang"
        ]
    }

def create_sample_data():
    """Create sample data for testing (call this from init_db.py)"""
    # Create sample company
    if not Company.query.first():
        company = Company(
            name="PT Sawit Mandiri",
            area_hectares=1250.5,
            location="Cikijang, Sukabumi, Jawa Barat",
            established_date=datetime(2010, 1, 1).date()
        )
        db.session.add(company)
    
    # Create sample palm trees
    if PalmTree.query.count() == 0:
        # Sample coordinates around Cikijang, Sukabumi area
        base_lat, base_lng = -6.8447, 106.9317
        
        for i in range(100):
            tree = PalmTree(
                tree_id=f"TREE-{1000 + i}",
                latitude=base_lat + random.uniform(-0.1, 0.1),
                longitude=base_lng + random.uniform(-0.1, 0.1),
                status=random.choice(['active', 'active', 'active', 'inactive']),
                productivity=random.choice(['productive', 'productive', 'unproductive']),
                health_score=random.uniform(0.3, 1.0),
                last_census_date=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            db.session.add(tree)
    
    # Create sample census operations
    if CensusOperation.query.count() == 0:
        operations = []
        for i in range(10):
            operation = CensusOperation(
                operation_id=f"OP-{datetime.now().strftime('%Y%m%d')}-{100 + i}",
                date=datetime.now() - timedelta(days=i),
                entity=f"Blok {chr(65 + i)}",
                census_type="oil palm flower & fruit",
                hectare_covered=random.uniform(10, 50),
                prediction_result=f"Prediksi hasil: {random.randint(80, 120)} ton",
                action_recommendation="Lanjutkan monitoring rutin"
            )
            db.session.add(operation)
            operations.append(operation)
        
        # Commit operations first
        db.session.commit()
        
        # Then create corresponding census data
        for operation in operations:
            census_data = CensusData(
                operation_id=operation.operation_id,
                male_flower=random.randint(50, 200),
                female_flower=random.randint(30, 150),
                purse_flower=random.randint(20, 100),
                red_fruit=random.randint(100, 300),
                black_fruit=random.randint(80, 250),
                total_palm_trees=random.randint(200, 500),
                productive_trees=random.randint(150, 400),
                unproductive_trees=random.randint(20, 100),
                land_area_census=random.uniform(10, 50)
            )
            db.session.add(census_data)
    
    db.session.commit()
