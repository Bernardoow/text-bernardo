from flask import request
from flask_restplus import Resource, Api, fields
from marshmallow.exceptions import ValidationError
from app.api_v1.schemas import (
    FrequenceDistributionSchema,
    Gram2VocabularySchema,
    IsolatedVocabularySchema,
    SendTextSchema,
)
from app.models import Text
from app.extensions import db
from app.text_handler.text_handler import TextHandler
from . import api_bp_v1

api_restfull = Api(api_bp_v1, title="Text Handler Web APP", description="Text Handler Web APP")

SEND_TEXT_API_FIELD_INCOME = api_restfull.model("SendTextAPIIncomeField", {"text": fields.String})
SEND_TEXT_API_FIELD_OUTCOME = api_restfull.model(
    "SendTextAPIOutcomeFields", {"id": fields.Integer, "text": fields.String}
)
RESPONSE_WITH_ERROR = api_restfull.model(
    "ResponseWithError", {"fieldNameWithProblem": fields.List(fields.String)}
)
ISOLATED_VOCABULARY_OUTCOME = api_restfull.model(
    "IsolatedVocabularyOutcome", {"vocabulary": fields.List(fields.String)}
)
NGRAM_VOCABULARY_OUTCOME = api_restfull.model(
    "NGramVocabularyOutcome", {"vocabulary": fields.List(fields.String)}
)

FREQUENCY = api_restfull.model("Frequency", {"texts": fields.List(fields.Integer)})

FREQUENCY_DISTRIBUTION_OUTCOME = api_restfull.model(
    "FrequencyDistributionOutcome", {"frequency": fields.Nested(FREQUENCY)}
)


@api_restfull.route("/send-text")
class SendTextAPI(Resource):
    @api_restfull.doc(body=SEND_TEXT_API_FIELD_INCOME)
    @api_restfull.response(201, "Success", SEND_TEXT_API_FIELD_OUTCOME)
    @api_restfull.response(400, "Validation Error", RESPONSE_WITH_ERROR)
    def post(self):
        json_data = request.get_json(force=True)
        schema = SendTextSchema()

        try:

            data = schema.load(json_data)

            text = Text()
            text.text = data.get("text")

            db.session.add(text)
            db.session.commit()

            data.update({"id": text.id})

            return schema.dump(data), 201

        except ValidationError as error:
            return error.messages, 400


@api_restfull.route("/isolated-vocabulary")
class IsolatedVocabularyApi(Resource):
    @api_restfull.response(200, "Success", ISOLATED_VOCABULARY_OUTCOME)
    def get(self):
        list_of_texts = [text for text, in db.session.query(Text.text).order_by(Text.id).all()]
        text_handler = TextHandler(list_of_texts)

        vocabulary = {"vocabulary": text_handler.sw_vocabulary()}
        schema = IsolatedVocabularySchema()

        return schema.load(vocabulary), 200


@api_restfull.route("/isolated-frequency-distribution")
class IsolatedFrequencyDistributionAPI(Resource):
    @api_restfull.response(200, "Success", FREQUENCY_DISTRIBUTION_OUTCOME)
    def get(self):
        list_of_texts = [text for text, in db.session.query(Text.text).order_by(Text.id).all()]
        text_handler = TextHandler(list_of_texts)

        frequency = {"frequency": text_handler.sw_frequency_distribution()}
        schema = FrequenceDistributionSchema()

        return schema.load(frequency), 200


@api_restfull.route("/ngran-vocabulary")
class NGramVocabularyAPI(Resource):
    @api_restfull.response(200, "Success", NGRAM_VOCABULARY_OUTCOME)
    def get(self):
        list_of_texts = [text for text, in db.session.query(Text.text).order_by(Text.id).all()]
        text_handler = TextHandler(list_of_texts)

        vocabulary = {"vocabulary": text_handler.ng_vocabulary()}

        schema = Gram2VocabularySchema()

        return schema.load(vocabulary), 200


@api_restfull.route("/ngran-frequency-distribution")
class NGramFrequencyDistributionAPI(Resource):
    @api_restfull.response(200, "Success", FREQUENCY_DISTRIBUTION_OUTCOME)
    def get(self):
        list_of_texts = [text for text, in db.session.query(Text.text).order_by(Text.id).all()]
        text_handler = TextHandler(list_of_texts)

        frequency = {"frequency": text_handler.ng_frequency_distribution()}

        schema = FrequenceDistributionSchema()

        return schema.load(frequency), 200
