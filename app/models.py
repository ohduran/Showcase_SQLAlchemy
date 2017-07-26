"""Database Model."""
from app import db


reports_loans = db.Table('reports_loans',
                                                  db.Column('report_id',
                                                                         db.Integer,
                                                                         db.ForeignKey('report.id')),
                                                  db.Column('loan_id',
                                                                         db.Integer,
                                                                         db.ForeignKey('loan.id')))


class User (db.Model):
    """User table."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, unique=True)
    reports = db.relationship('Report', backref='author', lazy='dynamic')
    loans = db.relationship('Loan', backref='debtor', lazy='dynamic')


class Report(db.Model):
    """Report table."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True, unique=True)
    body = db.Column(db.String(1500), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    loans = db.relationship('Loan',
                                                  secondary=reports_loans,
                                                  primaryjoin=(reports_loans.c.report_id == id),
                                                  backref=db.backref('loans', lazy='dynamic'),
                                                  lazy='dynamic')

    def is_assigned(self, loan):
        """Is this report assigned to this loan."""
        return self.loans.filter(reports_loans.c.loan_id == loan.id).count() > 0

    def assign(self, loan):
        """Assign the report to the loan."""
        if not self.is_assigned(loan):
            self.loans.append(loan)
            return self

    def unassign(self, loan):
        """Unassign the report to the loan."""
        if self.is_assigned(loan):
            self.loans.remove(loan)
            return self

    def sum_of_loans(self):
        """Sum all loan balances within the report."""
        # What if currencies are not the same?
        values = [loan.balance for loan in self.loans]
        return reduce((lambda x, y: x + y), values)


class Loan(db.Model):
    """Loan table."""

    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer)
    currency = db.Column(db.String(3))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reports = db.relationship('Report',
                                                      secondary=reports_loans,
                                                      primaryjoin=(reports_loans.c.loan_id == id),
                                                      backref=db.backref('reports', lazy='dynamic'),
                                                      lazy='dynamic')

    def is_referred(self, report):
        """Is this loan reported by this report."""
        return self.reports.filter(reports_loans.c.report_id == report.id).count() > 0

    def refer(self, report):
        """Refer this loan to the report."""
        if not self.is_referred(report):
            self.reports.append(report)
            return self

    def unrefer(self, report):
        """Unrefer this loan from the report."""
        if self.is_referred(report):
            self.reports.remove(report)
            return self
