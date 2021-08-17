from project import db
from project.utils import calculate_random_float


class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float(), nullable=False)
    reason_id = db.Column(db.Integer(), db.ForeignKey("reasons.id"))
    reason = db.relationship("Reason")
    expiry = db.Column(db.Date())
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    user = db.relationship("User")


class Bank(db.Model):
    __tablename__ = "banks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)


class Offer(db.Model):
    __tablename__ = "offers"
    id = db.Column(db.Integer, primary_key=True)
    interest_rate = db.Column(db.Float(), nullable=False)
    bank_id = db.Column(db.Integer(), db.ForeignKey("banks.id"))
    bank = db.relationship("Bank")
    loan_id = db.Column(db.Integer(), db.ForeignKey("loans.id"))
    loan = db.relationship("Loan")
    status = db.Column(db.Boolean())

    @staticmethod
    def create_random_offers(loan_id):
        banks = Bank.query.all()

        for bank in banks:
            offer = Offer(
                interest_rate=calculate_random_float(),
                bank_id=bank.id,
                loan_id=loan_id,
            )
            db.session.add(offer)
            db.session.commit()


class Reason(db.Model):
    __tablename__ = "reasons"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
