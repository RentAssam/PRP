from flask import render_template, request, jsonify, send_file
from app import app, db
from app.models import Calculation
from app.forms import PRPForm
from app.utils.calculations import (
    calculate_prp,
    tax_impact,
    retirement_projections
)
from app.utils.reporting import generate_pdf_report
import json

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PRPForm()
    if form.validate_on_submit():
        # Calculation logic
        result = calculate_prp(
            form.basic.data,
            form.da.data,
            form.company_rating.data,
            form.individual_rating.data,
            form.employee_type.data,
            form.profit_met.data
        )
        
        # Save to database
        calc = Calculation(
            user_id=1,  # Replace with actual user ID
            inputs=json.dumps(form.data),
            result=result
        )
        db.session.add(calc)
        db.session.commit()

        return render_template('result.html', 
                            result=result,
                            form_data=form.data)
    
    return render_template('index.html', form=form)

@app.route('/api/compare', methods=['POST'])
def compare_scenarios():
    data = request.get_json()
    results = []
    for scenario in data:
        result = calculate_prp(**scenario)
        results.append(result)
    return jsonify(results)

@app.route('/report/<int:id>')
def download_report(id):
    calculation = Calculation.query.get_or_404(id)
    pdf = generate_pdf_report(calculation)
    return send_file(pdf, as_attachment=True, download_name="prp_report.pdf")