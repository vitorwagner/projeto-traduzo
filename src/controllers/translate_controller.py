from flask import Blueprint, render_template, request
from deep_translator import GoogleTranslator
from models.language_model import LanguageModel
from models.history_model import HistoryModel


translate_controller = Blueprint("translate_controller", __name__)


def _get_all_languages():
    return LanguageModel.list_dicts()


# Reqs. 4 e 5
@translate_controller.route("/", methods=["GET", "POST"])
def index():

    text_to_translate = (
        request.form.get("text-to-translate")
        if request.method == "POST"
        else ""
    )

    translate_from = (
        request.form.get("translate-from")
        if request.method == "POST"
        else "en"
    )

    translate_to = (
        request.form.get("translate-to") if request.method == "POST" else "pt"
    )

    translated = (
        GoogleTranslator(source=translate_from, target=translate_to).translate(
            text_to_translate
        )
        if request.method == "POST"
        else "Tradução"
    )

    if request.method == "POST":
        HistoryModel({
            "text_to_translate": text_to_translate,
            "translate_from": translate_from,
            "translate_to": translate_to,
            "translated": translated,
        }
        ).save()

    return render_template(
        "index.html",
        languages=_get_all_languages(),
        text_to_translate=text_to_translate,
        translate_from=translate_from,
        translate_to=translate_to,
        translated=translated,
    )


# Req. 6
@translate_controller.route("/reverse", methods=["POST"])
def reverse():
    translated = GoogleTranslator(
            source=request.form.get("translate-to"),
            target=request.form.get("translate-from"),
        ).translate(request.form.get("text-to-translate"))

    text_to_translate = GoogleTranslator(
            source=request.form.get("translate-from"),
            target=request.form.get("translate-to"),
        ).translate(translated)

    return render_template(
        "index.html",
        languages=_get_all_languages(),
        text_to_translate=text_to_translate,
        translate_from=request.form.get("translate-to"),
        translate_to=request.form.get("translate-from"),
        translated=translated,
    )
