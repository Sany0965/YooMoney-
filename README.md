# YooMoney-
# 📌 Как получить токен и настроить оплату через YooMoney

Этот гайд поможет вам получить токен и настроить прием платежей через ЮMoney в вашем Telegram-боте. (Также в репозитории в файлах есть телеграм бот, можете запустить, проверить как все работает, там все подробно расписано)

---

## 1. Создание кошелька ЮMoney

Если у вас еще нет кошелька, создайте его:  
🔗 [Регистрация ЮMoney](https://yoomoney.ru/)

📌 **Важно!** Для приема платежей ваш кошелек должен быть идентифицирован.

---

## 2. Регистрация приложения в ЮMoney

Чтобы ваш бот мог принимать платежи, нужно зарегистрировать приложение в ЮMoney:

### 2.1. Открываем "Мои сервисы"

Перейдите по ссылке:  
🔗 [Создать приложение](https://yoomoney.ru/myservices/new)

### 2.2. Указываем параметры

- **Название:** любое (например, "TelegramBot")
- **Redirect URI:** `https://t.me/ВАШ_БОТ` (замените на свой)

Нажмите **Подтвердить**.

### 2.3. Получаем данные

После регистрации вам выдадут:
- ✅ `client_id`
- ✅ `client_secret`
- ✅ `redirect_uri`

💾 **Сохраните эти данные**, они понадобятся для получения токена.

---

## 3. Получение access_token

Теперь вам нужно получить токен доступа, который позволит боту управлять платежами.

### 3.1. Устанавливаем библиотеку `yoomoney`

```bash
pip install yoomoney
```

### 3.2. Запускаем код для получения токена

```python
from yoomoney import Authorize

Authorize(
    client_id="ВАШ_CLIENT_ID",
    redirect_uri="ВАШ_REDIRECT_URI",
    client_secret="ВАШ_CLIENT_SECRET",
    scope=["account-info", "operation-history", "payment-shop"]
)
```

### 3.3. Что делать дальше?

📌 После запуска кода в консоли появится ссылка.

1. Перейдите по ссылке и войдите в ЮMoney.
2. Подтвердите доступ приложения.
3. После авторизации вас перенаправит на `redirect_uri`.
4. В адресной строке будет код (`code`).
5. Введите этот код в консоль.

✅ Если код верный, в консоли появится ваш `access_token`.

💾 **Сохраните этот токен**, он понадобится для работы бота!

---

## 4. Проверка токена

Чтобы убедиться, что ваш `access_token` работает, выполните код:

```python
from yoomoney import Client

token = "ВАШ_ACCESS_TOKEN"
client = Client(token)

user = client.account_info()
print("Номер кошелька:", user.account)
print("Баланс:", user.balance)
```

✅ Если всё правильно, вы увидите номер кошелька и баланс.

---

## Готово! 🎉

Теперь у вас есть `access_token`, и вы можете использовать его в своем Telegram-боте для приема платежей через Yoo?oney! 🚀

💡 Если что-то не работает, пишите в [Telegram](https://t.me/worpli)!
