#!/usr/bin/env python3
"""Admin CLI for the paid-API key registry (billing.py).

Usage:
    python scripts/manage_keys.py create <customer_id> --plan pro
    python scripts/manage_keys.py revoke <raw_key>
    python scripts/manage_keys.py list

Reads the SQLite path from BOARDCOMPOSER_DB_PATH, or --db-path.
"""

import argparse
import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from boardcomposer import billing, stripe_billing  # noqa: E402


def _db_path(args) -> str:
    path = args.db_path or os.environ.get("BOARDCOMPOSER_DB_PATH")
    if not path:
        raise SystemExit(
            "Falta la ruta de la base de datos: pásala con --db-path o define "
            "BOARDCOMPOSER_DB_PATH."
        )
    return path


def _cmd_create(args) -> None:
    db_path = _db_path(args)

    stripe_customer_id = None
    stripe_subscription_item_id = None
    if args.plan in billing.PAID_PLANS:
        if stripe_billing.is_configured(args.plan):
            stripe_customer_id, stripe_subscription_item_id = (
                stripe_billing.create_customer_and_subscription(
                    args.customer_id, args.plan
                )
            )
            print(f"Cliente Stripe creado: {stripe_customer_id}")
        else:
            print(
                "Aviso: Stripe no configurado (falta STRIPE_SECRET_KEY, o el "
                "Price de cuota fija, o el de overage de este plan) — la clave "
                "se emite igualmente, sin facturación automática de overage."
            )

    raw_key = billing.create_key(
        db_path,
        args.customer_id,
        args.plan,
        stripe_customer_id=stripe_customer_id,
        stripe_subscription_item_id=stripe_subscription_item_id,
    )
    print(f"Clave creada para {args.customer_id!r} (plan {args.plan}):")
    print(raw_key)
    print("\nGuárdala ahora — no se puede recuperar después (solo se guarda el hash).")


def _cmd_revoke(args) -> None:
    db_path = _db_path(args)
    if billing.revoke_key(db_path, args.raw_key):
        print("Clave revocada.")
    else:
        print("No se encontró esa clave.")
        raise SystemExit(1)


def _cmd_list(args) -> None:
    db_path = _db_path(args)
    billing.init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT customer_id, plan, active, created_at FROM api_keys "
            "ORDER BY created_at DESC"
        ).fetchall()

    if not rows:
        print("Sin claves registradas.")
        return

    for row in rows:
        status = "activa" if row["active"] else "revocada"
        print(
            f"{row['customer_id']:<20} {row['plan']:<8} {status:<9} {row['created_at']}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--db-path", help="Ruta al SQLite de claves (o BOARDCOMPOSER_DB_PATH)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("create", help="Emitir una clave nueva")
    create_parser.add_argument("customer_id")
    create_parser.add_argument(
        "--plan", choices=sorted(billing.PLAN_LIMITS), default="free"
    )
    create_parser.set_defaults(func=_cmd_create)

    revoke_parser = subparsers.add_parser("revoke", help="Revocar una clave existente")
    revoke_parser.add_argument("raw_key")
    revoke_parser.set_defaults(func=_cmd_revoke)

    list_parser = subparsers.add_parser("list", help="Listar todas las claves")
    list_parser.set_defaults(func=_cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
