import os
from dotenv import load_dotenv
from typing import List, Optional, Dict
from datetime import datetime
from ic.identity import Identity
from ic.client import Client
from ic.agent import Agent
from ic.candid import encode, Types
import requests

# 環境変数をロード
load_dotenv()

# VlyWallet APIのシークレットトークンを環境変数から取得
VLY_SECRET_TOKEN = os.getenv('VLY_SECRET_TOKEN')

def get_vly_wallet_addresses(user_ids: List[str]) -> Dict[str, Optional[str]]:
    addresses = {}
    for user_id in user_ids:
        url = f"https://service.vly.money/api/third_party/user_mapping?chain=icp&name={user_id}&scope=twitter"
        headers = {
            'secret-token': VLY_SECRET_TOKEN
        }
        try:
            print(f"リクエストURL: {url}")
            print(f"ヘッダー: {headers}")
            
            response = requests.get(url, headers=headers)
            print(f"ステータスコード: {response.status_code}")
            print(f"レスポンスヘッダー: {response.headers}")
            print(f"レスポンス本文: {response.text}")
            
            response.raise_for_status()
            data = response.json()
            address = data.get('data', {}).get('address')
            addresses[user_id] = address
            if address:
                print(f"ユーザー {user_id} のVlyWalletアドレス: {address}")
            else:
                print(f"ユーザー {user_id} のVlyWalletアドレスを取得できませんでした。")
        except requests.exceptions.RequestException as e:
            print(f"APIリクエストエラー: {e}")
            addresses[user_id] = None
        except ValueError as e:
            print(f"JSONデコードエラー: {e}")
            addresses[user_id] = None
    return addresses

def get_account_tx(account, query_amount):
    types = Types.Record({
        'max_results': Types.Nat,
        'start': Types.Opt(Types.Nat),
        'account': Types.Record({'owner': Types.Principal, 'subaccount': Types.Opt(Types.Vec(Types.Nat8))}),
    })
    values = {
        'max_results': query_amount,
        'start': [],
        'account': {'owner': account, 'subaccount': []},
    }
    params = [{'type': types, 'value': values}]
    return encode(params)

def query_transactions(agent, like_index, usr_account, query_amount, cutoff_date):
    while True:
        usr_tx = agent.query_raw(
            like_index,
            "get_account_transactions",
            get_account_tx(usr_account, query_amount)
        )
        processed_data = process_transactions(usr_tx)

        if len(processed_data) == query_amount:
            if any(tx['Timestamp'] >= cutoff_date for tx in processed_data):
                query_amount += query_amount
                print(f"Querying more transactions, new query amount: {query_amount}")
            else:
                print("No transactions after cutoff_date. Process complete.")
                new_transactions_count = sum(1 for tx in processed_data if tx['Timestamp'] >= cutoff_date)
                return new_transactions_count
        else:
            print("Transaction count is less than query_amount. Process complete.")
            new_transactions_count = sum(1 for tx in processed_data if tx['Timestamp'] >= cutoff_date)
            return new_transactions_count

def process_transactions(data):
    transactions = []
    for item in data:
        value = item.get('value', {})
        for key, details in value.items():
            records = details.get('_3331539157', [])
            for record in records:
                record_details = record.get('_1266835934', {})
                timestamp = record_details.get('_2781795542')
                operation = record_details.get('_1191829844')
                amount = record_details.get('_3664621355', [{}])[0].get('_3573748184', 0)
                sender = (
                    record_details.get('_3664621355', [{}])[0]
                    .get('_25979', {})
                    .get('_947296307', None)
                )
                receiver = (
                    record_details.get('_3664621355', [{}])[0]
                    .get('_1136829802', {})
                    .get('_947296307', None)
                )
                transactions.append({
                    'Transaction ID': record.get('_23515'),
                    'Type': operation,
                    'Sender': sender,
                    'Receiver': receiver,
                    'Amount': amount,
                    'Timestamp': timestamp
                })
    return transactions

def main(user_ids: List[str]) -> Dict[str, Optional[int]]:
    print(f"使用するシークレットトークン: {VLY_SECRET_TOKEN}")

    # VlyWalletアドレスを取得
    addresses = get_vly_wallet_addresses(user_ids)

    # ICRCトランザクション数を取得
    ano = Identity()
    client = Client(url="https://icp-api.io")
    agent = Agent(ano, client)
    like_index = "mvtuy-wiaaa-aaaam-adh7a-cai"
    query_amount = 100
    cutoff_date = datetime(2024, 11, 9, 0, 0, 0).timestamp()

    tx_counts = {}
    for user_id, address in addresses.items():
        if address:
            tx_count = query_transactions(agent, like_index, address, query_amount, cutoff_date)
            tx_counts[user_id] = tx_count
            print(f"ユーザー {user_id} のトランザクション数: {tx_count}")
        else:
            tx_counts[user_id] = None
            print(f"ユーザー {user_id} のトランザクション数を取得できませんでした。")

    return tx_counts

# 使用例
if __name__ == "__main__":
    # テスト用のユーザーID配列
    test_user_ids = ["mugeimunou", "realDonaldTrump"]
    result = main(test_user_ids)
    print("\nトランザクション数の結果:")
    print(result)