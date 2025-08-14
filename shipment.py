from math import ceil
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy import select
from extensions import db
from models import Shipment

shipment_bp = Blueprint('shipment', __name__, url_prefix='/shipments')

STATUS_CHOICES = ['Pending', 'In-Transit', 'Delivered']
SERVICE_CHOICES = ['Economy', 'Standard', 'Express']
DAILY_KM = {'Economy': 200, 'Standard': 300, 'Express': 450}

def compute_estimated_days(distance_km: int, service_level: str) -> int:
    daily = DAILY_KM.get(service_level, 300)
    return max(1, ceil(max(0, distance_km) / daily))

@shipment_bp.route('/')
@login_required
def list_shipments():
    page = max(1, int(request.args.get('page', 1)))
    per_page = 5

    status = request.args.get('status', '').strip()
    q = request.args.get('q', '').strip()

    stmt = select(Shipment)
    if status in STATUS_CHOICES:
        stmt = stmt.where(Shipment.status == status)
    if q:
        # simple contains search (SQLite `LIKE`)
        stmt = stmt.where(Shipment.name.ilike(f'%{q}%'))

    stmt = stmt.order_by(Shipment.created_at.desc())
    pagination = db.paginate(stmt, page=page, per_page=per_page, error_out=False)

    return render_template('dashboard.html',
                           shipments=pagination.items,
                           page=page,
                           pages=pagination.pages,
                           total=pagination.total,
                           status=status,
                           q=q,
                           STATUS_CHOICES=STATUS_CHOICES)

@shipment_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_shipment():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        status = request.form.get('status', 'Pending')
        is_fragile = bool(request.form.get('is_fragile'))
        distance_km = int(request.form.get('distance_km') or 0)
        service_level = request.form.get('service_level', 'Standard')

        if not name:
            flash('Name is required', 'danger')
            return redirect(url_for('shipment.create_shipment'))
        if status not in STATUS_CHOICES:
            flash('Invalid status', 'danger')
            return redirect(url_for('shipment.create_shipment'))
        if service_level not in SERVICE_CHOICES:
            flash('Invalid service level', 'danger')
            return redirect(url_for('shipment.create_shipment'))

        estimated_days = compute_estimated_days(distance_km, service_level)

        s = Shipment(name=name, status=status, is_fragile=is_fragile,
                     distance_km=distance_km, service_level=service_level,
                     estimated_days=estimated_days)
        db.session.add(s)
        db.session.commit()
        flash('Shipment created', 'success')
        return redirect(url_for('shipment.list_shipments'))
    return render_template('shipment_form.html', shipment=None,
                           STATUS_CHOICES=STATUS_CHOICES,
                           SERVICE_CHOICES=SERVICE_CHOICES)

@shipment_bp.route('/<int:shipment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_shipment(shipment_id):
    s = db.session.get(Shipment, shipment_id)
    if not s:
        flash('Shipment not found', 'danger')
        return redirect(url_for('shipment.list_shipments'))

    if request.method == 'POST':
        s.name = request.form.get('name', '').strip()
        s.status = request.form.get('status', s.status)
        s.is_fragile = bool(request.form.get('is_fragile'))
        s.distance_km = int(request.form.get('distance_km') or 0)
        s.service_level = request.form.get('service_level', s.service_level)
        s.estimated_days = compute_estimated_days(s.distance_km, s.service_level)

        if not s.name:
            flash('Name is required', 'danger')
            return redirect(request.url)
        if s.status not in STATUS_CHOICES:
            flash('Invalid status', 'danger')
            return redirect(request.url)
        if s.service_level not in SERVICE_CHOICES:
            flash('Invalid service level', 'danger')
            return redirect(request.url)

        db.session.commit()
        flash('Shipment updated', 'success')
        return redirect(url_for('shipment.list_shipments'))

    return render_template('shipment_form.html', shipment=s,
                           STATUS_CHOICES=STATUS_CHOICES,
                           SERVICE_CHOICES=SERVICE_CHOICES)

@shipment_bp.route('/<int:shipment_id>/delete', methods=['POST'])
@login_required
def delete_shipment(shipment_id):
    s = db.session.get(Shipment, shipment_id)
    if not s:
        flash('Shipment not found', 'danger')
        return redirect(url_for('shipment.list_shipments'))
    db.session.delete(s)
    db.session.commit()
    flash('Shipment deleted', 'success')
    return redirect(url_for('shipment.list_shipments'))