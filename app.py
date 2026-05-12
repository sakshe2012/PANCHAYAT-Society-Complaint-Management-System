import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Complaint

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)

# --- Categorization Logic ---
def categorize_complaint(text):
    text = text.lower()
    if any(word in text for word in ['water', 'leakage', 'plumb', 'pipe', 'tap']):
        return 'Water Issue'
    if any(word in text for word in ['light', 'electric', 'power', 'wire', 'bulb']):
        return 'Electrical Issue'
    if any(word in text for word in ['security', 'guard', 'theft', 'stranger', 'safe']):
        return 'Security Issue'
    if any(word in text for word in ['clean', 'garbage', 'trash', 'waste', 'sweep', 'dust']):
        return 'Cleaning & Hygiene'
    if any(word in text for word in ['road', 'pothole', 'street', 'park', 'lift', 'elevator']):
        return 'Infrastructure'
    return 'Other'

from sqlalchemy.exc import IntegrityError

# --- Context Processors ---
@app.context_processor
def inject_user():
    user = None
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
    return dict(current_user=user)

# --- Routes ---

@app.route('/')
def index():
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user:
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('user_dashboard'))
        else:
            # If user is in session but not in database (e.g., switched databases)
            session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        role = request.form.get('role', 'user') # For testing, we allow selecting role. In prod, admin should be restricted.
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_pw, role=role)
        db.session.add(new_user)
        
        try:
            db.session.commit()
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        
        user = db.session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash(f'Welcome back, {user.username}!', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/user/dashboard')
def user_dashboard():
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))
    
    complaints = Complaint.query.filter_by(user_id=session['user_id']).order_by(Complaint.created_at.desc()).all()
    return render_template('user_dashboard.html', complaints=complaints)

@app.route('/user/submit_complaint', methods=['GET', 'POST'])
def submit_complaint():
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        
        category = categorize_complaint(description)
        
        new_complaint = Complaint(
            user_id=session['user_id'],
            title=title,
            description=description,
            category=category,
            location=location
        )
        db.session.add(new_complaint)
        db.session.commit()
        
        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('user_dashboard'))
        
    return render_template('submit_complaint.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    category_filter = request.args.get('category')
    status_filter = request.args.get('status')
    
    query = Complaint.query
    if category_filter:
        query = query.filter_by(category=category_filter)
    if status_filter:
        query = query.filter_by(status=status_filter)
        
    complaints = query.order_by(Complaint.created_at.desc()).all()
    
    # Get distinct categories and statuses for filters
    categories = db.session.query(Complaint.category).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template('admin_dashboard.html', complaints=complaints, categories=categories, current_cat=category_filter, current_status=status_filter)

@app.route('/admin/update_status/<int:id>', methods=['POST'])
def update_status(id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    complaint = Complaint.query.get_or_404(id)
    new_status = request.form.get('status')
    
    if new_status in ['Pending', 'In Progress', 'Resolved']:
        complaint.status = new_status
        db.session.commit()
        flash(f'Status updated for {complaint.title}', 'success')
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete/<int:id>', methods=['POST'])
def delete_complaint(id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    complaint = Complaint.query.get_or_404(id)
    db.session.delete(complaint)
    db.session.commit()
    flash('Complaint deleted.', 'success')
    
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
