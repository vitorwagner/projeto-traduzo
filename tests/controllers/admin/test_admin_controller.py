from src.models.history_model import HistoryModel
from src.models.user_model import UserModel


def test_history_delete(app_test):
    history = HistoryModel(
        {
            "text_to_translate": "Hello",
            "translate_from": "en",
            "translate_to": "pt",
            "translated": "Olá",
        }
    )
    history.save()

    user = UserModel(
        {
            "name": "test",
            "token": "777",
        }
    )
    user.save()

    app_test.delete(
        f"/admin/history/{history.data['_id']}",
        headers={
            "Authorization": "777",
            "User": "test",
        },
    )

    assert HistoryModel.find_one({"_id": history.data["_id"]}) is None
