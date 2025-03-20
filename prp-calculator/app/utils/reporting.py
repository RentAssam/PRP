from weasyprint import HTML
from flask import render_template, current_app
from datetime import datetime
import tempfile
import os

def generate_pdf_report(calculation):
    """Generate a professional PDF report for a PRP calculation"""
    try:
        # Extract calculation data
        inputs = calculation.inputs
        result = calculation.result
        created_at = calculation.created_at.strftime("%d %b %Y %H:%M")
        
        # Calculate additional financial metrics
        tax_deduction = result * 0.3  # Assuming 30% tax
        net_amount = result - tax_deduction
        retirement_10yr = result * (1.05 ** 10)  # 5% annual growth
        
        # Create context for template
        context = {
            'calculation_date': created_at,
            'basic_pay': f"₹{inputs['basic']:,.2f}",
            'da': f"₹{inputs['da']:,.2f}",
            'company_rating': inputs['company_rating'],
            'individual_rating': inputs['individual_rating'],
            'employee_type': inputs['employee_type'],
            'gross_prp': f"₹{result:,.2f}",
            'tax_deduction': f"₹{tax_deduction:,.2f}",
            'net_amount': f"₹{net_amount:,.2f}",
            'retirement_projection': f"₹{retirement_10yr:,.2f}",
            'report_date': datetime.now().strftime("%d %b %Y"),
            'report_id': f"PRP-{calculation.id:05d}"
        }

        # Render HTML template
        html_string = render_template(
            'report.html',
            **context,
            logo_path=os.path.join(current_app.static_folder, 'images/logo.png')
        )
        
        # Generate PDF
        html = HTML(string=html_string)
        pdf_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        
        html.write_pdf(pdf_file.name, 
                      stylesheets=[os.path.join(current_app.static_folder, 'css/report.css')])
        
        return pdf_file.name

    except Exception as e:
        current_app.logger.error(f"Report generation failed: {str(e)}")
        raise