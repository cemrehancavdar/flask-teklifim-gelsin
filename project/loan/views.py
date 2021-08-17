from flask import Blueprint, make_response, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from project.loan.models import Bank, Loan, Offer, Reason
from project import db
from project.utils import calculate_expiry_date


app_blueprint = Blueprint("app", __name__, url_prefix="/app")


@app_blueprint.post("/loans")
@jwt_required()
def post_loan():
    post_data = request.get_json()
    print(post_data)
    try:
        loan = Loan(
            amount=post_data.get("amount"),
            reason_id=post_data.get("reason"),
            expiry=calculate_expiry_date(post_data.get("expiry")),
            user_id=get_jwt_identity(),
        )
        db.session.add(loan)
        db.session.commit()

        Offer.create_random_offers(loan.id)

        response = {
            "status": "success",
            "message": "Kayıt yapıldı.",
        }

        return make_response(jsonify(response)), 201

    except Exception as e:
        print(e)
        response = {"status": "fail", "message": "Try again"}
        return make_response(jsonify(response)), 500


@app_blueprint.get("/loans")
@jwt_required()
def get_offers():
    current_user_id = get_jwt_identity()
    current_user_loans = []
    try:
        loans = Loan.query.filter(Loan.user.has(id=current_user_id)).all()
        banks = Bank.query.all()
        reasons = Reason.query.all()

        bank_enum = {bank.id: bank.name for bank in banks}
        reason_enum = {reason.id: reason.name for reason in reasons}

        for loan in loans:
            offers = Offer.query.filter_by(loan_id=loan.id).all()
            current_user_offers = []
            reason_name = reason_enum.get(loan.reason_id)
            for offer in offers:

                bank_name = bank_enum.get(offer.bank_id)

                current_user_offers.append(
                    {
                        "id": offer.id,
                        "interest_rate": offer.interest_rate,
                        "bank": bank_name,
                        "status": offer.status,
                        "total_pay_amount": loan.amount
                        + (offer.interest_rate * loan.amount / 100),
                    }
                )

            current_user_loans.append(
                {
                    "id": loan.id,
                    "amount": loan.amount,
                    "reason": reason_name,
                    "expiry": loan.expiry.strftime("%m/%d/%Y"),
                    "offers": current_user_offers,
                }
            )
        response = {
            "status": "success",
            "message": "Kullanıcı  verileri çekildi.",
            "data": current_user_loans,
        }

        return make_response(jsonify(response)), 200

    except Exception as e:
        print(e)
        response = {"status": "fail", "message": "Try again"}
        return make_response(jsonify(response)), 500


@app_blueprint.put("/choose_offer")
@jwt_required()
def put_choose_offer():
    post_data = request.get_json()
    print(post_data)
    try:
        choosen_offer = Offer.query.filter_by(id=post_data.get("offer_id")).first()
        offers = Offer.query.filter_by(loan_id=choosen_offer.loan_id).all()
        for offer in offers:
            if offer.status is None:
                if offer.id == post_data.get("offer_id"):
                    offer.status = True
                else:
                    offer.status = False
            db.session.commit()

        response = {"status": "success", "message": "İçerik güncellendi"}
        return make_response(jsonify(response)), 201

    except Exception as e:
        print(e)
        response = {"status": "fail", "message": "Try again"}
        return make_response(jsonify(response)), 500


@app_blueprint.get("/reasons")
@jwt_required()
def get_reasons():
    try:
        reasons = Reason.query.all()
        data = [{"id": reason.id, "name": reason.name} for reason in reasons]

        response = {"status": "success", "message": "Veri getirildi.", "data": data}
        return make_response(jsonify(response)), 200

    except Exception as e:
        print(e)
        response = {"status": "fail", "message": "Try again"}
        return make_response(jsonify(response)), 500
