from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app import app, db
from models import User, Company, CensusOperation, CensusData, PalmTree
from utils import get_dashboard_summary, get_census_summary, get_monitoring_data
from datetime import datetime, timedelta
import json

@app.route('/')
@login_required
def dashboard():
    """Main dashboard page"""
    summary = get_dashboard_summary()
    census_data = get_census_summary()
    return render_template('dashboard.html', summary=summary, census_data=census_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Username atau password salah', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logout user"""
    logout_user()
    flash('Anda telah berhasil keluar', 'success')
    return redirect(url_for('login'))

@app.route('/monitoring')
@login_required
def monitoring():
    """Monitoring and intelligence page"""
    monitoring_data = get_monitoring_data()
    operations = CensusOperation.query.order_by(CensusOperation.date.desc()).limit(10).all()
    return render_template('monitoring.html', monitoring_data=monitoring_data, operations=operations)

@app.route('/users')
@login_required
def users():
    """User management page (admin only)"""
    if current_user.role != 'admin':
        flash('Akses ditolak. Hanya admin yang dapat mengakses halaman ini.', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/create', methods=['POST'])
@login_required
def create_user():
    """Create new user (admin only)"""
    if current_user.role != 'admin':
        flash('Akses ditolak', 'error')
        return redirect(url_for('dashboard'))
    
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']
    
    if User.query.filter_by(username=username).first():
        flash('Username sudah digunakan', 'error')
        return redirect(url_for('users'))
    
    if User.query.filter_by(email=email).first():
        flash('Email sudah digunakan', 'error')
        return redirect(url_for('users'))
    
    user = User(username=username, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    flash('User berhasil ditambahkan', 'success')
    return redirect(url_for('users'))

@app.route('/users/<int:user_id>/toggle', methods=['POST'])
@login_required
def toggle_user_status(user_id):
    """Toggle user active status (admin only)"""
    if current_user.role != 'admin':
        flash('Akses ditolak', 'error')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'diaktifkan' if user.is_active else 'dinonaktifkan'
    flash(f'User {user.username} berhasil {status}', 'success')
    return redirect(url_for('users'))

@app.route('/settings')
@login_required
def settings():
    """Settings page"""
    return render_template('settings.html')

@app.route('/api/palm-trees')
@login_required
def api_palm_trees():
    """API endpoint for palm tree locations"""
    trees = PalmTree.query.all()
    tree_data = []
    for tree in trees:
        tree_data.append({
            'id': tree.tree_id,
            'lat': tree.latitude,
            'lng': tree.longitude,
            'status': tree.status,
            'productivity': tree.productivity,
            'health_score': tree.health_score,
            'last_census': tree.last_census_date.isoformat() if tree.last_census_date else None
        })
    return jsonify(tree_data)

@app.route('/api/census-summary')
@login_required
def api_census_summary():
    """API endpoint for census summary data"""
    summary = get_census_summary()
    return jsonify(summary)

@app.context_processor
def inject_user():
    """Inject current user into all templates"""
    return dict(current_user=current_user)
