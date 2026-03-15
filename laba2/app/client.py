import argparse
import base64
import sys

import httpx

from app.crypto import KeyPair, Verifier


def run_scenario_1(base_url: str) -> None:
    """Подпись на стороне клиента: клиент подписывает сообщение, сервер верифицирует."""
    keypair = KeyPair()
    message = input("Введите сообщение: ")
    message_bytes = message.encode("utf-8")
    signature = keypair.sign(message_bytes)

    payload = {
        "message": message,
        "signature": base64.b64encode(signature).decode("ascii"),
        "public_key": keypair.get_public_key_pem().decode("utf-8"),
    }

    with httpx.Client(base_url=base_url) as client:
        response = client.post("/verify", json=payload)
        response.raise_for_status()
        data = response.json()

    verified = data.get("verified", False)
    print("Сценарий 1: Подпись на стороне клиента")
    msg_preview = message[:50] + ("..." if len(message) > 50 else "")
    print(f"  Сообщение: {msg_preview}")
    print(f"  Результат верификации на сервере: {'подпись верна' if verified else 'подпись неверна'}")


def run_scenario_2(base_url: str) -> None:
    """Подпись на стороне сервера: сервер подписывает сообщение, клиент верифицирует."""
    with httpx.Client(base_url=base_url) as client:
        # 1. Запросить открытый ключ сервера
        resp_key = client.get("/public-key")
        resp_key.raise_for_status()
        public_key_pem = resp_key.json()["public_key"]

        # 2. Запросить подписанное сообщение
        resp_signed = client.post("/signed-message")
        resp_signed.raise_for_status()
        data = resp_signed.json()
        message = data["message"]
        signature_b64 = data["signature"]

    signature = base64.b64decode(signature_b64)
    verifier = Verifier(public_key_pem.encode("utf-8"))
    message_bytes = message.encode("utf-8")
    verified = verifier.verify(message_bytes, signature)

    print("Сценарий 2: Подпись на стороне сервера")
    print(f"  Полученное сообщение: {message}")
    print(f"  Сообщение подлинное: {'да' if verified else 'нет'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Клиент ЭЦП — сценарии 1 и 2")
    parser.add_argument(
        "--scenario",
        "-s",
        type=int,
        choices=[1, 2],
        required=True,
        help="Номер сценария: 1 — подпись на клиенте, 2 — подпись на сервере",
    )
    parser.add_argument(
        "--url",
        "-u",
        default="http://127.0.0.1:8000",
        help="Базовый URL сервера (по умолчанию: http://127.0.0.1:8000)",
    )
    args = parser.parse_args()

    if args.scenario == 1:
        run_scenario_1(args.url)
    else:
        run_scenario_2(args.url)


if __name__ == "__main__":
    main()
