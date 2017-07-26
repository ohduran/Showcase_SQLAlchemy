"""Test cases."""
#!environment/bin/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Report, Loan


class TestCase(unittest.TestCase):
    """Test cases."""

    def setUp(self):
        """Set up the test database."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """End the tests by removing the database."""
        db.session.remove()
        db.drop_all()

    def test_add_user_loan_report(self):
        """Test that the test worked."""
        u = User(name="Uu")
        v = User(name="Vv")
        l = Loan(balance=10, currency='GBP', debtor=u)
        r = Report(title="The Report", body="This is the body of the report", author=v)
        db.session.add(u)
        db.session.add(v)
        db.session.add(r)
        db.session.add(l)
        db.session.commit()
        return u, v, l, r

    def test_assign_loan_to_a_report(self):
        """Assign loan to a report."""
        u, v, l, r = self.test_add_user_loan_report()
        # check that whatever is coming from test_add is correct
        self.assertTrue(u.name == "Uu")

        # Assignment
        self.assertFalse(r.is_assigned(l))
        r.assign(l)
        self.assertTrue(r.loans.count() == 1)
        self.assertTrue(r.is_assigned(l))

        # Unassignment
        r.unassign(l)
        self.assertTrue(r.loans.count() == 0)
        self.assertFalse(r.is_assigned(l))

    def test_refer_report_to_a_loan(self):
        """Refer a report to a loan."""
        u, v, l, r = self.test_add_user_loan_report()
        # check that whatever is coming from test_add is correct
        self.assertTrue(u.name == "Uu")

        # Referral
        self.assertFalse(l.is_referred(l))
        l.refer(r)
        self.assertTrue(l.reports.count() == 1)
        self.assertTrue(l.is_referred(r))

        # Unreferral
        l.unrefer(r)
        self.assertTrue(l.reports.count() == 0)
        self.assertFalse(l.is_referred(r))


class TestFinders(TestCase):
    """Find all reports that a loan belongs to."""

    def test_find_reports(self):
        """Test that the reports that a loan belongs to are found correctly."""
        u, v, l, r = self.test_add_user_loan_report()

        # Create reports, and assign them to loan l2 except the fifth one
        l2 = Loan(balance=100, currency='USD', debtor=u)
        db.session.add(l2)
        rep = []
        for i in range(5):
            rep.append(Report(title="report" + str(i), body="This is the body of the report", author=v))
            db.session.add(rep[i])
        db.session.commit()
        for i in range(4):
            l2.refer(rep[i])

        # Check that all but the fifth are referring l2
        for i in range(5):
            if i != 4:
                self.assertTrue(l2.is_referred(rep[i]))
            else:
                self.assertFalse(l2.is_referred(rep[i]))

        # Check that the rep list is NOT l2.reports
        self.assertFalse(l2.reports == rep)
        # Check that the first 4 items in rep are in the list of l2.reports
        for i in range(len(rep[:4])):
            self.assertTrue(rep[i] in l2.reports)


class TestSum(TestCase):
    """Test sum of values in model."""

    def test_sum_of_loan_balances(self):
        """Test is self-explanatory."""
        u, v, l, r = self.test_add_user_loan_report()
        l2 = Loan(balance=100, currency='GBP', debtor=u)
        db.session.add(l2)
        db.session.commit()

        r.assign(l)
        r.assign(l2)

        amount = l.balance + l2.balance
        self.assertTrue(amount == r.sum_of_loans())


if __name__ == '__main__':
    unittest.main()
